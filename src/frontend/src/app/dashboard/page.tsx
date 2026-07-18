/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppShell from "../../components/app-shell";
import api from "../../lib/api";

interface Course {
  course_code: string;
  name: string;
  description: string;
}

interface DocumentContrib {
  id: string;
  title: string;
  course_code: string;
  status: string;
  uploaded_at: string;
  file_size_bytes: number;
  review_reason: string | null;
}

// Map a document status to a Vietnamese label + Tailwind badge classes.
const PROCESSING_BADGE = {
  label: "Đang xử lý",
  classes: "text-blue-600 bg-blue-50 border-blue-100",
};
const PENDING_BADGE = {
  label: "Chờ duyệt",
  classes: "text-slate-600 bg-slate-50 border-slate-200",
};
const APPROVED_BADGE = {
  label: "Đã duyệt",
  classes: "text-system-green bg-green-50 border-green-100",
};

// Maps the backend DocumentStatus pipeline (UPLOADED → PARSING → EVALUATING →
// NEEDS_REVIEW → APPROVED → INDEXING → INDEXED, plus REJECTED/FAILED) to badges.
const STATUS_BADGE: Record<string, { label: string; classes: string }> = {
  UPLOADED: PROCESSING_BADGE,
  PARSING: PROCESSING_BADGE,
  EVALUATING: PROCESSING_BADGE,
  INDEXING: PROCESSING_BADGE,
  PROCESSING: PROCESSING_BADGE,
  PENDING: PENDING_BADGE,
  NEEDS_REVIEW: PENDING_BADGE,
  APPROVED: APPROVED_BADGE,
  INDEXED: APPROVED_BADGE,
  REJECTED: {
    label: "Bị từ chối",
    classes: "text-system-red bg-red-50 border-red-100",
  },
  FAILED: {
    label: "Lỗi xử lý",
    classes: "text-orange-600 bg-orange-50 border-orange-100",
  },
};

const getStatusBadge = (status: string) =>
  STATUS_BADGE[status] || {
    label: "Không xác định",
    classes: "text-slate-500 bg-slate-50 border-slate-200",
  };

