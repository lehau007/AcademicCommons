/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "../../lib/api";
import { useAsyncAction } from "../../lib/useAsyncAction";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [needsVerification, setNeedsVerification] = useState(false);
  const [resendStatus, setResendStatus] = useState<"idle" | "sending" | "sent" | "failed">("idle");

  const { pending: loading, run: handleLogin } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Vui lòng điền đầy đủ email và mật khẩu.");
      return;
    }

    setError("");
    setNeedsVerification(false);

    try {
      const data = await api.post<{ access_token: string; token_type: string }>("/auth/login", {
        email,
        password,
      });

      if (data && data.access_token) {
        localStorage.setItem("token", data.access_token);
        const user = await api.get<{ role: string }>("/auth/me");
        if (user.role === "reviewer") {
          router.push("/review");
        } else if (user.role === "admin") {
          router.push("/admin");
        } else {
          router.push("/dashboard");
        }
      } else {
        setError("Không nhận được token từ hệ thống.");
      }
    } catch (err: any) {
      if (err?.message === "email_not_verified" || err?.status === 403) {
        setNeedsVerification(true);
        setError("Tài khoản chưa được xác minh email. Vui lòng kiểm tra hộp thư (kể cả mục Spam) và nhấn nút bên dưới để gửi lại email xác minh.");
      } else {
        setError(err.message || "Email hoặc mật khẩu không đúng hoặc không tồn tại.");
      }
    }
  });

  const handleResend = async () => {
    if (!email) {
      setError("Vui lòng nhập email trước khi gửi lại email xác minh.");
      return;
    }
    setResendStatus("sending");
    try {
      await api.post("/auth/resend-verification", { email });
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

      {/* Right Column: Credential/Login Container */}
      <section className="w-full lg:w-1/2 h-full flex flex-col items-center justify-center p-6 bg-canvas-base overflow-y-auto">
        <div className="w-full max-w-[460px] bg-white border border-whisper-border rounded-2xl p-8 md:p-10 shadow-sm space-y-6">

          <div className="text-center space-y-1">
            <h1 className="font-headline-lg text-2xl font-black text-slate-950">Đăng nhập</h1>
            <p className="text-xs text-slate-500 font-semibold">
              Tiếp tục hành trình số hóa tài liệu học thuật cùng HUST
            </p>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs font-bold text-hust-red text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-slate-600 ml-1">
                Email / Tài khoản SIS
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Ví dụ: anh.nv226038@sis.hust.edu.vn"
                className="w-full bg-canvas-base border border-whisper-border rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-hust-red focus:border-hust-red font-body-sm font-semibold outline-none transition-all text-sm text-slate-800"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center px-1">
                <label className="text-xs font-bold text-slate-600">Mật khẩu</label>
              </div>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Nhập mật khẩu của bạn"
                  className="w-full bg-canvas-base border border-whisper-border rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-hust-red focus:border-hust-red font-body-sm font-semibold outline-none transition-all pr-12 text-sm text-slate-800"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700"
                >
                  <span className="material-symbols-outlined text-[20px]">
                    {showPassword ? "visibility_off" : "visibility"}
                  </span>
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="tactile-button tactile-button-primary w-full py-3.5 mt-2 rounded-xl text-base font-bold shadow-sm disabled:opacity-60"
            >
              {loading ? "Đang xử lý..." : "Đăng nhập"}
            </button>
          </form>

          {needsVerification && (
            <div className="space-y-2 p-3 bg-amber-50 border border-amber-200 rounded-xl">
              <p className="text-xs font-bold text-amber-800">
                Email của bạn chưa được xác minh. Nhấn vào nút dưới đây để gửi lại liên kết xác minh đến {email}.
              </p>
              <button
                type="button"
                onClick={handleResend}
                disabled={resendStatus === "sending"}
                className="tactile-button text-xs py-2 w-full bg-amber-100 border border-amber-300 text-amber-800 font-bold hover:bg-amber-200 disabled:opacity-60"
              >
                {resendStatus === "sending"
                  ? "Đang gửi..."
                  : resendStatus === "sent"
                  ? "Đã gửi lại email xác minh"
                  : resendStatus === "failed"
                  ? "Gửi thất bại, vui lòng thử lại"
                  : "Gửi lại email xác minh"}
              </button>
            </div>
          )}

          <div className="text-center pt-2">
            <p className="text-xs text-slate-500 font-semibold">
              Chưa có tài khoản?{" "}
              <Link href="/register" className="text-hust-red font-bold hover:underline">
                Đăng ký thành viên
              </Link>
            </p>
          </div>

        </div>
      </section>
    </main>
  );
}