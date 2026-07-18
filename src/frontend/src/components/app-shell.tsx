/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import api from "../lib/api";

export interface User {
  id?: string;
  user_id?: string;
  email: string;
  full_name: string;
  role: "admin" | "reviewer" | "student";
}

// Route → which roles may access it. Prefix match: "/courses" covers "/courses/IT3210".
const ROUTE_ROLES: Array<{ prefix: string; roles: string[] }> = [
  { prefix: "/dashboard", roles: ["student"] },
  { prefix: "/courses",   roles: ["student"] },
  { prefix: "/search",    roles: ["student"] },
  { prefix: "/profile",   roles: ["student"] },
  { prefix: "/leaderboard", roles: ["student", "reviewer", "admin"] },
  { prefix: "/my-documents", roles: ["student"] },
  { prefix: "/review",    roles: ["reviewer"] },
  { prefix: "/official-upload", roles: ["reviewer", "admin"] },
  { prefix: "/manage-documents", roles: ["reviewer", "admin"] },
  { prefix: "/admin/users", roles: ["admin"] },
  { prefix: "/admin",     roles: ["admin"] },
  { prefix: "/register",  roles: ["admin"] },
];

const HOME_BY_ROLE: Record<string, string> = {
  student:  "/dashboard",
  reviewer: "/review",
  admin:    "/admin",
};

// Vietnamese labels for known route segments. Unknown segments (e.g. course
// codes like "IT3292E") fall back to their raw value untouched.
const BREADCRUMB_LABELS: Record<string, string> = {
  search:    "Tìm kiếm",
  review:    "Kiểm duyệt",
  profile:   "Trang cá nhân",
  dashboard: "Bảng điều khiển",
  courses:   "Môn học",
  admin:     "Quản trị",
  register:  "Đăng ký người dùng",
  leaderboard: "Bảng xếp hạng",
  "my-documents": "Tài liệu của tôi",
  "official-upload": "Tải tài liệu chính thức",
  "manage-documents": "Quản lý tài liệu",
};

const navigationConfig = {
  student: [
    { name: "Tổng quan học tập", href: "/dashboard", icon: "dashboard" },
    { name: "Tài liệu của tôi", href: "/my-documents", icon: "folder_shared" },
    { name: "Bảng xếp hạng", href: "/leaderboard", icon: "emoji_events" },
    { name: "Tìm kiếm toàn cầu", href: "/search", icon: "search" },
    { name: "Trang cá nhân", href: "/profile", icon: "person" },
  ],
  reviewer: [
    { name: "Hàng đợi phê duyệt", href: "/review", icon: "rate_review" },
    { name: "Tải tài liệu chính thức", href: "/official-upload", icon: "upload_file" },
    { name: "Quản lý tài liệu", href: "/manage-documents", icon: "folder_managed" },
    { name: "Bảng xếp hạng", href: "/leaderboard", icon: "emoji_events" },
  ],
  admin: [
    { name: "Bảng quản trị Admin", href: "/admin", icon: "admin_panel_settings" },
    { name: "Quản lý người dùng", href: "/admin/users", icon: "manage_accounts" },
    { name: "Tải tài liệu chính thức", href: "/official-upload", icon: "upload_file" },
    { name: "Quản lý tài liệu", href: "/manage-documents", icon: "folder_managed" },
    { name: "Bảng xếp hạng", href: "/leaderboard", icon: "emoji_events" },
  ],
};

interface NotificationItem {
  id: string;
  type: string;
  message: string;
  created_at: string;
}

// Format an ISO timestamp into a short Vietnamese relative time.
function relativeTime(iso: string): string {
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return "";
  const diffSec = Math.max(0, Math.floor((Date.now() - then) / 1000));
  if (diffSec < 60) return "Vừa xong";
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin < 60) return `${diffMin} phút trước`;
  const diffHour = Math.floor(diffMin / 60);
  if (diffHour < 24) return `${diffHour} giờ trước`;
  const diffDay = Math.floor(diffHour / 24);
  return `${diffDay} ngày trước`;
}

