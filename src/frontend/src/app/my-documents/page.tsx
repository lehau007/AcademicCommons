"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { 
  Search, 
  Filter, 
  Calendar, 
  FileText, 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  Loader2, 
  AlertCircle, 
  XCircle, 
  RefreshCw, 
  UploadCloud,
  BookOpen
} from "lucide-react";
import AppShell from "@/components/app-shell";
import api from "@/lib/api";

interface UploadedDocument {
  id: string;
  course_id: string;
  course_code: string | null;
  uploader_id: string;
  document_tier: string;
  material_type: string | null;
  contribution_type: string | null;
  topic_tags: string[];
  status: string;
  version: number;
  original_filename: string;
  display_name?: string | null;
  file_format: string;
  sla_breached: boolean;
  sla_deadline: string | null;
  uploaded_at: string;
  updated_at: string;
  reviewer_note: string | null;
  failure_hint?: string | null;
}

interface StepState {
  label: string;
  description: string;
  status: "done" | "in_progress" | "pending" | "failed";
}

function getPipelineSteps(status: string): StepState[] {
  const steps: StepState[] = [
    { label: "Bước 1: Tải lên", description: "Tải lên tài liệu thành công", status: "pending" },
    { label: "Bước 2: Phân tích OCR", description: "Trích xuất văn bản từ tài liệu", status: "pending" },
    { label: "Bước 3: Đánh giá chất lượng", description: "Chạy tác vụ AI đánh giá nội dung", status: "pending" },
    { label: "Bước 4: Kiểm duyệt học thuật", description: "Ban kiểm duyệt phê duyệt tài liệu", status: "pending" },
    { label: "Bước 5: Lập chỉ mục & Hoàn thành", description: "Lập chỉ mục vào DB Vector và cộng điểm đóng góp", status: "pending" },
  ];

  const s = status.toUpperCase();

  if (s === "FAILED") {
    steps[0].status = "done";
    steps[1].status = "failed";
    return steps;
  }

  if (s === "REJECTED") {
    steps[0].status = "done";
    steps[1].status = "done";
    steps[2].status = "done";
    steps[3].status = "failed";
    return steps;
  }

  // Normal pipeline state
  steps[0].status = "done";

  if (s === "UPLOADED") {
    steps[1].status = "in_progress";
  } else if (s === "PARSING") {
    steps[1].status = "in_progress";
  } else if (s === "EVALUATING") {
    steps[1].status = "done";
    steps[2].status = "in_progress";
  } else if (s === "NEEDS_REVIEW") {
    steps[1].status = "done";
    steps[2].status = "done";
    steps[3].status = "in_progress";
  } else if (s === "APPROVED") {
    steps[1].status = "done";
    steps[2].status = "done";
    steps[3].status = "done";
    steps[4].status = "in_progress";
  } else if (s === "INDEXING") {
    steps[1].status = "done";
    steps[2].status = "done";
    steps[3].status = "done";
    steps[4].status = "in_progress";
  } else if (s === "INDEXED") {
    steps[1].status = "done";
    steps[2].status = "done";
    steps[3].status = "done";
    steps[4].status = "done";
  }

  return steps;
}

