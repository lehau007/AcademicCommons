"use client";

import React, { useState } from "react";
import Link from "next/link";
import api from "../../lib/api";
import { useAsyncAction } from "../../lib/useAsyncAction";

export default function RegisterUserPage() {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [stage, setStage] = useState<"form" | "pending-verification">("form");
  const [error, setError] = useState("");
  const [resendStatus, setResendStatus] = useState<"idle" | "sending" | "sent" | "failed">("idle");

  const { pending: loading, run: handleSubmit } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password.length < 8) {
      setError("Mật khẩu phải có ít nhất 8 ký tự.");
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      setError("Mật khẩu và xác nhận mật khẩu không khớp.");
      return;
    }

    try {
      await api.post("/auth/register", {
        email: formData.email,
        full_name: formData.fullName,
        password: formData.password,
        role: "student",
      });
      setStage("pending-verification");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đăng ký thất bại. Vui lòng thử lại.");
    }
  });

  const handleResend = async () => {
    if (!formData.email) return;
    setResendStatus("sending");
    try {
      await api.post("/auth/resend-verification", { email: formData.email });
      setResendStatus("sent");
    } catch {
      setResendStatus("failed");
    }
  };

  return (
    <main className="flex h-screen w-full font-body-md text-on-surface antialiased bg-canvas-base select-none">

      {/* Left Column: Graphic & Branding */}
      <section className="hidden lg:flex w-1/2 h-full relative flex-col justify-end p-16 overflow-hidden" style={{ backgroundImage: "url('/assets/auth_illustration.jpg')", backgroundSize: "cover", backgroundPosition: "center" }}>
        {/* Direct watercolor feel with very light translucent mask */}
        <div className="absolute inset-0 bg-white/10 backdrop-blur-[0.5px] z-0"></div>

        {/* Logo anchor top-left */}
        <div className="absolute top-12 left-16 flex items-center gap-3 z-10">
          <img alt="Academic Commons Logo" className="w-8 h-8 object-contain" src="/assets/logo.svg" />
          <span className="text-[20px] font-extrabold text-[#0F172A] tracking-tight font-headline-md whitespace-nowrap">
            Academic Commons
          </span>
        </div>

        {/* Footer info */}
        <div className="absolute bottom-8 left-16 text-slate-500 text-[10px] font-semibold tracking-wider opacity-60 font-label-mono">
          HUST SECURE SSO v2.0
        </div>
      </section>

      {/* Right Column: Register Container */}
      <section className="w-full lg:w-1/2 h-full flex flex-col items-center justify-center p-6 bg-canvas-base overflow-y-auto">
        <div className="w-full max-w-[460px] bg-white border border-whisper-border rounded-2xl p-8 md:p-10 shadow-sm space-y-6 my-8">

          <div className="text-center space-y-1">
            <h1 className="font-headline-lg text-2xl font-black text-slate-950">Đăng ký</h1>
            <p className="text-xs text-slate-500 font-semibold">
              Tham gia hệ thống học liệu số cộng đồng HUST
            </p>
          </div>

          {stage === "pending-verification" ? (
            <div className="space-y-5">
              <div className="p-4 bg-green-50 border border-green-200 rounded-xl text-center space-y-2">
                <div className="text-3xl">📧</div>
                <p className="text-sm font-bold text-system-green">
                  Đăng ký thành công! Vui lòng kiểm tra email.
                </p>
                <p className="text-xs text-slate-600 font-medium leading-relaxed">
                  Chúng tôi đã gửi một liên kết xác minh tới <span className="font-bold">{formData.email}</span>.
                  Nhấn vào liên kết trong email để kích hoạt tài khoản, sau đó bạn có thể đăng nhập.
                </p>
                <p className="text-[11px] text-slate-400">
                  (Liên kết có hiệu lực 60 phút. Nếu không thấy, vui lòng kiểm tra mục Spam.)
                </p>
              </div>
              <button
                type="button"
                onClick={handleResend}
                disabled={resendStatus === "sending"}
                className="tactile-button text-xs py-2.5 w-full bg-slate-50 border border-whisper-border text-slate-700 font-bold hover:bg-slate-100 disabled:opacity-60"
              >
                {resendStatus === "sending"
                  ? "Đang gửi..."
                  : resendStatus === "sent"
                  ? "Đã gửi lại email xác minh"
                  : resendStatus === "failed"
                  ? "Gửi thất bại, vui lòng thử lại"
                  : "Gửi lại email xác minh"}
              </button>
              <div className="text-center pt-2">
                <p className="text-xs text-slate-500 font-semibold">
                  Đã xác minh?{" "}
                  <Link href="/login" className="text-hust-red font-bold hover:underline">
                    Đăng nhập ngay
                  </Link>
                </p>
              </div>
            </div>
          ) : (
            <>
              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs font-bold text-hust-red text-center">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="block text-xs font-bold text-slate-600 ml-1">
                    Họ và tên
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    placeholder="Ví dụ: Nguyễn Văn A"
                    className="w-full bg-canvas-base border border-whisper-border rounded-xl px-4 py-3 focus:ring-2 focus:ring-hust-red focus:border-hust-red font-body-sm font-semibold outline-none transition-all text-sm text-slate-800"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-bold text-slate-600 ml-1">
                    Email học tập
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="Ví dụ: sinhvien@sis.hust.edu.vn"
                    className="w-full bg-canvas-base border border-whisper-border rounded-xl px-4 py-3 focus:ring-2 focus:ring-hust-red focus:border-hust-red font-body-sm font-semibold outline-none transition-all text-sm text-slate-800"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-bold text-slate-600 ml-1">
                    Mật khẩu
                  </label>
                  <input
                    type="password"
                    required
                    minLength={8}
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    placeholder="Ít nhất 8 ký tự"
                    className="w-full bg-canvas-base border border-whisper-border rounded-xl px-4 py-3 focus:ring-2 focus:ring-hust-red focus:border-hust-red font-body-sm font-semibold outline-none transition-all text-sm text-slate-800"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-bold text-slate-600 ml-1">
                    Nhập lại mật khẩu
                  </label>
                  <input
                    type="password"
                    required
                    minLength={8}
                    value={formData.confirmPassword}
                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                    placeholder="Nhập lại m mật khẩu của bạn"
                    className="w-full bg-canvas-base border border-whisper-border rounded-xl px-4 py-3 focus:ring-2 focus:ring-hust-red focus:border-hust-red font-body-sm font-semibold outline-none transition-all text-sm text-slate-800"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="tactile-button tactile-button-primary w-full py-3.5 mt-2 rounded-xl text-base font-bold shadow-sm disabled:opacity-60"
                >
                  {loading ? "Đang xử lý..." : "Đăng ký tài khoản"}
                </button>
              </form>

              <div className="text-center pt-2">
                <p className="text-xs text-slate-500 font-semibold">
                  Đã có tài khoản?{" "}
                  <Link href="/login" className="text-hust-red font-bold hover:underline">
                    Đăng nhập ngay
                  </Link>
                </p>
              </div>
            </>
          )}

        </div>
      </section>
    </main>
  );
}