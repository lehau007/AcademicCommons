"use client";

import React, { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import api from "../../lib/api";

type State = "verifying" | "success" | "invalid" | "missing";

function VerifyEmailInner() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [state, setState] = useState<State>(token ? "verifying" : "missing");

  useEffect(() => {
    if (!token) {
      // Initial state already set to "missing" via useState initializer.
      return;
    }

    let cancelled = false;
    (async () => {
      try {
        await api.post("/auth/verify-email", null, { params: { token } });
        if (!cancelled) setState("success");
      } catch {
        if (!cancelled) setState("invalid");
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [token]);

  return (
    <main className="flex h-screen w-full items-center justify-center font-body-md text-on-surface antialiased bg-canvas-base">
      <div className="w-full max-w-[460px] bg-white border border-whisper-border rounded-2xl p-8 md:p-10 shadow-sm space-y-5 mx-6 text-center">

        {state === "verifying" && (
          <>
            <div className="text-3xl">⏳</div>
            <h1 className="font-headline-lg text-2xl font-black text-slate-950">Đang xác minh</h1>
            <p className="text-sm text-slate-500 font-medium">
              Vui lòng đợi trong giây lát...
            </p>
          </>
        )}

        {state === "success" && (
          <>
            <div className="text-3xl">✅</div>
            <h1 className="font-headline-lg text-2xl font-black text-slate-950">Xác minh thành công</h1>
            <p className="text-sm text-slate-600 font-medium">
              Email của bạn đã được xác minh. Bạn có thể đăng nhập và sử dụng hệ thống.
            </p>
            <Link href="/login" className="tactile-button tactile-button-primary inline-block px-6 py-3 rounded-xl text-sm font-bold">
              Đăng nhập ngay
            </Link>
          </>
        )}

        {state === "invalid" && (
          <>
            <div className="text-3xl">⚠️</div>
            <h1 className="font-headline-lg text-2xl font-black text-slate-950">Liên kết không hợp lệ</h1>
            <p className="text-sm text-slate-600 font-medium">
              Liên kết xác minh đã hết hạn hoặc đã được sử dụng. Vui lòng đăng nhập để gửi lại email xác minh.
            </p>
            <Link href="/login" className="tactile-button inline-block px-6 py-3 rounded-xl text-sm font-bold bg-slate-50 border border-whisper-border text-slate-700 hover:bg-slate-100">
              Về trang đăng nhập
            </Link>
          </>
        )}

        {state === "missing" && (
          <>
            <div className="text-3xl">⚠️</div>
            <h1 className="font-headline-lg text-2xl font-black text-slate-950">Thiếu token</h1>
            <p className="text-sm text-slate-600 font-medium">
              Không tìm thấy token xác minh trong liên kết. Vui lòng mở liên kết đầy đủ từ email của bạn.
            </p>
            <Link href="/login" className="tactile-button inline-block px-6 py-3 rounded-xl text-sm font-bold bg-slate-50 border border-whisper-border text-slate-700 hover:bg-slate-100">
              Về trang đăng nhập
            </Link>
          </>
        )}
      </div>
    </main>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<div className="flex h-screen w-full items-center justify-center text-sm text-slate-500">Đang tải...</div>}>
      <VerifyEmailInner />
    </Suspense>
  );
}