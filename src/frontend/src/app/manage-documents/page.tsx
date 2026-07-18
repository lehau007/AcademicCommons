/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
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
  BookOpen,
  Trash2,
  ShieldAlert,
  Eye,
  ClipboardCheck,
  ExternalLink,
  X,
  CheckCheck,
  Sparkles,
} from "lucide-react";
import AppShell from "@/components/app-shell";
import MarkdownRenderer from "@/components/markdown-renderer";
import ConfirmDialog from "@/components/confirm-dialog";
import { useToast } from "@/components/toast";
import api from "@/lib/api";
import { useAsyncAction } from "@/lib/useAsyncAction";

interface EvaluationReport {
  final_recommendation: string | null;
  agent1_output: any;
  agent2_output: any;
  agent3_output: any;
  generated_at?: string;
}

interface ManagedDocument {
  id: string;
  course_id: string;
  course_code: string | null;
  uploader_id: string;
  document_tier: string;
  material_type: string | null;
  contribution_type: string | null;
  status: string;
  original_filename: string;
  display_name?: string | null;
  file_format: string;
  uploaded_at: string;
  updated_at: string;
  reviewer_note: string | null;
  ai_recommendation?: string | null;
  ai_overall_score?: number | null;
}

const QUICK_APPROVE_THRESHOLD = 90;

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

  steps[0].status = "done";
  if (s === "UPLOADED" || s === "PARSING") {
    steps[1].status = "in_progress";
  } else if (s === "EVALUATING") {
    steps[1].status = "done";
    steps[2].status = "in_progress";
  } else if (s === "NEEDS_REVIEW") {
    steps[1].status = "done";
    steps[2].status = "done";
    steps[3].status = "in_progress";
  } else if (s === "APPROVED" || s === "INDEXING") {
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

function getStatusBadge(status: string) {
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
}

export default function ManageDocumentsPage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [user, setUser] = useState<any>(null);
  const [documents, setDocuments] = useState<ManagedDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [courseFilter, setCourseFilter] = useState("ALL");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  // Bulk approve (quick approve) state
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [bulkConfirmOpen, setBulkConfirmOpen] = useState(false);

  // Delete modal state
  const [deleteTarget, setDeleteTarget] = useState<ManagedDocument | null>(null);
  const [deleteReason, setDeleteReason] = useState("");
  const [deleteError, setDeleteError] = useState("");

  // Detail (document content) modal state
  const [detailTarget, setDetailTarget] = useState<ManagedDocument | null>(null);
  const [detailMarkdown, setDetailMarkdown] = useState("");
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState("");
  const [rawLoading, setRawLoading] = useState(false);

  // Evaluation (AI agent report) modal state
  const [evalTarget, setEvalTarget] = useState<ManagedDocument | null>(null);
  const [evalReport, setEvalReport] = useState<EvaluationReport | null>(null);
  const [evalLoading, setEvalLoading] = useState(false);
  const [evalError, setEvalError] = useState("");

  async function loadDocuments() {
    setLoading(true);
    setError("");
    try {
      const data = await api.get<any>("/documents/manage");
      setDocuments(Array.isArray(data) ? data : data.items || []);
    } catch (err: any) {
      console.error("Failed to load managed documents:", err);
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
        if (!loggedInUser || (loggedInUser.role !== "admin" && loggedInUser.role !== "reviewer")) {
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
  }, [router]);

  const handleToggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const openDeleteModal = (doc: ManagedDocument) => {
    setDeleteTarget(doc);
    setDeleteReason("");
    setDeleteError("");
  };

  const closeDeleteModal = () => {
    if (isDeleting) return;
    setDeleteTarget(null);
    setDeleteReason("");
    setDeleteError("");
  };

  const { pending: isDeleting, run: handleConfirmDelete } = useAsyncAction(async () => {
    if (!deleteTarget) return;
    if (deleteReason.trim().length < 3) {
      setDeleteError("Vui lòng nhập nguyên nhân xoá (tối thiểu 3 ký tự).");
      return;
    }
    setDeleteError("");
    try {
      await api.del(`/documents/${deleteTarget.id}`, { reason: deleteReason.trim() });
      setDocuments((prev) => prev.filter((d) => d.id !== deleteTarget.id));
      setDeleteTarget(null);
      setDeleteReason("");
    } catch (err: any) {
      setDeleteError(err.message || "Xoá tài liệu thất bại.");
    }
  });

  const openDetail = async (doc: ManagedDocument) => {
    setDetailTarget(doc);
    setDetailMarkdown("");
    setDetailError("");
    setDetailLoading(true);
    try {
      const md = await api.get<string>(`/documents/${doc.id}/markdown`);
      setDetailMarkdown(typeof md === "string" ? md : JSON.stringify(md));
    } catch (err: any) {
      setDetailError(err.message || "Không thể tải nội dung tài liệu.");
    } finally {
      setDetailLoading(false);
    }
  };

  const openRawFile = async (doc: ManagedDocument) => {
    setRawLoading(true);
    try {
      const res = await api.get<{ url: string }>(`/documents/${doc.id}/raw-url`);
      if (res?.url) {
        window.open(res.url, "_blank", "noopener,noreferrer");
      }
    } catch (err: any) {
      setDetailError(err.message || "Không thể mở tệp gốc.");
    } finally {
      setRawLoading(false);
    }
  };

  const openEvaluation = async (doc: ManagedDocument) => {
    setEvalTarget(doc);
    setEvalReport(null);
    setEvalError("");
    setEvalLoading(true);
    try {
      const report = await api.get<EvaluationReport>(`/documents/${doc.id}/evaluation-report`);
      setEvalReport(report);
    } catch (err: any) {
      setEvalError(err.message || "Không thể tải báo cáo đánh giá.");
    } finally {
      setEvalLoading(false);
    }
  };

  const evalScore = (key: "relevance" | "completeness" | "quality"): number => {
    const v = evalReport?.agent3_output?.scores?.[key];
    return typeof v === "number" ? v : 0;
  };
  const evalJustification = (key: string): string => {
    const j = evalReport?.agent3_output?.evaluation_justification;
    return (j && j[key]) || "";
  };

  const uniqueCourses = Array.from(new Set(documents.map((d) => d.course_code).filter(Boolean)));

  const filteredDocs = documents.filter((doc) => {
    const filenameMatch = (doc.display_name || doc.original_filename).toLowerCase().includes(searchQuery.toLowerCase());
    const courseCodeMatch = doc.course_code && doc.course_code.toLowerCase().includes(searchQuery.toLowerCase());
    const queryMatch = filenameMatch || courseCodeMatch;
    const statusMatch = statusFilter === "ALL" || doc.status.toUpperCase() === statusFilter;
    const courseMatch = courseFilter === "ALL" || doc.course_code === courseFilter;
    const uploadedMs = new Date(doc.uploaded_at).getTime();
    const fromMatch = !dateFrom || uploadedMs >= new Date(`${dateFrom}T00:00:00`).getTime();
    const toMatch = !dateTo || uploadedMs <= new Date(`${dateTo}T23:59:59`).getTime();
    return queryMatch && statusMatch && courseMatch && fromMatch && toMatch;
  });

  // --- Bulk quick-approve (only NEEDS_REVIEW documents are selectable) ---
  const isSelectable = (doc: ManagedDocument) => doc.status.toUpperCase() === "NEEDS_REVIEW";
  const eligibleHighScore = filteredDocs.filter(
    (d) => isSelectable(d) && (d.ai_overall_score ?? 0) >= QUICK_APPROVE_THRESHOLD
  );

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };
  const selectHighScore = () => setSelectedIds(new Set(eligibleHighScore.map((d) => d.id)));
  const clearSelection = () => setSelectedIds(new Set());

  const { pending: bulkBusy, run: handleBulkApprove } = useAsyncAction(async () => {
    try {
      const ids = Array.from(selectedIds);
      const res = await api.post<{ count?: number }>("/review/batch-approve", { document_ids: ids });
      showToast(`Đã duyệt nhanh ${res?.count ?? ids.length} tài liệu.`, "success");
      clearSelection();
      setBulkConfirmOpen(false);
      await loadDocuments();
    } catch {
      showToast(
        "Duyệt nhanh thất bại. Một số tài liệu có thể đã được duyệt hoặc chưa có báo cáo đánh giá. Không có thay đổi nào được áp dụng.",
        "error"
      );
      setBulkConfirmOpen(false);
    }
  });

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Header */}
        <div className="relative rounded-2xl border border-whisper-border bg-white p-6 shadow-sm overflow-hidden">
          <div className="absolute top-0 right-0 h-24 w-24 translate-x-8 -translate-y-8 rounded-full bg-hust-red/5 blur-2xl" />
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <h1 className="font-headline-lg text-2xl font-black text-slate-900">Quản Lý Tài Liệu</h1>
              <p className="mt-1 font-body-sm text-xs text-muted-steel font-semibold max-w-2xl">
                {user?.role === "admin"
                  ? "Theo dõi tiến trình xử lý (OCR, đánh giá AI, kiểm duyệt, lập chỉ mục) của mọi tài liệu trong hệ thống và xoá tài liệu kèm nguyên nhân."
                  : "Theo dõi tiến trình xử lý và xoá (kèm nguyên nhân) các tài liệu thuộc những học phần bạn được phân công phụ trách."}
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

        {/* Filters */}
        <div className="flex flex-col gap-4 md:flex-row md:items-center justify-between bg-white border border-whisper-border rounded-2xl p-4 shadow-sm">
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
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 bg-canvas-base border border-whisper-border rounded-md px-3 py-1.5 text-xs">
              <Filter className="h-4 w-4 text-muted-steel" />
              <span className="font-label-mono font-bold text-muted-steel uppercase tracking-wider text-[10px]">Trạng thái:</span>
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
              <span className="font-label-mono font-bold text-muted-steel uppercase tracking-wider text-[10px]">Môn học:</span>
              <select
                value={courseFilter}
                onChange={(e) => setCourseFilter(e.target.value)}
                className="bg-transparent border-none outline-none font-semibold text-slate-800 cursor-pointer"
              >
                <option value="ALL">Tất cả môn</option>
                {uniqueCourses.map((code) => (
                  <option key={code} value={code || ""}>
                    {code}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-center gap-2 bg-canvas-base border border-whisper-border rounded-md px-3 py-1.5 text-xs">
              <Calendar className="h-4 w-4 text-muted-steel" />
              <span className="font-label-mono font-bold text-muted-steel uppercase tracking-wider text-[10px]">Ngày tải:</span>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="bg-transparent border-none outline-none font-semibold text-slate-800 cursor-pointer"
              />
              <span className="text-muted-steel">→</span>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="bg-transparent border-none outline-none font-semibold text-slate-800 cursor-pointer"
              />
              {(dateFrom || dateTo) && (
                <button
                  onClick={() => {
                    setDateFrom("");
                    setDateTo("");
                  }}
                  title="Xoá lọc ngày"
                  className="text-muted-steel hover:text-system-red"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Bulk quick-approve action bar */}
        {(selectedIds.size > 0 || eligibleHighScore.length > 0) && (
          <div className="flex flex-wrap items-center justify-between gap-3 bg-[#FFF8F6] border border-hust-red/20 rounded-2xl px-4 py-3 shadow-sm">
            <div className="flex items-center gap-2 text-xs font-semibold text-charcoal-ink">
              <Sparkles className="h-4 w-4 text-hust-red shrink-0" />
              {selectedIds.size > 0 ? (
                <span>
                  Đã chọn <b>{selectedIds.size}</b> tài liệu để duyệt nhanh
                </span>
              ) : (
                <span>
                  Có <b>{eligibleHighScore.length}</b> tài liệu được AI chấm ≥ {QUICK_APPROVE_THRESHOLD}% đang chờ duyệt
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              {eligibleHighScore.length > 0 && (
                <button
                  onClick={selectHighScore}
                  className="tactile-button text-[12px] py-1.5 px-3 bg-white border border-whisper-border text-charcoal-ink"
                >
                  Chọn tất cả AI ≥ {QUICK_APPROVE_THRESHOLD}%
                </button>
              )}
              {selectedIds.size > 0 && (
                <>
                  <button
                    onClick={clearSelection}
                    className="tactile-button text-[12px] py-1.5 px-3 bg-white border border-whisper-border text-muted-steel"
                  >
                    Bỏ chọn
                  </button>
                  <button
                    onClick={() => setBulkConfirmOpen(true)}
                    className="tactile-button-primary text-[12px] py-1.5 px-4 bg-hust-red text-white flex items-center gap-1.5"
                  >
                    <CheckCheck className="h-4 w-4" /> Duyệt nhanh ({selectedIds.size})
                  </button>
                </>
              )}
            </div>
          </div>
        )}

        {/* Table */}
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
              <button onClick={loadDocuments} className="mt-6 tactile-button-primary text-[12px] py-1.5 px-4 bg-hust-red text-white">
                Thử lại
              </button>
            </div>
          ) : filteredDocs.length === 0 ? (
            <div className="py-20 text-center">
              <FileText className="mx-auto h-12 w-12 text-muted-steel" />
              <p className="mt-4 font-headline-md text-base font-extrabold text-slate-900">Không tìm thấy tài liệu nào</p>
              <p className="mt-1 font-body-sm text-xs text-muted-steel">
                {documents.length === 0
                  ? "Hiện chưa có tài liệu nào thuộc phạm vi quản lý của bạn."
                  : "Không có tài liệu nào khớp với bộ lọc hiện tại."}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-whisper-border bg-slate-50 font-label-mono text-[10px] font-bold text-muted-steel uppercase tracking-wider select-none">
                    <th className="p-4 w-10"></th>
                    <th className="p-4 w-12"></th>
                    <th className="p-4">Tên tài liệu</th>
                    <th className="p-4 w-28">Mã môn</th>
                    <th className="p-4 w-40">Ngày tải lên</th>
                    <th className="p-4 w-48">Trạng thái</th>
                    <th className="p-4 w-40 text-center">Thao tác</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-whisper-border font-body-sm text-slate-800">
                  {filteredDocs.map((doc) => {
                    const isExpanded = expandedId === doc.id;
                    const steps = getPipelineSteps(doc.status);
                    return (
                      <React.Fragment key={doc.id}>
                        <tr
                          onClick={() => handleToggleExpand(doc.id)}
                          className={`cursor-pointer hover:bg-slate-50/50 transition-colors duration-150 ${isExpanded ? "bg-slate-50" : ""}`}
                        >
                          <td className="p-4 text-center" onClick={(e) => e.stopPropagation()}>
                            {isSelectable(doc) && (
                              <input
                                type="checkbox"
                                className="accent-hust-red h-4 w-4 cursor-pointer"
                                checked={selectedIds.has(doc.id)}
                                onChange={() => toggleSelect(doc.id)}
                                title="Chọn để duyệt nhanh"
                              />
                            )}
                          </td>
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
                              {doc.document_tier === "official" && (
                                <span className="shrink-0 rounded bg-hust-red/10 px-1.5 py-0.5 text-[9px] font-bold text-hust-red uppercase tracking-wide">
                                  Chính thức
                                </span>
                              )}
                            </div>
                          </td>
                          <td className="p-4 font-bold text-muted-steel">{doc.course_code || "N/A"}</td>
                          <td className="p-4 text-muted-steel font-semibold text-xs">
                            <span className="inline-flex items-center gap-1.5">
                              <Calendar className="h-3.5 w-3.5" />
                              {new Date(doc.uploaded_at).toLocaleString("vi-VN", {
                                day: "2-digit",
                                month: "2-digit",
                                year: "numeric",
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </span>
                          </td>
                          <td className="p-4">
                            {getStatusBadge(doc.status)}
                            {typeof doc.ai_overall_score === "number" && (
                              <span className="mt-1 flex items-center gap-1 text-[10px] font-bold text-muted-steel">
                                <Sparkles className="h-3 w-3 text-blue-500 shrink-0" />
                                AI: {doc.ai_overall_score}%{doc.ai_recommendation ? ` · ${doc.ai_recommendation}` : ""}
                              </span>
                            )}
                          </td>
                          <td className="p-4" onClick={(e) => e.stopPropagation()}>
                            <div className="flex items-center justify-center gap-1.5">
                              <button
                                onClick={() => openDetail(doc)}
                                title="Xem chi tiết tài liệu"
                                className="inline-flex items-center justify-center h-8 w-8 rounded-lg border border-whisper-border bg-white text-muted-steel hover:bg-charcoal-ink hover:text-white transition-all cursor-pointer"
                              >
                                <Eye className="h-4 w-4" />
                              </button>
                              <button
                                onClick={() => openEvaluation(doc)}
                                title="Xem đánh giá của AI"
                                className="inline-flex items-center justify-center h-8 w-8 rounded-lg border border-blue-100 bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white transition-all cursor-pointer"
                              >
                                <ClipboardCheck className="h-4 w-4" />
                              </button>
                              <button
                                onClick={() => openDeleteModal(doc)}
                                title="Xoá tài liệu"
                                className="inline-flex items-center justify-center h-8 w-8 rounded-lg border border-red-100 bg-red-50 text-system-red hover:bg-system-red hover:text-white transition-all cursor-pointer"
                              >
                                <Trash2 className="h-4 w-4" />
                              </button>
                            </div>
                          </td>
                        </tr>

                        {isExpanded && (
                          <tr>
                            <td colSpan={7} className="p-0 bg-slate-50/30">
                              <div className="p-6 border-t border-b border-whisper-border space-y-6">
                                <div className="flex items-center justify-between border-b border-whisper-border pb-3">
                                  <h4 className="font-headline-md text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                                    <FileText className="h-4 w-4 text-muted-steel animate-pulse" /> Tiến trình xử lý Pipeline
                                  </h4>
                                  <span className="font-mono text-xs text-muted-steel">ID: {doc.id}</span>
                                </div>

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
                                              className={`h-full transition-all duration-300 ${step.status === "done" ? "bg-system-green" : ""}`}
                                              style={{ width: step.status === "done" ? "100%" : "0%" }}
                                            />
                                          </div>
                                        )}
                                        <div className={`relative z-10 flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all ${circleColorClass}`}>
                                          {iconElement}
                                        </div>
                                        <div className="mt-3 space-y-1 px-2 md:px-0">
                                          <h5 className={`font-headline-md text-xs ${titleColorClass}`}>{step.label}</h5>
                                          <p className={`font-body-sm text-[11px] ${descColorClass} leading-snug`}>{step.description}</p>
                                        </div>
                                      </div>
                                    );
                                  })}
                                </div>

                                {(doc.status.toUpperCase() === "REJECTED" || doc.status.toUpperCase() === "FAILED") && (
                                  <div className="rounded-xl border border-system-red/20 bg-red-50/50 p-4 mt-6">
                                    <div className="flex items-start gap-3">
                                      <AlertCircle className="h-5 w-5 text-system-red shrink-0 mt-0.5" />
                                      <div className="space-y-1">
                                        <h5 className="font-headline-md text-sm font-extrabold text-system-red">
                                          {doc.status.toUpperCase() === "REJECTED"
                                            ? "Tài liệu không được phê duyệt bởi ban kiểm duyệt học thuật"
                                            : "Gặp lỗi kỹ thuật khi xử lý tài liệu"}
                                        </h5>
                                        <p className="font-body-sm text-xs text-slate-700 leading-relaxed font-semibold">
                                          {doc.reviewer_note ||
                                            (doc.status.toUpperCase() === "REJECTED"
                                              ? "Người kiểm duyệt từ chối tài liệu này vì lý do học thuật hoặc chất lượng file kém."
                                              : "Hệ thống xử lý tài liệu tự động (OCR/AI evaluation) đã gặp sự cố.")}
                                        </p>
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

      {/* Document detail modal */}
      {detailTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[1px] p-4">
          <div className="w-full max-w-[760px] max-h-[85vh] flex flex-col bg-white border border-whisper-border rounded-2xl shadow-xl">
            <div className="flex items-start justify-between gap-3 border-b border-whisper-border p-5">
              <div className="min-w-0">
                <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink flex items-center gap-2">
                  <Eye className="h-5 w-5 text-charcoal-ink" /> Chi tiết tài liệu
                </h3>
                <p className="text-[11px] text-muted-steel mt-0.5 truncate" title={detailTarget.display_name || detailTarget.original_filename}>
                  {detailTarget.course_code} — {detailTarget.display_name || detailTarget.original_filename}
                </p>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => openRawFile(detailTarget)}
                  disabled={rawLoading}
                  className="tactile-button text-[11px] py-1.5 px-3 bg-white border border-whisper-border text-charcoal-ink flex items-center gap-1.5 disabled:opacity-60"
                >
                  {rawLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <ExternalLink className="h-3.5 w-3.5" />}
                  Mở tệp gốc
                </button>
                <button onClick={() => setDetailTarget(null)} className="text-muted-steel hover:text-charcoal-ink">
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>
            <div className="p-5 overflow-y-auto">
              {detailLoading ? (
                <div className="py-16 text-center text-muted-steel text-sm flex items-center justify-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" /> Đang tải nội dung...
                </div>
              ) : detailError ? (
                <div className="py-12 text-center">
                  <AlertCircle className="mx-auto h-10 w-10 text-system-red" />
                  <p className="mt-3 text-sm font-bold text-slate-900">Không có nội dung để hiển thị</p>
                  <p className="mt-1 text-xs text-muted-steel">
                    {detailError.includes("not available") || detailError.includes("404")
                      ? "Tài liệu chưa được trích xuất nội dung (OCR chưa hoàn tất). Bạn vẫn có thể mở tệp gốc."
                      : detailError}
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <span className="text-[10px] bg-system-green/10 text-system-green font-bold px-2 py-0.5 rounded border border-system-green/20">
                    OCR Normalized Content
                  </span>
                  <MarkdownRenderer
                    content={
                      detailMarkdown ||
                      `# ${detailTarget.original_filename}\n\nNội dung văn bản gốc chưa trích xuất hoặc đang chạy tiến trình tự động.`
                    }
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* AI evaluation modal */}
      {evalTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[1px] p-4">
          <div className="w-full max-w-[640px] max-h-[85vh] flex flex-col bg-white border border-whisper-border rounded-2xl shadow-xl">
            <div className="flex items-start justify-between gap-3 border-b border-whisper-border p-5">
              <div className="min-w-0">
                <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink flex items-center gap-2">
                  <ClipboardCheck className="h-5 w-5 text-blue-600" /> Đánh giá của AI
                </h3>
                <p className="text-[11px] text-muted-steel mt-0.5 truncate" title={evalTarget.display_name || evalTarget.original_filename}>
                  {evalTarget.course_code} — {evalTarget.display_name || evalTarget.original_filename}
                </p>
              </div>
              <button onClick={() => setEvalTarget(null)} className="text-muted-steel hover:text-charcoal-ink shrink-0">
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="p-5 overflow-y-auto space-y-5">
              {evalLoading ? (
                <div className="py-16 text-center text-muted-steel text-sm flex items-center justify-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" /> Đang tải báo cáo đánh giá...
                </div>
              ) : evalError ? (
                <div className="py-12 text-center">
                  <ClipboardCheck className="mx-auto h-10 w-10 text-muted-steel" />
                  <p className="mt-3 text-sm font-bold text-slate-900">Chưa có báo cáo đánh giá AI</p>
                  <p className="mt-1 text-xs text-muted-steel">
                    {evalError.includes("404") || evalError.includes("No evaluation")
                      ? "Tài liệu này chưa được agent đánh giá, hoặc đang trong giai đoạn xử lý."
                      : evalError}
                  </p>
                </div>
              ) : (
                <>
                  {evalReport?.final_recommendation && (
                    <div className="rounded-xl border border-whisper-border bg-canvas-base p-4">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-muted-steel">
                        Khuyến nghị cuối cùng của AI
                      </span>
                      <p className="mt-1 font-headline-md text-sm font-extrabold text-charcoal-ink">
                        {evalReport.final_recommendation}
                      </p>
                    </div>
                  )}

                  <div className="grid grid-cols-3 gap-3">
                    {(["relevance", "completeness", "quality"] as const).map((k) => {
                      const label = { relevance: "Độ liên quan", completeness: "Độ đầy đủ", quality: "Chất lượng" }[k];
                      const pct = Math.round(evalScore(k) * 10);
                      return (
                        <div key={k} className="rounded-xl border border-whisper-border p-3 text-center">
                          <div className="text-2xl font-black text-blue-600">{pct}%</div>
                          <div className="text-[10px] font-bold uppercase tracking-wider text-muted-steel mt-1">{label}</div>
                        </div>
                      );
                    })}
                  </div>

                  <div className="space-y-3">
                    {[
                      { key: "relevance_rationale", label: "Lý giải độ liên quan" },
                      { key: "completeness_rationale", label: "Lý giải độ đầy đủ" },
                      { key: "quality_rationale", label: "Lý giải chất lượng" },
                      { key: "overall_rationale", label: "Nhận định tổng thể" },
                    ].map(({ key, label }) => {
                      const text = evalJustification(key);
                      if (!text) return null;
                      return (
                        <div key={key} className="rounded-xl bg-slate-50 border border-whisper-border p-3">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-muted-steel">{label}</span>
                          <p className="mt-1 text-[12px] text-slate-700 leading-relaxed font-semibold">{text}</p>
                        </div>
                      );
                    })}
                  </div>

                  {typeof evalReport?.agent1_output?.duplicate?.similarity_score === "number" && (
                    <div className="rounded-xl border border-amber-200 bg-amber-50 p-3">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-amber-700">
                        Mức độ trùng lặp (Chunk-Level Set Matching)
                      </span>
                      <p className="mt-1 text-sm font-extrabold text-amber-800">
                        {Math.round(evalReport.agent1_output.duplicate.similarity_score * 100)}%
                      </p>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Delete modal */}
      {deleteTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[1px]">
          <div className="w-full max-w-[480px] bg-white border border-whisper-border rounded-2xl p-6 shadow-xl space-y-4">
            <div className="flex items-start gap-3 border-b border-whisper-border pb-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-red-50">
                <ShieldAlert className="h-5 w-5 text-system-red" />
              </div>
              <div className="min-w-0">
                <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink">Xoá vĩnh viễn tài liệu</h3>
                <p className="text-[11px] text-muted-steel mt-0.5 truncate" title={deleteTarget.display_name || deleteTarget.original_filename}>
                  {deleteTarget.course_code} — {deleteTarget.display_name || deleteTarget.original_filename}
                </p>
              </div>
            </div>

            <div className="rounded-lg bg-amber-50 border border-amber-200 p-3 text-[11px] text-amber-800 font-semibold leading-relaxed">
              Hành động này sẽ xoá vĩnh viễn tài liệu, tệp tin trên kho lưu trữ và toàn bộ dữ liệu liên quan
              (chỉ mục, đánh giá, lịch sử xử lý). Không thể hoàn tác.
            </div>

            <div className="space-y-1">
              <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">
                Nguyên nhân xoá <span className="text-system-red">*</span>
              </label>
              <textarea
                rows={3}
                value={deleteReason}
                onChange={(e) => {
                  setDeleteReason(e.target.value);
                  if (deleteError) setDeleteError("");
                }}
                placeholder="Ví dụ: Tài liệu trùng lặp / sai học phần / vi phạm bản quyền..."
                className={`w-full bg-[#F8FAFC] border rounded-xl px-4 py-2.5 text-body-md focus:ring-2 focus:ring-hust-red focus:border-hust-red outline-none resize-none ${
                  deleteError ? "border-system-red" : "border-whisper-border"
                }`}
              />
              {deleteError && <span className="block text-[11px] text-system-red font-semibold mt-1">{deleteError}</span>}
            </div>

            <div className="flex gap-3 pt-1">
              <button
                type="button"
                onClick={closeDeleteModal}
                disabled={isDeleting}
                className="tactile-button bg-white border border-whisper-border text-charcoal-ink flex-1 py-2 disabled:opacity-60"
              >
                Hủy bỏ
              </button>
              <button
                type="button"
                onClick={handleConfirmDelete}
                disabled={isDeleting}
                className="tactile-button flex-1 py-2 bg-system-red text-white hover:opacity-90 flex items-center justify-center gap-2 disabled:opacity-60"
              >
                {isDeleting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" /> Đang xoá...
                  </>
                ) : (
                  <>
                    <Trash2 className="h-4 w-4" /> Xoá vĩnh viễn
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmDialog
        open={bulkConfirmOpen}
        title="Duyệt nhanh tài liệu"
        message={`Bạn sắp phê duyệt ${selectedIds.size} tài liệu đã chọn. Các tài liệu sẽ chuyển sang trạng thái đã duyệt và được lập chỉ mục. Tiếp tục?`}
        confirmLabel="Duyệt nhanh"
        busy={bulkBusy}
        onConfirm={handleBulkApprove}
        onCancel={() => setBulkConfirmOpen(false)}
      />
    </AppShell>
  );
}
