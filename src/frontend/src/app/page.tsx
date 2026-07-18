"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "../lib/api";

export default function LandingPage() {
  const router = useRouter();
  const [currentSlide, setCurrentSlide] = useState(0);
  // While a logged-in user's session is being verified we render a loader instead
  // of the landing page, so the "Đăng nhập" buttons aren't clickable during the
  // (possibly slow) /auth/me round-trip that ends in a redirect.
  const [checkingAuth, setCheckingAuth] = useState(false);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
    if (!token) return;
    void (async () => {
      setCheckingAuth(true);
      try {
        const user = await api.get<{ role: string }>("/auth/me");
        if (user.role === "reviewer") router.replace("/review");
        else if (user.role === "admin") router.replace("/admin");
        else router.replace("/dashboard");
      } catch {
        localStorage.removeItem("token");
        setCheckingAuth(false);
      }
    })();
  }, [router]);

  const slides = [
    {
      src: "/assets/document_digitization.jpg",
      alt: "Số hóa tài liệu học tập",
      title: "Số hóa học liệu Bách Khoa",
      desc: "Chụp ảnh slide, giáo trình hoặc vở ghi chép, hệ thống tự động nhận diện công thức LaTeX và sơ đồ hóa.",
    },
    {
      src: "/assets/anime_tutor.jpg",
      alt: "AI Virtual Tutor",
      title: "Hỏi đáp cùng AI Virtual Tutor",
      desc: "Trò chuyện trực tiếp với AI thông minh được tối ưu hóa theo tài liệu nội bộ, trích dẫn chính xác nguồn gốc.",
    },
    {
      src: "/assets/anime_mindmap.jpg",
      alt: "Sơ đồ khái niệm",
      title: "Tạo sơ đồ khái niệm tự động",
      desc: "Tự động trích xuất các chủ đề cốt lõi và liên kết chúng dưới dạng bản đồ tư duy trực quan sống động.",
    },
    {
      src: "/assets/anime_quiz.jpg",
      alt: "Luyện tập đề thi thử",
      title: "Luyện tập đề thi thử",
      desc: "Sinh viên mỉm cười hài lòng khi hoàn thành xuất sắc bài thi trắc nghiệm thử (MCQ) trên điện thoại.",
    },
  ];

  // Rotate hero background images
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 8000);
    return () => clearInterval(timer);
  }, [slides.length]);

  if (checkingAuth) {
    return (
      <div className="min-h-screen bg-canvas-base flex flex-col items-center justify-center gap-4 select-none">
        <div className="h-10 w-10 rounded-full border-[3px] border-whisper-border border-t-hust-red animate-spin" />
        <p className="font-body-md text-sm font-semibold text-muted-steel">Đang kiểm tra đăng nhập…</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-canvas-base font-body-md text-on-surface antialiased select-none relative">

      {/* Top Navbar */}
      <header className="fixed top-4 left-1/2 -translate-x-1/2 w-[calc(100%-2rem)] max-w-7xl z-50 bg-white/95 backdrop-blur-md border border-whisper-border rounded-2xl shadow-sm px-8 py-3.5 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <img alt="Academic Commons Logo" className="w-8 h-8 object-contain" src="/assets/logo.svg" />
          <span className="font-headline-md text-xl font-extrabold text-hust-red tracking-tight">
            Academic Commons
          </span>
        </div>
        <nav className="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-600">
          <a href="#hero" className="hover:text-hust-red transition-colors">Giới thiệu</a>
          <a href="#metrics" className="hover:text-hust-red transition-colors">Thống kê</a>
          <a href="#features" className="hover:text-hust-red transition-colors">Tính năng</a>
        </nav>
        <Link href="/login" className="tactile-button text-sm py-2 px-5 hover:bg-canvas-base border border-whisper-border text-slate-800">
          Đăng nhập
        </Link>
      </header>

      {/* Main Container */}
      <main className="pt-28 pb-16 px-4 md:px-8 max-w-7xl mx-auto space-y-16">
        
        {/* Hero Section */}
        <section id="hero" className="scroll-mt-28">
          <div className="bg-white border-1.5 border-whisper-border rounded-[2.5rem] p-8 md:p-12 lg:p-14 flex flex-col lg:flex-row gap-8 lg:gap-12 items-stretch min-h-[500px] shadow-sm">
            
            {/* Left Content Column */}
            <div className="flex-1 flex flex-col justify-center items-start text-left space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-red-50 text-hust-red border border-red-100 font-bold text-xs uppercase tracking-wider">
                <span className="material-symbols-outlined text-[16px] font-bold">verified_user</span>
                HUST SOICT
              </div>

              <h1 className="font-headline-xl text-4xl md:text-5xl lg:text-[3.25rem] font-black text-slate-900 tracking-tight leading-none">
                Số hóa Tri thức <br />
                <span className="text-hust-red">Học thuật Cộng đồng</span>
              </h1>

              <p className="font-body-lg text-base md:text-lg text-slate-600 max-w-xl leading-relaxed">
                Hệ thống hỗ trợ sinh viên Bách Khoa đóng góp, chuẩn hóa và khai thác học liệu số tích hợp AI Tutor, sơ đồ khái niệm tự động và ngân hàng câu hỏi trắc nghiệm.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto pt-2">
                <Link href="/login" className="tactile-button tactile-button-primary text-center px-8 py-4 text-base shadow-sm w-full sm:w-auto">
                  Khám phá ngay
                </Link>
                <a href="#features" className="tactile-button text-center px-8 py-4 text-base hover:bg-canvas-base border border-whisper-border text-slate-800 w-full sm:w-auto">
                  Tìm hiểu thêm
                </a>
              </div>
            </div>

            {/* Right Image Column */}
            <div className="flex-1 min-h-[400px] bg-canvas-base border border-whisper-border rounded-[2rem] relative overflow-hidden">
              <img
                src={slides[currentSlide].src}
                alt={slides[currentSlide].alt}
                className="absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 opacity-90"
              />
              
              {/* Overlay Text Banner */}
              <div className="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-md rounded-2xl shadow-md p-5 border border-whisper-border z-10 space-y-1">
                <h4 className="text-xs font-bold text-hust-red uppercase tracking-wider font-label-mono">
                  {slides[currentSlide].title}
                </h4>
                <p className="text-[11px] text-slate-600 leading-relaxed font-semibold">
                  {slides[currentSlide].desc}
                </p>
              </div>
            </div>

          </div>
        </section>

        {/* Metrics Section */}
        <section id="metrics" className="scroll-mt-28 bg-white border-1.5 border-whisper-border rounded-[2rem] p-8 md:p-12">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 md:gap-12">
            <div className="space-y-1">
              <span className="font-label-mono text-3xl md:text-4xl font-extrabold text-hust-red block">
                15,420+
              </span>
              <span className="text-xs md:text-sm text-slate-500 font-bold">
                Tài liệu học tập số hóa
              </span>
            </div>
            <div className="space-y-1 border-l border-whisper-border pl-6 md:pl-10">
              <span className="font-label-mono text-3xl md:text-4xl font-extrabold text-hust-red block">
                2,500+
              </span>
              <span className="text-xs md:text-sm text-slate-500 font-bold">
                Sơ đồ khái niệm được tạo
              </span>
            </div>
            <div className="space-y-1 border-l border-whisper-border pl-6 md:pl-10">
              <span className="font-label-mono text-3xl md:text-4xl font-extrabold text-hust-red block">
                48h
              </span>
              <span className="text-xs md:text-sm text-slate-500 font-bold">
                SLA kiểm duyệt chất lượng
              </span>
            </div>
            <div className="space-y-1 border-l border-whisper-border pl-6 md:pl-10">
              <span className="font-label-mono text-3xl md:text-4xl font-extrabold text-hust-red block">
                98.5%
              </span>
              <span className="text-xs md:text-sm text-slate-500 font-bold">
                Độ chính xác OCR LaTeX
              </span>
            </div>
          </div>
        </section>

        {/* Features Bento Grid */}
        <section id="features" className="scroll-mt-28 space-y-8">
          <div>
            <h2 className="font-headline-lg text-2xl md:text-3xl font-extrabold text-slate-950">
              Học tập thông minh tích hợp AI
            </h2>
            <p className="font-body-sm text-slate-500 font-semibold max-w-xl">
              Hệ thống cung cấp chuỗi công cụ bổ trợ học tập kỹ thuật toàn diện, thúc đẩy tự học tối ưu.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
            
            {/* Bento Card 1: AI Tutor */}
            <div className="md:col-span-8 bg-white border-1.5 border-whisper-border rounded-2xl p-8 flex flex-col justify-between relative overflow-hidden min-h-[300px]">
              <div className="space-y-4 relative z-10">
                <div className="w-12 h-12 rounded-xl bg-hust-red/10 flex items-center justify-center text-hust-red">
                  <span className="material-symbols-outlined text-[28px] font-light">smart_toy</span>
                </div>
                <h3 className="font-headline-md text-xl font-bold text-slate-900">AI Virtual Tutor</h3>
                <p className="font-body-sm text-slate-600 max-w-lg leading-relaxed font-semibold">
                  Mô hình AI tương tác trực tiếp trên học liệu chính thống được tải lên, hỗ trợ tóm tắt bài giảng phức tạp, dịch thuật thuật ngữ và hiển thị công thức toán học định dạng LaTeX.
                </p>
              </div>
              <div className="flex gap-2 mt-6 relative z-10">
                <span className="px-2.5 py-1 bg-canvas-base border border-whisper-border rounded-lg text-[10px] font-label-mono font-bold text-slate-600">
                  RAG-BASED CHAT
                </span>
                <span className="px-2.5 py-1 bg-canvas-base border border-whisper-border rounded-lg text-[10px] font-label-mono font-bold text-slate-600">
                  LATEX MATH ENGINE
                </span>
              </div>
            </div>

            {/* Bento Card 2: Concept Mindmap */}
            <div className="md:col-span-4 bg-hust-red text-white rounded-2xl p-8 flex flex-col justify-between min-h-[300px]">
              <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center">
                <span className="material-symbols-outlined text-[28px] font-light">account_tree</span>
              </div>
              <div className="space-y-2">
                <h3 className="font-headline-md text-xl font-bold">Sơ đồ khái niệm</h3>
                <p className="font-body-sm text-red-50 leading-relaxed font-semibold">
                  Tự động phân tách cấu trúc tri thức môn học dưới dạng Mindmap sinh động, thể hiện mối quan hệ liên đới giữa các khái niệm.
                </p>
              </div>
            </div>

            {/* Bento Card 3: Mock Quiz */}
            <div className="md:col-span-5 bg-white border-1.5 border-whisper-border rounded-2xl p-8 flex flex-col justify-between min-h-[300px]">
              <div className="space-y-4">
                <div className="w-12 h-12 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-600">
                  <span className="material-symbols-outlined text-[28px] font-light">quiz</span>
                </div>
                <h3 className="font-headline-md text-xl font-bold text-slate-900">Thi thử trắc nghiệm</h3>
                <p className="font-body-sm text-slate-600 leading-relaxed font-semibold">
                  Hệ thống tự động biên soạn ngân hàng câu hỏi trắc nghiệm kiểm tra kiến thức đa dạng dựa trên tài liệu lớp học.
                </p>
              </div>
              <div className="mt-6">
                <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-amber-500 h-full w-[85%]"></div>
                </div>
                <span className="font-label-mono text-[9px] mt-2 block text-slate-500 font-bold">
                  85% TỶ LỆ HOÀN THÀNH TIÊU CHUẨN
                </span>
              </div>
            </div>

            {/* Bento Card 4: Review Workflow */}
            <div className="md:col-span-7 bg-white border-1.5 border-whisper-border rounded-2xl p-8 flex flex-col justify-between min-h-[300px]">
              <div className="space-y-4">
                <div className="w-12 h-12 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-600">
                  <span className="material-symbols-outlined text-[28px] font-light">verified_user</span>
                </div>
                <h3 className="font-headline-md text-xl font-bold text-slate-900">Kiểm định chất lượng (HITL)</h3>
                <p className="font-body-sm text-slate-600 leading-relaxed font-semibold">
                  Mô hình cộng tác đa tầng: AI trích xuất sơ bộ, đội ngũ sinh viên xuất sắc thẩm định và ban cố vấn chuyên môn (Giáo viên HUST) phê duyệt đảm bảo chất lượng học thuật cao nhất.
                </p>
              </div>
              <div className="flex items-center -space-x-2 mt-6">
                <div className="w-8 h-8 rounded-full bg-slate-200 border border-white flex items-center justify-center text-[10px] font-bold text-slate-800">
                  LH
                </div>
                <div className="w-8 h-8 rounded-full bg-slate-300 border border-white flex items-center justify-center text-[10px] font-bold text-slate-800">
                  TD
                </div>
                <div className="w-8 h-8 rounded-full bg-slate-400 border border-white flex items-center justify-center text-[10px] font-bold text-slate-800">
                  PT
                </div>
                <span className="text-xs font-semibold text-slate-500 ml-4">
                  +12 Reviewers chuyên môn trực tuyến
                </span>
              </div>
            </div>

          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full bg-white border-t-1.5 border-whisper-border py-12 px-8">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start gap-8 border-b border-whisper-border pb-8 mb-8">
          <div className="space-y-4 max-w-sm">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-hust-red flex items-center justify-center text-white font-extrabold text-sm tracking-tighter">
                AC
              </div>
              <span className="font-headline-md text-lg font-bold text-slate-950">Academic Commons</span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed font-semibold">
              Cơ sở hạ tầng lưu trữ và số hóa tri thức học tập Bách Khoa Hà Nội. Phát triển bởi SOICT.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-12 text-sm font-semibold text-slate-700">
            <div className="space-y-3">
              <h4 className="font-bold text-slate-950">Sản phẩm</h4>
              <ul className="space-y-2 text-xs text-slate-500 font-semibold">
                <li><a href="#" className="hover:underline">OCR & LaTeX</a></li>
                <li><a href="#" className="hover:underline">AI Virtual Tutor</a></li>
                <li><a href="#" className="hover:underline">Concept Mindmaps</a></li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-bold text-slate-950">Liên kết</h4>
              <ul className="space-y-2 text-xs text-slate-500 font-semibold">
                <li><a href="#" className="hover:underline">SOICT HUST</a></li>
                <li><a href="#" className="hover:underline">SIS Student Portal</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto text-center md:text-left text-xs text-slate-400 font-semibold">
          © 2026 Academic Commons. Mọi quyền được bảo lưu.
        </div>
      </footer>
    </div>
  );
}