const NOTIFICATION_STYLE: Record<string, { icon: string; iconColor: string; bg: string }> = {
  status_approved: { icon: "check_circle", iconColor: "text-emerald-500", bg: "bg-emerald-50" },
  status_indexed: { icon: "database", iconColor: "text-teal-500", bg: "bg-teal-50" },
  status_rejected: { icon: "cancel", iconColor: "text-rose-500", bg: "bg-rose-50" },
  status_failed: { icon: "error", iconColor: "text-rose-500", bg: "bg-rose-50" },
  document_deleted: { icon: "delete_forever", iconColor: "text-rose-500", bg: "bg-rose-50" },
  status_needs_review: { icon: "rate_review", iconColor: "text-amber-500", bg: "bg-amber-50" },
};

function getNotificationStyle(type: string) {
  return NOTIFICATION_STYLE[type] || { icon: "info", iconColor: "text-slate-500", bg: "bg-slate-50" };
}

// How many notifications to fetch per "load more" page.
const NOTIFICATION_PAGE_SIZE = 10;

export default function AppShell({
  children,
  fullBleed = false,
}: {
  children: React.ReactNode;
  // App-like pages (e.g. the course workspace) manage their own internal
  // scrolling. fullBleed keeps the outer <main> fixed (no scroll, no padding)
  // so only inner panels scroll.
  fullBleed?: boolean;
}) {
  const pathname = usePathname();
  const router = useRouter();

  // Role management for demo purposes
  const [currentRole, setCurrentRole] = useState<"student" | "reviewer" | "admin">("student");
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  // Read-state is tracked client-side: the API has no is_read column and many
  // items are derived on the fly from document state logs, so persisting read
  // status in localStorage (keyed by stable notification id) is the pragmatic
  // approach.
  const [readIds, setReadIds] = useState<Set<string>>(new Set());
  // hasMoreNotifications: whether the server may have older notifications to
  // load; isLoadingMore guards the "load more" request.
  const [hasMoreNotifications, setHasMoreNotifications] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  // Load initial collapsed state from localStorage on client mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("sidebar-collapsed");
      if (saved === "true") {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setIsSidebarCollapsed(true);
      }
    }
  }, []);

  // Load persisted read-notification ids on client mount.
  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      const saved = localStorage.getItem("notifications-read");
      if (saved) {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setReadIds(new Set(JSON.parse(saved) as string[]));
      }
    } catch {
      /* ignore malformed cache */
    }
  }, []);

  // Poll notifications every 60 seconds when logged in
  useEffect(() => {
    if (!currentUser) return;
    const fetchNotifications = async () => {
      try {
        const notifs = await api.get<NotificationItem[]>(
          `/notifications?limit=${NOTIFICATION_PAGE_SIZE}&offset=0`
        );
        const fresh = Array.isArray(notifs) ? notifs : [];
        // Refresh the first page but keep any older pages the user loaded.
        setNotifications((prev) => {
          const freshIds = new Set(fresh.map((n) => n.id));
          const tail = prev.slice(fresh.length).filter((n) => !freshIds.has(n.id));
          return [...fresh, ...tail];
        });
      } catch (err) {
        console.error("Failed to poll notifications:", err);
      }
    };
    const interval = setInterval(fetchNotifications, 60000);
    return () => clearInterval(interval);
  }, [currentUser]);

  // Sync current user based on actual logged in state
  useEffect(() => {
    const fetchProfile = async () => {
      const token = typeof window !== 'undefined' ? localStorage.getItem("token") : null;
      if (!token) {
        // Only redirect if not on /login
        if (pathname !== "/login" && pathname !== "/register") {
          router.push("/login");
        }
        return;
      }
      try {
        const user = await api.get<any>("/auth/me");
        setCurrentUser(user);
        setCurrentRole(user.role as "student" | "reviewer" | "admin");

        try {
          const notifs = await api.get<NotificationItem[]>(
            `/notifications?limit=${NOTIFICATION_PAGE_SIZE}&offset=0`
          );
          const fresh = Array.isArray(notifs) ? notifs : [];
          setNotifications(fresh);
          setHasMoreNotifications(fresh.length === NOTIFICATION_PAGE_SIZE);
        } catch (notifErr) {
          console.error("Failed to load notifications:", notifErr);
        }

        // RBAC: find the first rule whose prefix matches current pathname
        const rule = ROUTE_ROLES.find(r => pathname.startsWith(r.prefix));
        if (rule && !rule.roles.includes(user.role)) {
          router.replace(HOME_BY_ROLE[user.role] ?? "/dashboard");
        }
      } catch (err) {
        console.error("Failed to load user profile:", err);
        if (pathname !== "/login" && pathname !== "/register") {
          router.push("/login");
        }
      }
    };
    fetchProfile();
  }, [pathname, router]);

  // Profile display variables
  const userInitials = currentUser?.full_name
    ? currentUser.full_name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .slice(-2)
        .toUpperCase()
    : "ST";

  const currentNav = navigationConfig[currentRole];

  // Notification read-state helpers (persisted to localStorage).
  const persistReadIds = (next: Set<string>) => {
    setReadIds(next);
    if (typeof window !== "undefined") {
      localStorage.setItem("notifications-read", JSON.stringify(Array.from(next)));
    }
  };
  const markRead = (id: string) => {
    if (readIds.has(id)) return;
    persistReadIds(new Set(readIds).add(id));
  };
  const markAllRead = () => {
    const next = new Set(readIds);
    notifications.forEach((n) => next.add(n.id));
    persistReadIds(next);
  };
  const unreadCount = notifications.reduce((acc, n) => acc + (readIds.has(n.id) ? 0 : 1), 0);

  // Fetch the next page of older notifications and append them.
  const loadMoreNotifications = async () => {
    if (isLoadingMore) return;
    setIsLoadingMore(true);
    try {
      const next = await api.get<NotificationItem[]>(
        `/notifications?limit=${NOTIFICATION_PAGE_SIZE}&offset=${notifications.length}`
      );
      const arr = Array.isArray(next) ? next : [];
      setNotifications((prev) => {
        const seen = new Set(prev.map((n) => n.id));
        return [...prev, ...arr.filter((n) => !seen.has(n.id))];
      });
      setHasMoreNotifications(arr.length === NOTIFICATION_PAGE_SIZE);
    } catch (err) {
      console.error("Failed to load more notifications:", err);
    } finally {
      setIsLoadingMore(false);
    }
  };

  // Dynamically generate breadcrumbs based on pathname
  const paths = pathname.split("/").filter((x) => x);
  const breadcrumbs = [
    { name: "Trang chủ", href: "/" },
    ...paths.map((p, index) => {
      const href = "/" + paths.slice(0, index + 1).join("/");
      // Known segments get a Vietnamese label; unknown segments (e.g. course
      // codes) keep their raw value as-is.
      const name = BREADCRUMB_LABELS[p] ?? p;
      return { name, href };
    }),
  ];

  return (
    <div className="flex h-screen w-full bg-canvas-base text-charcoal-ink overflow-hidden font-body-md">
      {/* 1. Sidebar */}
      <aside
        className={`bg-white flex flex-col justify-between flex-shrink-0 transition-all duration-300 ease-in-out ${
          isSidebarCollapsed
            ? "w-0 opacity-0 overflow-hidden border-r-0"
            : "w-64 border-r-1.5 border-whisper-border"
        }`}
      >
        <div className="w-64 flex flex-col h-full justify-between flex-shrink-0">
          <div>
            {/* Logo Brand Header */}
            <div className="p-6 border-b-1.5 border-whisper-border flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <img alt="Academic Commons Logo" className="w-8 h-8 object-contain" src="/assets/logo.svg" />
                <div>
                  <h1 className="font-headline-md font-extrabold text-[16px] text-hust-red leading-tight">
                    Academic Commons
                  </h1>
                </div>
              </div>
              <button
                onClick={() => {
                  setIsSidebarCollapsed(true);
                  localStorage.setItem("sidebar-collapsed", "true");
                }}
                className="p-1.5 rounded-lg hover:bg-canvas-base text-muted-steel hover:text-charcoal-ink transition-all duration-200 hover:scale-105 active:scale-95 flex items-center justify-center"
                title="Thu gọn menu"
              >
                <span className="material-symbols-outlined text-[18px]">chevron_left</span>
              </button>
            </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1">
            <div className="px-3 py-2 text-[11px] font-bold text-muted-steel tracking-wider uppercase font-headline-md">
              Mục lục ({currentRole === "student" ? "Sinh viên" : currentRole === "reviewer" ? "Người duyệt" : "Quản trị"})
            </div>
            {currentNav.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-xl font-body-sm font-semibold transition-all group ${
                    isActive
                      ? "bg-hust-red text-white"
                      : "text-muted-steel hover:bg-canvas-base hover:text-charcoal-ink"
                  }`}
                >
                  <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                  <span className="text-[14px]">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Sidebar Footer with Role Switcher & User Profile Metadata */}
        <div className="p-4 border-t-1.5 border-whisper-border bg-canvas-base/50 space-y-3">
          {/* User profile card */}
          <div className="flex items-center gap-3 p-2 bg-white border border-whisper-border rounded-xl">
            <div className="w-9 h-9 rounded-full bg-hust-red/10 text-hust-red flex items-center justify-center font-bold text-xs">
              {userInitials}
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-bold text-charcoal-ink truncate">
                {currentUser?.full_name || "Khách HUST"}
              </p>
              <p className="text-[10px] text-muted-steel truncate font-label-mono">
                {currentUser?.email || ""}
              </p>
            </div>
          </div>
        </div>
      </div>
      </aside>

      {/* 2. Main Content Canvas */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header bar */}
        <header className="h-16 bg-white border-b-1.5 border-whisper-border flex items-center justify-between px-6 flex-shrink-0 z-30">
          <div className="flex items-center gap-4">
            {isSidebarCollapsed && (
              <button
                onClick={() => {
                  setIsSidebarCollapsed(false);
                  localStorage.setItem("sidebar-collapsed", "false");
                }}
                className="w-9 h-9 rounded-xl border border-whisper-border bg-white flex items-center justify-center hover:bg-canvas-base text-muted-steel hover:text-charcoal-ink shadow-sm transition-all duration-200 hover:scale-105 active:scale-95"
                title="Mở menu"
              >
                <span className="material-symbols-outlined text-[20px]">menu</span>
              </button>
            )}

            {/* Breadcrumbs */}
            <nav className="flex items-center gap-1.5 text-xs text-muted-steel font-semibold">
              {breadcrumbs.map((crumb, index) => (
                <React.Fragment key={crumb.href}>
                  {index > 0 && <span className="text-slate-300 font-light">/</span>}
                  {index === breadcrumbs.length - 1 ? (
                    <span className="text-charcoal-ink font-bold">{crumb.name}</span>
                  ) : index === 0 ? (
                    <Link href={crumb.href} className="hover:text-hust-red transition-colors">
                      {crumb.name}
                    </Link>
                  ) : (
                    // Intermediate segments (e.g. "Courses") have no index page,
                    // so render them as plain text instead of broken links.
                    <span>{crumb.name}</span>
                  )}
                </React.Fragment>
              ))}
            </nav>
          </div>

          {/* Right widgets */}
          <div className="flex items-center gap-4">
            {/* Notification bell dropdown */}
            <div className="relative">
              <button
                onClick={() => setIsNotificationsOpen(!isNotificationsOpen)}
                className="w-9 h-9 rounded-full border-1.5 border-whisper-border flex items-center justify-center hover:bg-canvas-base transition-colors relative"
              >
                <span className="material-symbols-outlined text-[20px] text-slate-600">notifications</span>
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-system-red rounded-full border-2 border-white animate-pulse"></span>
                )}
              </button>

              {isNotificationsOpen && (
                <>
                  <div
                    className="fixed inset-0 z-40"
                    onClick={() => setIsNotificationsOpen(false)}
                  ></div>
                  {/* Notifications Dropdown: scrollable list, per-item read
                      marking (click), "mark all as read", and "load more". */}
                  <div className="absolute right-0 mt-2 w-80 bg-white border-1.5 border-whisper-border rounded-2xl shadow-xl z-50 flex flex-col max-h-[28rem]">
                    <div className="flex justify-between items-center p-4 pb-3 border-b border-whisper-border">
                      <div className="flex items-center gap-1.5">
                        <span className="material-symbols-outlined text-[16px] text-hust-red">notifications_active</span>
                        <span className="text-xs font-bold text-charcoal-ink">Nhật ký xử lý tài liệu</span>
                      </div>
                      {unreadCount > 0 && (
                        <span className="text-[10px] font-bold text-hust-red bg-red-50 px-2 py-0.5 rounded-full animate-pulse">
                          {unreadCount} tin mới
                        </span>
                      )}
                    </div>

                    {unreadCount > 0 && (
                      <button
                        onClick={markAllRead}
                        className="flex items-center justify-center gap-1 px-4 py-2 text-[11px] font-semibold text-hust-red hover:bg-red-50 transition-colors border-b border-whisper-border"
                      >
                        <span className="material-symbols-outlined text-[14px]">done_all</span>
                        Đánh dấu tất cả đã đọc
                      </button>
                    )}

                    <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
                      {notifications.length === 0 ? (
                        <p className="text-xs text-muted-steel py-6 text-center">Không có thông báo nào</p>
                      ) : (
                        notifications.map((notif) => {
                          const style = getNotificationStyle(notif.type);
                          const isRead = readIds.has(notif.id);
                          return (
                            <button
                              key={notif.id}
                              onClick={() => markRead(notif.id)}
                              className={`w-full flex items-start gap-3 p-2.5 rounded-xl text-left transition-colors border border-transparent ${
                                isRead ? "hover:bg-slate-50" : "bg-red-50/40 hover:bg-red-50"
                              }`}
                            >
                              <div className={`w-8 h-8 rounded-lg ${style.bg} flex items-center justify-center flex-shrink-0`}>
                                <span className={`material-symbols-outlined text-[18px] ${style.iconColor}`}>
                                  {style.icon}
                                </span>
                              </div>
                              <div className="min-w-0 flex-1">
                                <p className={`text-[12px] leading-snug ${isRead ? "text-slate-500 font-medium" : "text-slate-700 font-semibold"}`}>
                                  {notif.message}
                                </p>
                                <span className="text-[9px] text-muted-steel font-label-mono block mt-1">
                                  {relativeTime(notif.created_at)}
                                </span>
                              </div>
                              {!isRead && (
                                <span className="w-2 h-2 mt-1 rounded-full bg-hust-red flex-shrink-0"></span>
                              )}
                            </button>
                          );
                        })
                      )}
                    </div>

                    {notifications.length > 0 && hasMoreNotifications && (
                      <button
                        onClick={loadMoreNotifications}
                        disabled={isLoadingMore}
                        className="flex items-center justify-center gap-1 px-4 py-2.5 text-[11px] font-semibold text-slate-600 hover:bg-canvas-base transition-colors border-t border-whisper-border rounded-b-2xl disabled:opacity-60"
                      >
                        {isLoadingMore ? (
                          "Đang tải..."
                        ) : (
                          <>
                            <span className="material-symbols-outlined text-[14px]">expand_more</span>
                            Tải thêm tin nhắn
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </>
              )}
            </div>

            {/* Logout/Redirection Button */}
            <Link
              href="/login"
              onClick={() => {
                if (typeof window !== 'undefined') {
                  localStorage.removeItem("token");
                }
              }}
              className="tactile-button text-[12px] py-1.5 px-3 bg-white hover:bg-canvas-base border border-whisper-border text-slate-700"
            >
              Đăng xuất
            </Link>
          </div>
        </header>

        {/* Dynamic page component canvas wrapper */}
        <main className={`flex-1 bg-canvas-base ${fullBleed ? "overflow-hidden" : "overflow-y-auto p-6"}`}>
          {children}
        </main>
      </div>
    </div>
  );
}
