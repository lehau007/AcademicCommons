"use client";

import React, { useEffect, useState } from "react";
import AppShell from "../../../components/app-shell";
import api from "../../../lib/api";
import { useAsyncAction } from "../../../lib/useAsyncAction";
import { useToast } from "../../../components/toast";
import ConfirmDialog from "../../../components/confirm-dialog";
import { UserCog, Search, RefreshCw, Info } from "lucide-react";

type Role = "student" | "reviewer" | "admin";

interface UserRead {
  id: string;
  email: string;
  role: Role;
  full_name: string | null;
  is_active: boolean;
  created_at?: string;
}

const ROLE_LABELS: Record<Role, string> = {
  student: "Sinh viên",
  reviewer: "Người duyệt",
  admin: "Quản trị viên",
};

export default function AdminUsersPage() {
  const { showToast } = useToast();

  const [users, setUsers] = useState<UserRead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState<"" | Role>("");
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [updatingUserId, setUpdatingUserId] = useState<string | null>(null);
  const [confirmState, setConfirmState] = useState<{
    title: string;
    message: string;
    confirmLabel: string;
    variant: "danger" | "default";
    action: () => Promise<void>;
  } | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true);
      try {
        const res = await api.get<UserRead[]>("/admin/users", {
          params: roleFilter ? { role: roleFilter } : undefined,
        });
        setUsers(res);
      } catch (err) {
        showToast(
          err instanceof Error ? err.message : "Lỗi khi tải danh sách người dùng.",
          "error"
        );
      } finally {
        setIsLoading(false);
      }
    };
    fetchUsers();
  }, [roleFilter, showToast]);

  useEffect(() => {
    api
      .get<UserRead>("/auth/me")
      .then((me) => setCurrentUserId(me.id))
      .catch((err) => console.error("Failed to load current user:", err));
  }, []);

  const doRoleChange = async (targetUser: UserRead, newRole: Role) => {
    setUpdatingUserId(targetUser.id);
    try {
      const updated = await api.patch<UserRead>(`/admin/users/${targetUser.id}`, {
        role: newRole,
      });
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
      showToast(`Đã cập nhật vai trò của ${updated.email} thành ${ROLE_LABELS[updated.role]}.`, "success");
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Lỗi khi cập nhật vai trò.", "error");
    } finally {
      setUpdatingUserId(null);
    }
  };

  const handleRoleChange = (targetUser: UserRead, newRole: Role) => {
    if (newRole === targetUser.role) return;
    setConfirmState({
      title: "Đổi vai trò người dùng",
      message: `Bạn có chắc chắn muốn đổi vai trò của ${targetUser.email} thành "${ROLE_LABELS[newRole]}"?`,
      confirmLabel: "Đổi vai trò",
      variant: "default",
      action: () => doRoleChange(targetUser, newRole),
    });
  };

  const doToggleActive = async (targetUser: UserRead, nextActive: boolean) => {
    const verb = nextActive ? "kích hoạt lại" : "vô hiệu hóa";
    setUpdatingUserId(targetUser.id);
    try {
      const updated = await api.patch<UserRead>(`/admin/users/${targetUser.id}`, {
        is_active: nextActive,
      });
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
      showToast(`Đã ${verb} tài khoản ${updated.email}.`, "success");
    } catch (err) {
      showToast(err instanceof Error ? err.message : `Lỗi khi ${verb} tài khoản.`, "error");
    } finally {
      setUpdatingUserId(null);
    }
  };

  const handleToggleActive = (targetUser: UserRead) => {
    const nextActive = !targetUser.is_active;
    setConfirmState({
      title: nextActive ? "Kích hoạt lại tài khoản" : "Vô hiệu hóa tài khoản",
      message: nextActive
        ? `Bạn có chắc chắn muốn kích hoạt lại tài khoản ${targetUser.email}?`
        : `Bạn có chắc chắn muốn vô hiệu hóa tài khoản ${targetUser.email}? Người dùng sẽ không thể đăng nhập cho tới khi được kích hoạt lại.`,
      confirmLabel: nextActive ? "Kích hoạt lại" : "Vô hiệu hóa",
      variant: nextActive ? "default" : "danger",
      action: () => doToggleActive(targetUser, nextActive),
    });
  };

  const { pending: confirmBusy, run: runConfirm } = useAsyncAction(async () => {
    if (!confirmState) return;
    try {
      await confirmState.action();
    } finally {
      setConfirmState(null);
    }
  });

  const filteredUsers = users.filter((u) => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return true;
    return u.email.toLowerCase().includes(q) || (u.full_name ?? "").toLowerCase().includes(q);
  });

  return (
    <AppShell>
      <div className="flex flex-col h-full bg-canvas-base overflow-hidden">
        {/* Sub-header */}
        <header className="flex bg-white border-b border-whisper-border px-6 py-4 shrink-0 justify-between items-center gap-4 flex-wrap">
          <div>
            <h1 className="font-display font-extrabold text-[18px] text-charcoal-ink flex items-center gap-1.5">
              <UserCog className="w-5 h-5 text-hust-red" />
              <span>Quản lý người dùng</span>
            </h1>
            <p className="text-body-sm text-muted-steel mt-0.5">
              Tìm kiếm, phân quyền và kích hoạt/vô hiệu hóa tài khoản người dùng hệ thống.
            </p>
          </div>
          <div className="text-xs font-display font-extrabold text-charcoal-ink bg-slate-100 px-3 py-1 rounded-full border border-whisper-border">
            {users.length} người dùng
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-5xl mx-auto space-y-4 animate-in fade-in duration-200">
            {/* Filters */}
            <div className="tactile-card bg-white flex flex-wrap items-end gap-3">
              <div className="flex-1 min-w-[220px] space-y-1">
                <label className="block text-xs font-bold text-muted-steel uppercase">Tìm kiếm</label>
                <div className="relative">
                  <Search className="w-4 h-4 text-muted-steel absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 pl-9 text-body-md"
                    placeholder="Tìm theo email hoặc họ tên..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
              </div>
              <div className="space-y-1">
                <label className="block text-xs font-bold text-muted-steel uppercase">Vai trò</label>
                <select
                  className="bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md"
                  value={roleFilter}
                  onChange={(e) => setRoleFilter(e.target.value as "" | Role)}
                >
                  <option value="">Tất cả</option>
                  <option value="student">Sinh viên</option>
                  <option value="reviewer">Người duyệt</option>
                  <option value="admin">Quản trị viên</option>
                </select>
              </div>
            </div>

            {/* Users table */}
            <div className="border border-whisper-border rounded-xl overflow-hidden bg-white shadow-sm">
              <table className="w-full text-left text-body-sm">
                <thead className="bg-canvas-base border-b border-whisper-border text-muted-steel font-bold uppercase tracking-wider text-[10px]">
                  <tr>
                    <th className="p-3">Email</th>
                    <th className="p-3">Họ và tên</th>
                    <th className="p-3">Vai trò</th>
                    <th className="p-3">Trạng thái</th>
                    <th className="p-3">Ngày tạo</th>
                    <th className="p-3 text-right">Hành động</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-whisper-border">
                  {filteredUsers.map((u) => {
                    const isSelf = u.id === currentUserId;
                    const busy = updatingUserId === u.id;
                    return (
                      <tr key={u.id}>
                        <td className="p-3 font-mono text-xs">{u.email}</td>
                        <td className="p-3">
                          {u.full_name || <span className="text-muted-steel">—</span>}
                        </td>
                        <td className="p-3">
                          <select
                            className="bg-canvas-base border border-whisper-border rounded p-1.5 text-xs font-bold disabled:opacity-50 disabled:cursor-not-allowed"
                            value={u.role}
                            disabled={isSelf || busy}
                            title={isSelf ? "Không thể tự thay đổi vai trò của chính mình" : undefined}
                            onChange={(e) => handleRoleChange(u, e.target.value as Role)}
                          >
                            <option value="student">Sinh viên</option>
                            <option value="reviewer">Người duyệt</option>
                            <option value="admin">Quản trị viên</option>
                          </select>
                        </td>
                        <td className="p-3">
                          <span
                            className={`px-2 py-0.5 rounded text-xs font-semibold border ${
                              u.is_active
                                ? "bg-green-50 text-system-green border-system-green/20"
                                : "bg-red-50 text-system-red border-system-red/20"
                            }`}
                          >
                            {u.is_active ? "Hoạt động" : "Đã vô hiệu hóa"}
                          </span>
                        </td>
                        <td className="p-3 text-xs text-muted-steel font-mono">
                          {u.created_at ? new Date(u.created_at).toLocaleDateString("vi-VN") : "—"}
                        </td>
                        <td className="p-3 text-right">
                          <button
                            className="text-xs font-bold text-hust-red hover:underline disabled:opacity-50 disabled:cursor-not-allowed disabled:no-underline disabled:text-muted-steel"
                            disabled={isSelf || busy}
                            title={isSelf ? "Không thể tự vô hiệu hóa tài khoản của chính mình" : undefined}
                            onClick={() => handleToggleActive(u)}
                          >
                            {u.is_active ? "Vô hiệu hóa" : "Kích hoạt lại"}
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {!isLoading && filteredUsers.length === 0 && (
                <div className="text-center py-16">
                  <Info className="w-10 h-10 text-muted-steel mx-auto mb-2" />
                  <p className="text-body-sm text-muted-steel">Không tìm thấy người dùng phù hợp.</p>
                </div>
              )}

              {isLoading && (
                <div className="flex items-center justify-center py-16 gap-3">
                  <RefreshCw className="w-6 h-6 text-hust-red animate-spin" />
                  <p className="text-body-sm font-semibold text-muted-steel">Đang tải danh sách người dùng...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <ConfirmDialog
        open={confirmState !== null}
        title={confirmState?.title ?? ""}
        message={confirmState?.message ?? ""}
        confirmLabel={confirmState?.confirmLabel}
        variant={confirmState?.variant}
        busy={confirmBusy}
        onConfirm={runConfirm}
        onCancel={() => setConfirmState(null)}
      />
    </AppShell>
  );
}