interface LeaderboardItem {
  user_id: string;
  full_name: string;
  points: number;
  rank: number;
}

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState<"my-courses" | "my-contributions">("my-courses");
  const [searchQuery, setSearchQuery] = useState("");
  const [courses, setCourses] = useState<Course[]>([]);
  const [contributions, setContributions] = useState<DocumentContrib[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [rejectedDoc, setRejectedDoc] = useState<DocumentContrib | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [coursesData, docsData, leaderboardData] = await Promise.all([
          api.get<any[]>("/courses"),
          api.get<any[]>("/documents"),
          api.get<LeaderboardItem[]>("/leaderboard/global"),
        ]);
        
        // Map backend 'code' to frontend 'course_code'
        const mappedCourses = (coursesData || []).map((c: any) => ({
          ...c,
          course_code: c.code,
        }));
        setCourses(mappedCourses);

        // Map backend document fields using a course map
        const courseMap = new Map((coursesData || []).map((c: any) => [c.id, c.code]));
        const mappedDocs = (docsData || []).map((d: any) => ({
          ...d,
          title: d.original_filename || "Tài liệu",
          course_code: courseMap.get(d.course_id) || "IT3160E",
          file_size_bytes: d.file_size_bytes || 5242880, // 5MB default
          review_reason:
            d.review_reason ?? d.note ?? d.reason ?? d.error_message ?? null,
        }));
        setContributions(mappedDocs);
        
        setLeaderboard(leaderboardData || []);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Filter courses based on query
  const filteredCourses = courses.filter(
    (c) =>
      c.course_code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const dm = 1;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Top Header Panel */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white border border-whisper-border rounded-2xl p-6 shadow-sm">
          <div>
            <h1 className="text-2xl font-black text-slate-900 font-headline-lg">
              Bảng điều khiển học tập
            </h1>
            <p className="text-xs text-muted-steel font-semibold">
              Quản lý khóa học, theo dõi tiến độ số hóa học liệu và tương tác cùng AI
            </p>
          </div>
          <div className="relative w-full md:w-72">
            <input
              type="text"
              placeholder="Tìm kiếm môn học..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-canvas-base border border-whisper-border rounded-xl pl-10 pr-4 py-2 text-xs font-semibold outline-none focus:ring-2 focus:ring-hust-red transition-all"
            />
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-[18px]">
              search
            </span>
          </div>
        </div>

        {/* Dashboard Grid split into content and leaderboard sidebar */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Main Course Content (8 Cols) */}
          <div className="lg:col-span-8 space-y-6">
            
            {/* Tabs Selector */}
            <div className="flex border-b border-whisper-border">
              <button
                onClick={() => setActiveTab("my-courses")}
                className={`pb-3 px-4 text-xs font-bold transition-all border-b-2 ${
                  activeTab === "my-courses"
                    ? "border-hust-red text-hust-red"
                    : "border-transparent text-muted-steel hover:text-slate-700"
                }`}
              >
                Môn học của tôi ({filteredCourses.length})
              </button>
              <button
                onClick={() => setActiveTab("my-contributions")}
                className={`pb-3 px-4 text-xs font-bold transition-all border-b-2 ${
                  activeTab === "my-contributions"
                    ? "border-hust-red text-hust-red"
                    : "border-transparent text-muted-steel hover:text-slate-700"
                }`}
              >
                Đóng góp của tôi ({contributions.length})
              </button>
            </div>

            {activeTab === "my-courses" ? (
              /* Course Grid */
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredCourses.map((course) => (
                  <div
                    key={course.course_code}
                    className="bg-white border border-whisper-border hover:border-hust-red/40 rounded-2xl p-5 shadow-xs flex flex-col justify-between transition-all group"
                  >
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-label-mono text-[10px] font-bold text-hust-red bg-red-50 border border-red-100 px-2 py-0.5 rounded-md">
                          {course.course_code}
                        </span>
                        <span className="text-[10px] text-muted-steel font-bold uppercase tracking-wider">
                          SOICT
                        </span>
                      </div>
                      <h3 className="font-headline-md text-sm font-extrabold text-slate-900 group-hover:text-hust-red transition-colors line-clamp-1">
                        {course.name}
                      </h3>
                      <p className="text-[11px] text-slate-500 font-semibold line-clamp-2 leading-relaxed">
                        {course.description}
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-50 flex justify-between items-center">
                      <span className="text-[10px] text-slate-400 font-semibold italic">
                        SOICT Academic
                      </span>
                      <Link
                        href={`/courses/${course.course_code}`}
                        className="tactile-button text-[11px] py-1 px-3.5 hover:bg-canvas-base border border-whisper-border text-slate-800"
                      >
                        Vào học
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              /* Contributions List */
              <div className="space-y-3">
                {contributions.map((contrib) => {
                  const badge = getStatusBadge(contrib.status);
                  const isRejected = contrib.status === "REJECTED";
                  return (
                    <div
                      key={contrib.id}
                      onClick={isRejected ? () => setRejectedDoc(contrib) : undefined}
                      role={isRejected ? "button" : undefined}
                      tabIndex={isRejected ? 0 : undefined}
                      onKeyDown={
                        isRejected
                          ? (e) => {
                              if (e.key === "Enter" || e.key === " ") {
                                e.preventDefault();
                                setRejectedDoc(contrib);
                              }
                            }
                          : undefined
                      }
                      className={`bg-white border border-whisper-border rounded-xl p-4 flex items-center justify-between gap-4 transition-all ${
                        isRejected
                          ? "cursor-pointer hover:border-system-red/40 hover:shadow-sm"
                          : ""
                      }`}
                    >
                      <div className="space-y-1 min-w-0">
                        <p className="text-xs font-bold text-slate-800 truncate">
                          {contrib.title}
                        </p>
                        <div className="flex items-center gap-3 text-[10px] font-semibold text-muted-steel">
                          <span className="font-label-mono font-bold text-hust-red bg-red-50 px-1 rounded-md">
                            {contrib.course_code}
                          </span>
                          <span>{formatBytes(contrib.file_size_bytes)}</span>
                          <span>Tải lên lúc: {new Date(contrib.uploaded_at).toLocaleDateString()}</span>
                        </div>
                        {isRejected && (
                          <p className="text-[10px] font-semibold text-system-red/80 italic">
                            Nhấn để xem lý do từ chối
                          </p>
                        )}
                      </div>

                      <div className="flex items-center gap-2">
                        <span
                          className={`text-[10px] font-bold ${badge.classes} border px-2 py-0.5 rounded-full uppercase`}
                        >
                          {badge.label}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Leaderboard Sidebar (4 Cols) */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-white border border-whisper-border rounded-2xl p-6 shadow-sm space-y-4">
              <div>
                <h3 className="font-headline-md text-sm font-black text-slate-900">
                  Bảng xếp hạng đóng góp
                </h3>
                <p className="text-[10px] text-muted-steel font-semibold">
                  Tích lũy điểm đóng góp để mở khóa các huy hiệu học thuật
                </p>
              </div>

              <div className="space-y-3">
                {leaderboard.map((item) => (
                  <div
                    key={item.user_id}
                    className="flex items-center justify-between p-2 rounded-xl hover:bg-canvas-base/50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span
                        className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                          item.rank === 1
                            ? "bg-amber-500 text-white"
                            : item.rank === 2
                            ? "bg-slate-400 text-white"
                            : item.rank === 3
                            ? "bg-amber-700 text-white"
                            : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {item.rank}
                      </span>
                      <div>
                        <p className="text-xs font-bold text-slate-800">{item.full_name}</p>
                        <p className="text-[9px] text-muted-steel font-semibold font-label-mono">
                          ID: {item.user_id.slice(0, 8)}
                        </p>
                      </div>
                    </div>
                    <span className="font-label-mono text-xs font-extrabold text-hust-red">
                      {item.points} XP
                    </span>
                  </div>
                ))}

                {leaderboard.length < 3 && (
                  <div className="mt-2 rounded-xl border border-dashed border-hust-red/30 bg-red-50/40 p-3 text-center">
                    <span className="material-symbols-outlined text-hust-red text-[20px]">
                      emoji_events
                    </span>
                    <p className="text-[11px] font-bold text-slate-800 mt-1">
                      Hãy là người đầu tiên dẫn đầu bảng xếp hạng!
                    </p>
                    <p className="text-[10px] font-semibold text-muted-steel">
                      Đóng góp tài liệu để ghi điểm.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Rejection reason modal (item 2) */}
      {rejectedDoc && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4"
          onClick={() => setRejectedDoc(null)}
        >
          <div
            className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6 space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="font-headline-md text-sm font-black text-slate-900">
                  Tài liệu bị từ chối
                </h3>
                <p className="text-[11px] font-semibold text-muted-steel truncate">
                  {rejectedDoc.title}
                </p>
              </div>
              <button
                onClick={() => setRejectedDoc(null)}
                className="text-slate-400 hover:text-slate-700 transition-colors"
                aria-label="Đóng"
              >
                <span className="material-symbols-outlined text-[20px]">close</span>
              </button>
            </div>

            <div className="rounded-xl border border-red-100 bg-red-50/60 p-4">
              <p className="text-[10px] font-bold text-system-red uppercase tracking-wider mb-1">
                Lý do từ chối
              </p>
              <p className="text-xs font-semibold text-slate-700 leading-relaxed">
                {rejectedDoc.review_reason ||
                  "Chưa có lý do chi tiết. Vui lòng liên hệ người kiểm duyệt môn học."}
              </p>
            </div>

            <div className="flex justify-end gap-2 pt-1">
              <button
                onClick={() => setRejectedDoc(null)}
                className="tactile-button text-[11px] py-1.5 px-3.5 hover:bg-canvas-base border border-whisper-border text-slate-800"
              >
                Đóng
              </button>
              <Link
                href={`/courses/${rejectedDoc.course_code}`}
                className="tactile-button text-[11px] py-1.5 px-3.5 bg-hust-red text-white hover:bg-hust-red/90"
              >
                Gửi lại tài liệu
              </Link>
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
