/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
import AppShell from "../../components/app-shell";
import api from "../../lib/api";
import { useAsyncAction } from "../../lib/useAsyncAction";
import { Upload, CheckCircle2, AlertTriangle, ShieldCheck, Loader2 } from "lucide-react";

interface CourseRead {
  id: string;
  code: string;
  name: string;
  short_description: string | null;
}

interface CurrentUser {
  role: "admin" | "reviewer" | "student";
  full_name: string | null;
  email: string;
}

const MATERIAL_TYPES: { value: string; label: string }[] = [
  { value: "syllabus", label: "Đề Cương Học Phần" },
  { value: "textbook", label: "Giáo Trình" },
  { value: "lecture_slides", label: "Slide Bài Giảng" },
];

// Official upload is restricted to admin/reviewer, who get the privileged 50MB cap.
const MAX_FILE_MB = 50;
const MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024;
const ALLOWED_EXTENSIONS = [".pdf", ".pptx", ".png", ".jpg", ".jpeg"];

export default function OfficialUploadPage() {
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [courses, setCourses] = useState<CourseRead[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Form state
  const [courseCode, setCourseCode] = useState("");
  const [materialType, setMaterialType] = useState("lecture_slides");
  const [file, setFile] = useState<File | null>(null);
  const [consent, setConsent] = useState(false);
  const [errors, setErrors] = useState<{ course?: string; file?: string; consent?: string }>({});
  const [feedback, setFeedback] = useState<{ kind: "success" | "error"; message: string } | null>(null);

  useEffect(() => {
    const load = async () => {
      setIsLoading(true);
      try {
        const [user, myCourses] = await Promise.all([
          api.get<CurrentUser>("/auth/me"),
          api.get<CourseRead[]>("/review/my-courses"),
        ]);
        setCurrentUser(user);
        setCourses(myCourses);
        if (myCourses.length > 0) {
          setCourseCode(myCourses[0].code);
        }
      } catch (err: any) {
        setFeedback({ kind: "error", message: `Không thể tải danh sách học phần: ${err.message}` });
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, []);

  const { pending: isSubmitting, run: handleSubmit } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();
    setFeedback(null);

    const nextErrors: typeof errors = {};
    if (!courseCode) {
      nextErrors.course = "Vui lòng chọn học phần.";
    }
    if (!file) {
      nextErrors.file = "Vui lòng chọn tệp tin để tải lên.";
    } else {
      const ext = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
      if (!ALLOWED_EXTENSIONS.includes(ext)) {
        nextErrors.file = "Định dạng tệp không hợp lệ. Chỉ chấp nhận .pdf, .pptx, .png, .jpg, .jpeg.";
      } else if (file.size > MAX_FILE_BYTES) {
        nextErrors.file = `Tệp vượt quá dung lượng cho phép (tối đa ${MAX_FILE_MB}MB).`;
      }
    }
    if (!consent) {
      nextErrors.consent = "Bạn cần xác nhận quyền chia sẻ và đồng ý với chính sách trước khi tải lên.";
    }
    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }
    setErrors({});

    const formData = new FormData();
    formData.append("course_code", courseCode);
    formData.append("material_type", materialType);
    formData.append("file", file!); // validated non-null above

    try {
      await api.post<any>("/documents/official", formData);
      setFile(null);
      setConsent(false);
      setFeedback({
        kind: "success",
        message:
          "Tài liệu chính thức đã được tải lên thành công và đang được đưa vào hàng đợi xử lý tự động (OCR & Đánh giá chất lượng).",
      });
    } catch (err: any) {
      setFeedback({ kind: "error", message: `Lỗi tải lên tài liệu: ${err.message}` });
    }
  });

  const selectedCourse = courses.find((c) => c.code === courseCode);

  return (
    <AppShell>
      <div className="max-w-[720px] mx-auto py-8 px-4 space-y-6">
        <header className="space-y-2">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-hust-red" />
            <h1 className="font-display font-extrabold text-[22px] text-charcoal-ink">
              Tải lên tài liệu chính thức
            </h1>
          </div>
          <p className="text-[13px] text-muted-steel leading-relaxed">
            {currentUser?.role === "admin"
              ? "Với quyền Quản trị viên, bạn có thể tải tài liệu chính thức (Tier 1) cho bất kỳ học phần nào trong hệ thống."
              : "Với quyền Người phê duyệt, bạn chỉ có thể tải tài liệu chính thức cho những học phần đã được Quản trị viên phân công."}
          </p>
        </header>

        {isLoading ? (
          <div className="flex items-center gap-2 text-muted-steel text-sm py-12 justify-center">
            <Loader2 className="w-4 h-4 animate-spin" /> Đang tải danh sách học phần...
          </div>
        ) : courses.length === 0 ? (
          <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="font-bold text-[14px] text-charcoal-ink">Chưa có học phần nào được phân công</p>
              <p className="text-[12px] text-muted-steel leading-relaxed">
                Bạn hiện chưa được phân công phụ trách học phần nào. Vui lòng liên hệ Quản trị viên để
                được phân công trước khi tải lên tài liệu chính thức.
              </p>
            </div>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            noValidate
            className="bg-white border border-whisper-border rounded-2xl p-6 shadow-sm space-y-5"
          >
            {feedback && (
              <div
                className={`flex items-start gap-3 rounded-xl p-4 ${
                  feedback.kind === "success"
                    ? "bg-emerald-50 border border-emerald-200"
                    : "bg-red-50 border border-red-200"
                }`}
              >
                {feedback.kind === "success" ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
                )}
                <p className="text-[12px] text-charcoal-ink leading-relaxed">{feedback.message}</p>
              </div>
            )}

            <div className="space-y-1">
              <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">
                Học phần
              </label>
              <select
                className={`w-full bg-[#F8FAFC] border rounded-xl px-4 py-2.5 text-body-md focus:ring-2 focus:ring-hust-red focus:border-hust-red outline-none ${
                  errors.course ? "border-system-red" : "border-whisper-border"
                }`}
                value={courseCode}
                onChange={(e) => {
                  setCourseCode(e.target.value);
                  if (errors.course) setErrors((p) => ({ ...p, course: undefined }));
                }}
              >
                {courses.map((c) => (
                  <option key={c.id} value={c.code}>
                    {c.code} — {c.name}
                  </option>
                ))}
              </select>
              {selectedCourse?.short_description && (
                <p className="text-[11px] text-muted-steel mt-1">{selectedCourse.short_description}</p>
              )}
              {errors.course && (
                <span className="block text-[11px] text-system-red font-semibold mt-1">{errors.course}</span>
              )}
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">
                Phân loại tài liệu
              </label>
              <select
                className="w-full bg-[#F8FAFC] border border-whisper-border rounded-xl px-4 py-2.5 text-body-md"
                value={materialType}
                onChange={(e) => setMaterialType(e.target.value)}
              >
                {MATERIAL_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider font-display">
                Tệp tin (.pdf, .pptx, .png)
              </label>
              <div className="border-2 border-dashed border-whisper-border rounded-xl p-6 text-center hover:bg-canvas-base transition-colors cursor-pointer relative">
                <input
                  type="file"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                  accept=".pdf,.pptx,.png,.jpg,.jpeg"
                  onChange={(e) => {
                    setFile(e.target.files?.[0] || null);
                    if (errors.file) setErrors((p) => ({ ...p, file: undefined }));
                  }}
                />
                <Upload className="w-8 h-8 text-muted-steel mx-auto mb-2" />
                <span className="block text-xs font-bold text-charcoal-ink">
                  {file ? file.name : "Kéo thả hoặc nhấp để chọn tệp"}
                </span>
                <span className="block text-[10px] text-muted-steel mt-0.5">Dung lượng tối đa {MAX_FILE_MB}MB</span>
              </div>
              {errors.file && (
                <span className="block text-[11px] text-system-red font-semibold mt-1">{errors.file}</span>
              )}
            </div>

            <div className="space-y-1">
              <label className="flex items-start gap-2.5 cursor-pointer">
                <input
                  type="checkbox"
                  className="mt-0.5 accent-hust-red rounded shrink-0"
                  checked={consent}
                  onChange={(e) => {
                    setConsent(e.target.checked);
                    if (errors.consent) setErrors((p) => ({ ...p, consent: undefined }));
                  }}
                />
                <span className="text-[12px] text-charcoal-ink leading-relaxed">
                  Tôi xác nhận tài liệu này là tài liệu chính thức hợp lệ của học phần, tôi có quyền chia
                  sẻ và đồng ý với chính sách sử dụng học thuật nội bộ.
                </span>
              </label>
              {errors.consent && (
                <span className="block text-[11px] text-system-red font-semibold mt-1">{errors.consent}</span>
              )}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="tactile-button tactile-button-primary w-full py-2.5 flex items-center justify-center gap-2 disabled:opacity-60"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" /> Đang tải lên...
                </>
              ) : (
                "Tải lên tài liệu chính thức"
              )}
            </button>
          </form>
        )}
      </div>
    </AppShell>
  );
}
