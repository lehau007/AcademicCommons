/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import AppShell from "../../components/app-shell";
import api from "../../lib/api";

interface SearchableCourse {
  course_code: string;
  name: string;
  description: string;
  topic_summary: string;
}

export default function GlobalSearchPage() {
  const [query, setQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState<"ALL" | "IT" | "EE" | "MATH">("ALL");
  const [courses, setCourses] = useState<SearchableCourse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const data = await api.get<any[]>("/courses");
        // Map backend 'code' to 'course_code' (same convention as dashboard/page.tsx).
        setCourses(
          (data || []).map((c: any) => ({
            course_code: c.code,
            name: c.name,
            description: c.description || "",
            topic_summary: c.topic_summary || "",
          }))
        );
      } catch {
        setCourses([]);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  // Parse topic_summary into keyword chips (only when it's a ';'-separated list of
  // short keywords). Returns null when it's prose that just duplicates the
  // description — including the case where long sentences are joined by ';' — so we
  // hide the redundant section instead of echoing the description as fake "chips".
  const getTopicChips = (topicSummary: string): string[] | null => {
    if (!topicSummary.includes(";")) return null;
    const chips = topicSummary
      .split(";")
      .map((t) => t.trim())
      // Keep only genuine keyword-length fragments, not full sentences.
      .filter((t) => t.length > 0 && t.length <= 60);
    return chips.length > 0 ? chips : null;
  };

  // Smarter search: tokenize query on whitespace and match case-insensitively.
  // A course matches when ANY token is found in the combined haystack (so natural
  // multi-word queries like "database SQL" still surface relevant courses), then
  // results are ranked by how many tokens they match so the best ones come first.
  const tokens = query
    .toLowerCase()
    .split(/\s+/)
    .map((t) => t.trim())
    .filter(Boolean);

  const passesFilter = (course: SearchableCourse) => {
    if (activeFilter === "ALL") return true;
    if (activeFilter === "IT") return course.course_code.startsWith("IT");
    if (activeFilter === "MATH") return course.course_code.includes("3020") || course.course_code.includes("4110");
    if (activeFilter === "EE") return course.course_code.includes("3420") || course.course_code.includes("3280");
    return true;
  };

  const scored = courses
    .map((course) => {
      const haystack = `${course.course_code} ${course.name} ${course.description} ${course.topic_summary}`.toLowerCase();
      const score = tokens.filter((token) => haystack.includes(token)).length;
      return { course, score };
    })
    .filter(({ course }) => passesFilter(course));

  // Only surface the most relevant tier: courses matching the highest number of
  // query tokens. This keeps natural multi-word queries useful ("database SQL" →
  // the Database course) without flooding results when a common token ("c",
  // "programming") happens to appear in nearly every course.
  const maxScore = Math.max(0, ...scored.map(({ score }) => score));
  const matchedCourses = scored
    // Empty query (no tokens) shows everything; otherwise show only the top tier.
    .filter(({ score }) => (tokens.length === 0 ? true : score > 0 && score === maxScore))
    .map(({ course }) => course);

  return (
    <AppShell>
      <div className="space-y-6">
        
        {/* Search Input Card */}
        <div className="bg-white border border-whisper-border rounded-2xl p-6 md:p-8 shadow-sm space-y-4">
          <div className="space-y-1">
            <h1 className="text-xl font-black text-slate-900">Tìm kiếm toàn cục</h1>
            <p className="text-xs text-muted-steel font-semibold">
              Tra cứu nhanh học liệu môn học, công thức và chủ đề nghiên cứu của Bách Khoa
            </p>
          </div>

          <div className="relative">
            <input
              type="text"
              placeholder="Nhập mã môn học, tên môn học hoặc từ khóa (ví dụ: Quy hoạch động, IT3210, RAG)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-canvas-base border border-whisper-border rounded-xl pl-12 pr-4 py-4 text-sm font-semibold outline-none focus:ring-2 focus:ring-hust-red transition-all"
            />
            <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-[22px]">
              search
            </span>
          </div>

          {/* Filter Chips */}
          <div className="flex flex-wrap gap-2 pt-2">
            {[
              { id: "ALL", label: "Tất cả học phần" },
              { id: "IT", label: "Công nghệ thông tin (IT)" },
              { id: "MATH", label: "Toán học & Tính toán" },
              { id: "EE", label: "Điện & Điện tử" },
            ].map((filter) => (
              <button
                key={filter.id}
                onClick={() => setActiveFilter(filter.id as any)}
                className={`px-4 py-1.5 rounded-full text-xs font-bold transition-all border ${
                  activeFilter === filter.id
                    ? "bg-hust-red border-hust-red text-white"
                    : "bg-white border-whisper-border text-slate-600 hover:bg-canvas-base"
                }`}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>

        {/* Search Results Display */}
        <div className="space-y-4">
          <h2 className="text-xs font-bold text-muted-steel uppercase tracking-wider pl-1">
            Kết quả tra cứu ({matchedCourses.length} học phần phù hợp)
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {matchedCourses.map((course) => (
              <div
                key={course.course_code}
                className="bg-white border border-whisper-border hover:border-hust-red/40 rounded-2xl p-6 shadow-xs flex flex-col justify-between transition-all group"
              >
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="font-label-mono text-[10px] font-bold text-hust-red bg-red-50 border border-red-100 px-2 py-0.5 rounded-md">
                      {course.course_code}
                    </span>
                    <span className="text-[10px] text-muted-steel font-bold">SOICT</span>
                  </div>
                  
                  <h3 className="font-headline-md text-sm font-extrabold text-slate-900 group-hover:text-hust-red transition-colors line-clamp-1">
                    {course.name}
                  </h3>
                  
                  <p className="text-[11px] text-slate-500 font-semibold line-clamp-3 leading-relaxed">
                    {course.description}
                  </p>

                  {(() => {
                    const chips = getTopicChips(course.topic_summary);
                    if (!chips || chips.length === 0) return null;
                    return (
                      <div className="space-y-1.5">
                        <h4 className="text-[10px] font-bold text-slate-700 uppercase tracking-wide">
                          Chủ đề chính:
                        </h4>
                        <div className="flex flex-wrap gap-1.5">
                          {chips.slice(0, 6).map((chip, idx) => (
                            <span
                              key={idx}
                              className="text-[10px] font-semibold text-slate-600 bg-canvas-base border border-whisper-border px-2 py-0.5 rounded-full"
                            >
                              {chip}
                            </span>
                          ))}
                        </div>
                      </div>
                    );
                  })()}
                </div>

                <div className="mt-6 pt-4 border-t border-slate-50 flex justify-between items-center">
                  <span className="text-[10px] text-slate-400 font-semibold italic">
                    AI Indexing hoàn tất
                  </span>
                  <Link
                    href={`/courses/${course.course_code}`}
                    className="tactile-button text-[11px] py-1.5 px-4 bg-white border border-whisper-border hover:bg-canvas-base text-slate-800"
                  >
                    Vào không gian
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {!loading && matchedCourses.length === 0 && (
            <div className="bg-white border border-whisper-border rounded-2xl p-12 text-center space-y-2">
              <p className="text-slate-500 font-semibold">
                Không tìm thấy học phần nào khớp với từ khóa tìm kiếm của bạn.
              </p>
              <p className="text-xs text-muted-steel font-semibold">
                Gợi ý: thử từ khóa ngắn hơn hoặc kiểm tra chính tả. Ví dụ: &apos;cơ sở dữ liệu&apos;, &apos;lập trình&apos;, &apos;IT3292&apos;.
              </p>
              {activeFilter !== "ALL" && (
                <p className="text-xs text-muted-steel font-semibold">
                  Hoặc thử bỏ bộ lọc học phần đang áp dụng để mở rộng kết quả.
                </p>
              )}
            </div>
          )}
        </div>

      </div>
    </AppShell>
  );
}