export default function MyDocumentsPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  
  // Search & Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [courseFilter, setCourseFilter] = useState("ALL");

  async function loadDocuments() {
    setLoading(true);
    setError("");
    try {
      const data = await api.get<any>("/documents");
      setDocuments(Array.isArray(data) ? data : (data.items || []));
    } catch (err: any) {
      console.error("Failed to load my documents:", err);
      setError(err.message || "Không thể kết nối tới máy chủ.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const checkUserAndLoad = async () => {
      try {
        const loggedInUser = await api.get<any>("/auth/me");
        setUser(loggedInUser);
        if (!loggedInUser || loggedInUser.role !== "student") {
          router.push("/dashboard");
          return;
        }
        await loadDocuments();
      } catch (err: any) {
        console.error("Failed to authenticate user:", err);
        router.push("/login");
      }
    };
    checkUserAndLoad();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router]);

  const handleToggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const getStatusBadge = (status: string) => {
    const s = status.toUpperCase();
    switch (s) {
      case "INDEXED":
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-green-50 px-2 py-0.5 text-xs font-bold text-system-green border border-green-100">
            <CheckCircle2 className="h-3.5 w-3.5" /> Đã Hoàn Thành
          </span>
        );
      case "NEEDS_REVIEW":
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-amber-50 px-2 py-0.5 text-xs font-bold text-pear-yellow border border-amber-100">
            <AlertCircle className="h-3.5 w-3.5" /> Chờ Kiểm Duyệt
          </span>
        );
      case "REJECTED":
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-red-50 px-2 py-0.5 text-xs font-bold text-system-red border border-red-100">
            <XCircle className="h-3.5 w-3.5" /> Bị Từ Chối
          </span>
        );
      case "FAILED":
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-red-50 px-2 py-0.5 text-xs font-bold text-system-red border border-red-100">
            <AlertCircle className="h-3.5 w-3.5" /> Lỗi Hệ Thống
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-blue-50 px-2 py-0.5 text-xs font-bold text-blue-600 border border-blue-100 animate-pulse">
            <Loader2 className="h-3.5 w-3.5 animate-spin" /> Đang Xử Lý ({status})
          </span>
        );
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  // Extract unique courses from documents list for filter dropdown
  const uniqueCourses = Array.from(new Set(documents.map(d => d.course_code).filter(Boolean)));

  const filteredDocs = documents.filter((doc) => {
    const filenameMatch = (doc.display_name || doc.original_filename).toLowerCase().includes(searchQuery.toLowerCase());
    const courseCodeMatch = doc.course_code && doc.course_code.toLowerCase().includes(searchQuery.toLowerCase());
    const queryMatch = filenameMatch || courseCodeMatch;

    const statusMatch = statusFilter === "ALL" || doc.status.toUpperCase() === statusFilter;
    const courseMatch = courseFilter === "ALL" || doc.course_code === courseFilter;

    return queryMatch && statusMatch && courseMatch;
  });

  return (
    <AppShell>
      <div className="space-y-6">
        
        {/* Header section with HUST Mechanical details */}
        <div className="relative rounded-2xl border border-whisper-border bg-white p-6 shadow-sm overflow-hidden">
          <div className="absolute top-0 right-0 h-24 w-24 translate-x-8 -translate-y-8 rounded-full bg-hust-red/5 blur-2xl" />
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <h1 className="font-headline-lg text-2xl font-black text-slate-900">
                Tài Liệu Của Tôi
              </h1>
              <p className="mt-1 font-body-sm text-xs text-muted-steel font-semibold max-w-2xl">
                Theo dõi tiến trình xử lý, phân tích OCR, kiểm duyệt học thuật và lập chỉ mục của các tài liệu học tập bạn đã tải lên.
              </p>
            </div>
            <button
              onClick={loadDocuments}
              className="tactile-button text-[12px] py-2 px-4 bg-white hover:bg-canvas-base border border-whisper-border text-slate-800 self-start md:self-auto"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`} /> Tải lại danh sách
            </button>
          </div>
        </div>

        {/* Filter controls panel */}
        <div className="flex flex-col gap-4 md:flex-row md:items-center justify-between bg-white border border-whisper-border rounded-2xl p-4 shadow-sm">
          {/* Search bar */}
          <div className="relative flex-1 max-w-md">
            <span className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-4 w-4 text-muted-steel" />
            </span>
            <input
              type="text"
              placeholder="Tìm kiếm theo tên tài liệu hoặc mã môn học..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-canvas-base border border-whisper-border rounded-xl pl-9 pr-4 py-2 text-xs font-semibold outline-none focus:ring-2 focus:ring-hust-red transition-all"
            />
          </div>

          {/* Filter dropdowns */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 bg-canvas-base border border-whisper-border rounded-md px-3 py-1.5 text-xs">
              <Filter className="h-4 w-4 text-muted-steel" />
              <span className="font-label-mono font-bold text-muted-steel uppercase tracking-wider text-[10px]">
                Trạng thái:
              </span>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="bg-transparent border-none outline-none font-semibold text-slate-800 cursor-pointer"
              >
                <option value="ALL">Tất cả</option>
                <option value="UPLOADED">Đã tải lên</option>
                <option value="PARSING">Đang chạy OCR</option>
                <option value="EVALUATING">Đang đánh giá AI</option>
                <option value="NEEDS_REVIEW">Chờ kiểm duyệt</option>
                <option value="APPROVED">Đã duyệt</option>
                <option value="INDEXING">Đang lập chỉ mục</option>
                <option value="INDEXED">Hoàn thành</option>
                <option value="REJECTED">Bị từ chối</option>
                <option value="FAILED">Gặp lỗi</option>
              </select>
            </div>

            <div className="flex items-center gap-2 bg-canvas-base border border-whisper-border rounded-md px-3 py-1.5 text-xs">
              <BookOpen className="h-4 w-4 text-muted-steel" />
              <span className="font-label-mono font-bold text-muted-steel uppercase tracking-wider text-[10px]">
                Môn học:
              </span>
              <select
                value={courseFilter}
                onChange={(e) => setCourseFilter(e.target.value)}
                className="bg-transparent border-none outline-none font-semibold text-slate-800 cursor-pointer"
              >
                <option value="ALL">Tất cả môn</option>
                {uniqueCourses.map((code) => (
                  <option key={code} value={code || ""}>{code}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Documents Table */}
        <div className="bg-white border border-whisper-border rounded-2xl shadow-sm overflow-hidden">
          {loading ? (
            <div className="py-24 text-center">
              <Loader2 className="mx-auto h-8 w-8 animate-spin text-hust-red" />
              <p className="mt-4 font-body-sm text-xs text-muted-steel font-semibold">Đang tải danh sách tài liệu...</p>
            </div>
          ) : error ? (
            <div className="py-16 text-center">
              <AlertCircle className="mx-auto h-12 w-12 text-system-red" />
              <p className="mt-4 font-headline-md text-base font-extrabold text-slate-900">Đã xảy ra lỗi</p>
              <p className="mt-1 font-body-sm text-xs text-muted-steel">{error}</p>
              <button 
                onClick={loadDocuments} 
                className="mt-6 tactile-button-primary text-[12px] py-1.5 px-4 bg-hust-red text-white"
              >
                Thử lại
              </button>
            </div>
          ) : filteredDocs.length === 0 ? (
            <div className="py-20 text-center">
              <FileText className="mx-auto h-12 w-12 text-muted-steel" />
              <p className="mt-4 font-headline-md text-base font-extrabold text-slate-900">Không tìm thấy tài liệu nào</p>
              <p className="mt-1 font-body-sm text-xs text-muted-steel">
                {documents.length === 0 
                  ? "Bạn chưa đăng tải bất kỳ tài liệu học tập nào lên cộng đồng." 
                  : "Không có tài liệu nào khớp với bộ lọc hiện tại."}
              </p>
              {documents.length === 0 && (
                <Link
                  href="/courses"
                  className="mt-6 tactile-button-primary text-[12px] py-2 px-4 bg-hust-red text-white"
                >
                  <UploadCloud className="h-4 w-4 mr-2" /> Đóng góp tài liệu ngay
                </Link>
              )}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-whisper-border bg-slate-50 font-label-mono text-[10px] font-bold text-muted-steel uppercase tracking-wider select-none">
                    <th className="p-4 w-12"></th>
                    <th className="p-4">Tên tài liệu</th>
                    <th className="p-4 w-28">Mã môn</th>
                    <th className="p-4 w-40">Ngày tải lên</th>
                    <th className="p-4 w-32">Dung lượng</th>
                    <th className="p-4 w-48">Trạng thái</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-whisper-border font-body-sm text-slate-800">
                  {filteredDocs.map((doc) => {
                    const isExpanded = expandedId === doc.id;
                    const steps = getPipelineSteps(doc.status);
                    
                    return (
                      <React.Fragment key={doc.id}>
                        {/* Table Row */}
                        <tr 
                          onClick={() => handleToggleExpand(doc.id)}
                          className={`cursor-pointer hover:bg-slate-50/50 transition-colors duration-150 ${isExpanded ? "bg-slate-50" : ""}`}
                        >
                          <td className="p-4 text-center" onClick={(e) => e.stopPropagation()}>
                            <button 
                              onClick={() => handleToggleExpand(doc.id)}
                              className="flex items-center justify-center h-6 w-6 rounded border border-whisper-border bg-white text-muted-steel hover:text-slate-800 hover:border-charcoal-ink transition-all cursor-pointer"
                            >
                              {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                            </button>
                          </td>
                          <td className="p-4 font-headline-md text-sm font-extrabold max-w-xs truncate md:max-w-md">
                            <div className="flex items-center gap-2">
                              <FileText className="h-4 w-4 text-muted-steel shrink-0" />
                              <span className="truncate text-slate-900" title={doc.display_name || doc.original_filename}>
                                {doc.display_name || doc.original_filename}
                              </span>
                            </div>
                          </td>
                          <td className="p-4 font-bold text-muted-steel">
                            {doc.course_code || "N/A"}
                          </td>
                          <td className="p-4 text-muted-steel font-semibold text-xs">
                            <span className="inline-flex items-center gap-1.5">
                              <Calendar className="h-3.5 w-3.5" />
                              {new Date(doc.uploaded_at).toLocaleString("vi-VN", {
                                day: "2-digit",
                                month: "2-digit",
                                year: "numeric",
                                hour: "2-digit",
                                minute: "2-digit"
                              })}
                            </span>
                          </td>
                          <td className="p-4 text-muted-steel font-semibold text-xs">
                            {formatBytes((parseInt(doc.id.substring(0, 8), 16) % 1500000) + 120000)}
                          </td>
                          <td className="p-4">
                            {getStatusBadge(doc.status)}
                          </td>
                        </tr>

                        {/* Expandable Timeline section */}
                        {isExpanded && (
                          <tr>
                            <td colSpan={6} className="p-0 bg-slate-50/30">
                              <div className="p-6 border-t border-b border-whisper-border space-y-6">
                                <div className="flex items-center justify-between border-b border-whisper-border pb-3">
                                  <h4 className="font-headline-md text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                                    <FileText className="h-4 w-4 text-muted-steel animate-pulse" /> Tiến trình xử lý Pipeline
                                  </h4>
                                  <span className="font-mono text-xs text-muted-steel">ID: {doc.id}</span>
                                </div>

                                {/* Step timeline grid */}
                                <div className="grid grid-cols-1 md:grid-cols-5 gap-6 relative">
                                  {steps.map((step, idx) => {
                                    let iconElement;
                                    let circleColorClass = "";
                                    let titleColorClass = "";
                                    let descColorClass = "";

                                    if (step.status === "done") {
                                      iconElement = <CheckCircle2 className="h-5 w-5 text-system-green" />;
                                      circleColorClass = "bg-green-50 border-system-green";
                                      titleColorClass = "text-system-green font-extrabold";
                                      descColorClass = "text-muted-steel font-semibold";
                                    } else if (step.status === "in_progress") {
                                      iconElement = <Loader2 className="h-5 w-5 animate-spin text-blue-600" />;
                                      circleColorClass = "bg-blue-50 border-blue-500 animate-pulse";
                                      titleColorClass = "text-blue-600 font-extrabold";
                                      descColorClass = "text-slate-900 font-semibold";
                                    } else if (step.status === "failed") {
                                      iconElement = <XCircle className="h-5 w-5 text-system-red" />;
                                      circleColorClass = "bg-red-50 border-system-red animate-bounce";
                                      titleColorClass = "text-system-red font-extrabold";
                                      descColorClass = "text-system-red/80 font-semibold";
                                    } else {
                                      iconElement = <div className="h-2 w-2 rounded-full bg-slate-300" />;
                                      circleColorClass = "bg-slate-50 border-whisper-border";
                                      titleColorClass = "text-slate-400 font-bold";
                                      descColorClass = "text-slate-300 font-semibold";
                                    }

                                    return (
                                      <div key={idx} className="relative flex flex-col items-center md:items-start text-center md:text-left">
                                        {idx < 4 && (
                                          <div className="hidden md:block absolute top-5 left-10 w-full h-[2px] bg-slate-200 z-0">
                                            <div 
                                              className={`h-full transition-all duration-300 ${
                                                step.status === "done" ? "bg-system-green" : ""
                                              }`} 
                                              style={{ width: step.status === "done" ? "100%" : "0%" }}
                                            />
                                          </div>
                                        )}

                                        <div className={`relative z-10 flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all ${circleColorClass}`}>
                                          {iconElement}
                                        </div>

                                        <div className="mt-3 space-y-1 px-2 md:px-0">
                                          <h5 className={`font-headline-md text-xs ${titleColorClass}`}>
                                            {step.label}
                                          </h5>
                                          <p className={`font-body-sm text-[11px] ${descColorClass} leading-snug`}>
                                            {step.description}
                                          </p>
                                        </div>
                                      </div>
                                    );
                                  })}
                                </div>

                                {/* Reviewer Note or failure alerts */}
                                {(doc.status.toUpperCase() === "REJECTED" || doc.status.toUpperCase() === "FAILED") && (
                                  <div className="rounded-xl border border-system-red/20 bg-red-50/50 p-4 mt-6 animate-fadeIn">
                                    <div className="flex items-start gap-3">
                                      <AlertCircle className="h-5 w-5 text-system-red shrink-0 mt-0.5" />
                                      <div className="space-y-2">
                                        <h5 className="font-headline-md text-sm font-extrabold text-system-red">
                                          {doc.status.toUpperCase() === "REJECTED" 
                                            ? "Tài liệu không được phê duyệt bởi ban kiểm duyệt học thuật" 
                                            : "Gặp lỗi kỹ thuật khi xử lý tài liệu"}
                                        </h5>
                                        <p className="font-body-sm text-xs text-slate-700 leading-relaxed font-semibold">
                                          {doc.status.toUpperCase() === "REJECTED"
                                            ? doc.reviewer_note ||
                                              "Người kiểm duyệt từ chối tài liệu này vì lý do học thuật hoặc chất lượng file kém."
                                            : doc.failure_hint ||
                                              "Hệ thống xử lý tài liệu tự động (OCR/AI evaluation) đã gặp sự cố. Vui lòng tải lại hoặc liên hệ quản trị viên."}
                                        </p>
                                        {doc.course_code && (
                                          <div className="pt-2">
                                            <Link
                                              href={`/courses/${doc.course_code.toLowerCase()}`}
                                              className="inline-flex items-center gap-2 rounded-lg bg-system-red hover:opacity-90 text-white font-bold text-xs px-3 py-1.5 transition-all shadow-xs cursor-pointer"
                                            >
                                              <UploadCloud className="h-3.5 w-3.5" /> Tải lên lại tài liệu môn này
                                            </Link>
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                  </div>
                                )}
                              </div>
                            </td>
                          </tr>
                        )}
                      </React.Fragment>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
