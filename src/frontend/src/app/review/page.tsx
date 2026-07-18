/* eslint-disable react-hooks/set-state-in-effect, @typescript-eslint/no-explicit-any */
"use client";

import React, { useState, useEffect } from "react";
import AppShell from "../../components/app-shell";
import MarkdownRenderer from "../../components/markdown-renderer";
import api from "../../lib/api";
import { useAsyncAction } from "../../lib/useAsyncAction";
import { useToast } from "../../components/toast";
import {
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Clock, 
  FileText, 
  ArrowRight,
  ShieldAlert,
  BarChart2,
  Download
} from "lucide-react";

interface ReviewQueueItem {
  document_id: string;
  filename: string;
  course_code: string;
  document_tier: string;
  status: string;
  sla_deadline: string | null;
  sla_breached: boolean;
  no_reviewer_flag: boolean;
  uploaded_at: string;
}

interface ReviewAnalytics {
  average_sla_hours_per_course: Record<string, number>;
  sla_threshold_hours_per_course: Record<string, number>;
  ai_agreement_rate: number;
  ai_override_rate: number;
}

export default function ReviewerWorkspacePage() {
  const { showToast } = useToast();
  const [activeSubTab, setActiveSubTab] = useState<"queue" | "analytics">("queue");
  const [queueDocs, setQueueDocs] = useState<ReviewQueueItem[]>([]);
  const [analytics, setAnalytics] = useState<ReviewAnalytics | null>(null);
  
  // Selected document full details
  const [selectedDoc, setSelectedDoc] = useState<any | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [loadingQueue, setLoadingQueue] = useState(true);

  // Form states for review decision
  const [reviewNote, setReviewNote] = useState("");
  const [showOverrideModal, setShowOverrideModal] = useState(false);
  const [pendingDecision, setPendingDecision] = useState<string | null>(null);
  const [exporting, setExporting] = useState(false);

  // Export review decisions to CSV for reporting
  const handleExportCsv = async () => {
    setExporting(true);
    try {
      const csv = await api.get<string>("/review/decisions/export");
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `review-decisions-${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      showToast("Đã xuất báo cáo CSV các quyết định kiểm duyệt.", "success");
    } catch (err: any) {
      showToast(`Không thể xuất CSV: ${err.message || "Lỗi kết nối."}`, "error");
    } finally {
      setExporting(false);
    }
  };

  // Fetch queue and analytics on mount
  const fetchQueue = async () => {
    try {
      setLoadingQueue(true);
      const queue = await api.get<ReviewQueueItem[]>("/review/queue");
      setQueueDocs(queue || []);
    } catch (err) {
      console.error("Failed to load review queue:", err);
    } finally {
      setLoadingQueue(false);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const stats = await api.get<ReviewAnalytics>("/review/analytics");
      setAnalytics(stats);
    } catch (err) {
      console.error("Failed to load review analytics:", err);
    }
  };

  useEffect(() => {
    fetchQueue();
    fetchAnalytics();
  }, []);

  // Handle selecting a document from the queue to review
  const handleSelectDoc = async (item: ReviewQueueItem) => {
    setLoadingDetail(true);
    try {
      const [detail, metadata, markdown] = await Promise.all([
        api.get<any>(`/review/${item.document_id}`),
        api.get<any>(`/documents/${item.document_id}`),
        api.get<string>(`/documents/${item.document_id}/markdown`),
      ]);

      // Combine review detail, metadata, and markdown
      setSelectedDoc({
        id: item.document_id,
        course_code: item.course_code,
        tier: item.document_tier,
        status: item.status,
        title: metadata.filename || metadata.title || "Tài liệu học thuật",
        filename: metadata.filename,
        uploaded_by: metadata.uploader_id || "Sinh viên HUST",
        uploaded_at: metadata.uploaded_at,
        markdown_content: markdown,
        evaluation_report: detail.evaluation_report,
        state_logs: detail.state_logs || [],
      });
    } catch (err) {
      console.error("Failed to load document review details:", err);
      showToast("Không thể tải thông tin chi tiết tài liệu.", "error");
    } finally {
      setLoadingDetail(false);
    }
  };

  // Open the original uploaded file via a short-lived signed URL.
  const openOriginalFile = async () => {
    if (!selectedDoc) return;
    try {
      const res = await api.get<{ url: string }>(`/documents/${selectedDoc.id}/raw-url`);
      if (res?.url) {
        window.open(res.url, "_blank", "noopener,noreferrer");
      } else {
        showToast("Không lấy được liên kết tệp gốc.", "error");
      }
    } catch (err) {
      console.error("Failed to open original file:", err);
      showToast("Không thể mở tệp gốc.", "error");
    }
  };

  // Decision actions
  const handleDecisionClick = (status: "APPROVED" | "REJECTED") => {
    // Warn only when rejecting a document the AI recommended approving.
    if (status === "REJECTED" && getRecommendation() === "APPROVE") {
      setPendingDecision(status);
      setShowOverrideModal(true);
    } else {
      submitDecision(status);
    }
  };

  const { pending: deciding, run: submitDecision } = useAsyncAction(async (decisionStatus: "APPROVED" | "REJECTED" | "OVERRIDE_APPROVE" | "OVERRIDE_REJECT", overrideReason: string = "") => {
    if (!selectedDoc) return;

    try {
      // Map the UI status to the backend decision enum
      // (backend accepts APPROVE | REJECT | OVERRIDE_APPROVE | OVERRIDE_REJECT).
      let finalDecision = decisionStatus === "APPROVED" ? "APPROVE" : decisionStatus === "REJECTED" ? "REJECT" : decisionStatus;
      if (overrideReason) {
        finalDecision = decisionStatus === "APPROVED" ? "OVERRIDE_APPROVE" : "OVERRIDE_REJECT";
      }

      await api.post(`/review/${selectedDoc.id}/decide`, {
        decision: finalDecision,
        final_contribution_type: selectedDoc.tier === "community" ? "summary_note" : undefined,
        note: overrideReason || reviewNote || "Đã kiểm duyệt bởi Subject Reviewer",
      });

      showToast(`Tài liệu "${selectedDoc.title}" đã được quyết định: ${decisionStatus}!`, "success");
      setSelectedDoc(null);
      setReviewNote("");
      setShowOverrideModal(false);
      
      // Refresh state
      await Promise.all([fetchQueue(), fetchAnalytics()]);
    } catch (err: any) {
      console.error("Failed to submit review decision:", err);
      showToast(`Lỗi phê duyệt tài liệu: ${err.message}`, "error");
    }
  });

  // Resolvers reading the real backend EvaluationReport JSONB shape.
  // Scores live in agent3_output.scores (0-10 scale); justifications in
  // agent3_output.evaluation_justification; duplicate info in agent1_output.duplicate.
  const getScore = (key: "relevance" | "completeness" | "quality"): number => {
    const v = selectedDoc?.evaluation_report?.agent3_output?.scores?.[key];
    return typeof v === "number" ? v : 0; // 0-10
  };

  const getJustification = (key: string): string => {
    const j = selectedDoc?.evaluation_report?.agent3_output?.evaluation_justification;
    return (j?.[key] as string) || "";
  };

  const getPlagiarismSimilarity = (): number => {
    const v = selectedDoc?.evaluation_report?.agent1_output?.duplicate?.similarity_score;
    return typeof v === "number" ? v : 0; // 0-1
  };

  const getRecommendation = (): string =>
    selectedDoc?.evaluation_report?.final_recommendation || "";

  return (
    <AppShell>
      <div className="flex flex-col h-full bg-canvas-base overflow-hidden">
        {/* Sub-navigation header */}
        <header className="flex justify-between items-center bg-white border-b border-whisper-border px-6 py-3 shrink-0">
          <div className="flex gap-2">
            <button 
              className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg font-display text-xs font-bold transition-all border ${
                activeSubTab === "queue" 
                  ? "bg-hust-red text-white border-hust-red" 
                  : "bg-white text-charcoal-ink border-whisper-border hover:bg-canvas-base"
              }`}
              onClick={() => { setActiveSubTab("queue"); setSelectedDoc(null); }}
            >
              <Clock className="w-3.5 h-3.5" />
              <span>Hàng đợi phê duyệt ({queueDocs.length})</span>
            </button>
            <button 
              className={`flex items-center gap-1.5 px-4 py-1.5 rounded-lg font-display text-xs font-bold transition-all border ${
                activeSubTab === "analytics" 
                  ? "bg-hust-red text-white border-hust-red" 
                  : "bg-white text-charcoal-ink border-whisper-border hover:bg-canvas-base"
              }`}
              onClick={() => setActiveSubTab("analytics")}
            >
              <BarChart2 className="w-3.5 h-3.5" />
              <span>Thống kê hiệu suất Reviewer</span>
            </button>
          </div>

          <button
            type="button"
            onClick={() => { setActiveSubTab("queue"); setSelectedDoc(null); }}
            className="flex items-center gap-1.5 text-xs text-muted-steel font-bold hover:text-hust-red transition-colors"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Giao diện Duyệt tài liệu</span>
          </button>
        </header>

        {/* Dynamic page container */}
        <div className="flex-1 overflow-hidden">
          {activeSubTab === "queue" ? (
            loadingQueue ? (
              <div className="flex flex-col items-center justify-center h-full p-8 text-center bg-white">
                <div className="w-10 h-10 border-4 border-hust-red border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-muted-steel text-sm font-semibold">Đang tải hàng đợi phê duyệt...</p>
              </div>
            ) : !selectedDoc ? (
              /* QUEUE LIST VIEW */
              <div className="p-6 h-full overflow-y-auto max-w-5xl mx-auto space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-whisper-border">
                  <h2 className="font-display font-extrabold text-[18px] text-charcoal-ink">Tài liệu đang chờ xử lý</h2>
                  <span className="text-xs text-muted-steel">Đã sắp xếp theo thời hạn SLA</span>
                </div>

                <div className="grid grid-cols-1 gap-3">
                  {queueDocs.map((doc) => (
                    <div 
                      key={doc.document_id}
                      className="tactile-card flex justify-between items-center bg-white border border-whisper-border hover:border-charcoal-ink transition-all cursor-pointer"
                      onClick={() => handleSelectDoc(doc)}
                    >
                      <div className="flex items-start gap-4">
                        <div className="bg-[#FFF8F6] border border-hust-red/10 rounded-xl p-2.5 shrink-0 text-hust-red">
                          <FileText className="w-6 h-6" />
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink hover:text-hust-red">
                              {doc.filename}
                            </h3>
                            <span className="bg-canvas-base border border-whisper-border rounded px-1.5 py-0.5 text-[10px] font-bold font-mono text-muted-steel">
                              {doc.course_code}
                            </span>
                          </div>
                          <p className="text-body-sm text-muted-steel mt-0.5">
                            Loại: {doc.document_tier} | Tải lên lúc: {new Date(doc.uploaded_at).toLocaleString()}
                          </p>
                          <div className="flex gap-2.5 mt-2">
                            <span className="text-[10px] font-bold uppercase text-pear-yellow bg-yellow-50 border border-pear-yellow/20 px-2 py-0.5 rounded">
                              {doc.status}
                            </span>
                            <span className="text-[10px] font-mono text-muted-steel flex items-center gap-1">
                              <Clock className="w-3 h-3" />
                              Hạn xử lý: {doc.sla_deadline ? new Date(doc.sla_deadline).toLocaleString() : "Không có"}
                            </span>
                          </div>
                        </div>
                      </div>

                      <button className="tactile-button text-xs flex items-center gap-1 py-2 px-3.5 bg-white">
                        <span>Chi tiết duyệt</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))}

                  {queueDocs.length === 0 && (
                    <div className="text-center py-16 bg-white border border-whisper-border rounded-2xl space-y-2">
                      <CheckCircle className="w-12 h-12 text-system-green mx-auto" />
                      <h3 className="text-body-lg font-bold text-charcoal-ink">Đã giải quyết sạch hàng đợi!</h3>
                      <p className="text-body-sm text-muted-steel">Không có tài liệu mới nào cần kiểm duyệt lúc này.</p>
                    </div>
                  )}
                </div>
              </div>
            ) : loadingDetail ? (
              <div className="flex flex-col items-center justify-center h-full p-8 text-center bg-white">
                <div className="w-10 h-10 border-4 border-hust-red border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-muted-steel text-sm font-semibold">Đang nạp dữ liệu kiểm duyệt và trích xuất OCR...</p>
              </div>
            ) : (
              /* 3-COLUMN DETAIL AUDIT COMPARISON VIEW */
              <div className="flex h-full overflow-hidden">
                
                {/* Column 1: Source & OCR Markdown (35% Width) */}
                <div className="w-[35%] border-r border-whisper-border bg-white flex flex-col overflow-hidden">
                  <header className="px-5 py-3 border-b border-whisper-border bg-canvas-base flex justify-between items-center shrink-0">
                    <span className="text-xs font-bold text-charcoal-ink uppercase tracking-wider font-display">Cột 1: Đối chiếu OCR</span>
                    <button 
                      className="text-xs text-muted-steel hover:text-charcoal-ink flex items-center gap-1 font-bold"
                      onClick={() => setSelectedDoc(null)}
                    >
                      <XCircle className="w-4 h-4" />
                      <span>Thoát</span>
                    </button>
                  </header>

                  <div className="flex-1 overflow-y-auto p-5 space-y-4">
                    <div className="border border-whisper-border rounded-xl p-4 bg-canvas-base space-y-2">
                      <span className="text-[10px] font-bold text-muted-steel block uppercase font-display">Tệp tin bản gốc</span>
                      <button
                        type="button"
                        onClick={openOriginalFile}
                        title="Mở tệp gốc trong tab mới"
                        className="w-full h-32 bg-slate-200 hover:bg-slate-300 border border-whisper-border rounded flex flex-col items-center justify-center p-3 text-center transition-colors cursor-pointer"
                      >
                        <FileText className="w-8 h-8 text-muted-steel mb-1" />
                        <span className="text-[11px] font-semibold text-charcoal-ink truncate max-w-full">{selectedDoc.filename}</span>
                        <span className="text-[10px] text-hust-red font-bold mt-1">Bấm để mở tệp gốc</span>
                      </button>
                    </div>

                    <div className="space-y-2">
                      <span className="text-[10px] font-bold text-system-green block uppercase font-display">Nội dung OCR trích xuất</span>
                      <div className="text-body-sm bg-white border border-whisper-border rounded-xl p-4">
                        <MarkdownRenderer content={selectedDoc.markdown_content || `# ${selectedDoc.title}\n\nĐang tiến hành trích xuất chữ viết tự động bằng mô hình AI Vision...`} />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Column 2: AI Evaluation & Justification Rationale (40% Width) */}
                <div className="w-[40%] border-r border-whisper-border bg-white flex flex-col overflow-hidden">
                  <header className="px-5 py-3 border-b border-whisper-border bg-canvas-base shrink-0">
                    <span className="text-xs font-bold text-charcoal-ink uppercase tracking-wider font-display">Cột 2: Đánh giá tự động của AI</span>
                  </header>

                  <div className="flex-1 overflow-y-auto p-5 space-y-5">
                    {/* Performance metrics charts scores */}
                    <div className="grid grid-cols-3 gap-3">
                      <div className="border border-whisper-border rounded-xl p-3 text-center bg-canvas-base">
                        <span className="block text-[10px] font-bold text-muted-steel uppercase">Liên quan</span>
                        <span className="block text-2xl font-black text-hust-red font-mono mt-1">
                          {Math.round(getScore("relevance") * 10)}%
                        </span>
                      </div>
                      <div className="border border-whisper-border rounded-xl p-3 text-center bg-canvas-base">
                        <span className="block text-[10px] font-bold text-muted-steel uppercase">Đầy đủ</span>
                        <span className="block text-2xl font-black text-hust-red font-mono mt-1">
                          {Math.round(getScore("completeness") * 10)}%
                        </span>
                      </div>
                      <div className="border border-whisper-border rounded-xl p-3 text-center bg-canvas-base">
                        <span className="block text-[10px] font-bold text-muted-steel uppercase">Chất lượng</span>
                        <span className="block text-2xl font-black text-hust-red font-mono mt-1">
                          {Math.round(getScore("quality") * 10)}%
                        </span>
                      </div>
                    </div>

                    {/* Plagiarism indicator */}
                    <div className="border border-whisper-border rounded-xl p-4 bg-canvas-base space-y-2">
                      <div className="flex justify-between text-xs font-bold text-charcoal-ink">
                        <span>Độ trùng lặp văn bản:</span>
                        <span className="text-system-green font-mono">{Math.round(getPlagiarismSimilarity() * 100)}%</span>
                      </div>
                      <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                        <div className="bg-system-green h-full" style={{ width: `${getPlagiarismSimilarity() * 100}%` }}></div>
                      </div>
                      <span className="block text-[10px] text-muted-steel">Kiểm định chống sao chép và trùng lặp.</span>
                    </div>

                    {/* Justification details block */}
                    <div className="space-y-3.5">
                      <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-widest font-display">Khối giải trình tự động:</span>
                      
                      <div className="space-y-2.5">
                        <div className="border border-whisper-border rounded-lg p-3 bg-white space-y-1">
                          <span className="block text-[11px] font-bold text-charcoal-ink">Tính liên quan (Relevance)</span>
                          <p className="text-xs text-muted-steel leading-relaxed">
                            {getJustification("relevance_rationale") || "Chưa có dữ liệu đánh giá."}
                          </p>
                        </div>

                        <div className="border border-whisper-border rounded-lg p-3 bg-white space-y-1">
                          <span className="block text-[11px] font-bold text-charcoal-ink">Độ đầy đủ văn bản (Completeness)</span>
                          <p className="text-xs text-muted-steel leading-relaxed">
                            {getJustification("completeness_rationale") || "Chưa có dữ liệu đánh giá."}
                          </p>
                        </div>

                        <div className="border border-whisper-border rounded-lg p-3 bg-white space-y-1">
                          <span className="block text-[11px] font-bold text-charcoal-ink font-display">Chất lượng trình bày (Quality)</span>
                          <p className="text-xs text-muted-steel leading-relaxed">
                            {getJustification("quality_rationale") || "Chưa có dữ liệu đánh giá."}
                          </p>
                        </div>

                        <div className="border border-hust-red/20 rounded-lg p-3 bg-[#FFF8F6] space-y-1">
                          <span className="block text-[11px] font-bold text-hust-red font-display">Đánh giá chung (AI Recommendation)</span>
                          <p className="text-xs text-charcoal-ink font-semibold leading-relaxed">
                            {getJustification("overall_rationale") ||
                              (getRecommendation()
                                ? `Hệ thống khuyến nghị: ${getRecommendation()}.`
                                : "Chưa có dữ liệu đánh giá.")}
                          </p>
                        </div>
                      </div>

                      {/* State logs audit history widget */}
                      <div className="border border-whisper-border rounded-xl p-4 bg-slate-50 space-y-3">
                        <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-wider font-display">Nhật ký kiểm định (Audit Trail)</span>
                        <div className="space-y-2">
                          {selectedDoc.state_logs.map((log: any, lIdx: number) => (
                            <div key={lIdx} className="text-xs border-b border-slate-100 pb-1.5">
                              <div className="flex justify-between font-semibold text-slate-800 text-[11px]">
                                <span>Trạng thái: {log.to_state}</span>
                                <span className="text-muted-steel font-mono">{new Date(log.transitioned_at).toLocaleDateString()}</span>
                              </div>
                              {log.note && <p className="text-[10px] text-slate-500 mt-0.5">Chú thích: {log.note}</p>}
                            </div>
                          ))}
                          {selectedDoc.state_logs.length === 0 && (
                            <p className="text-xs text-slate-400 italic">Không có lịch sử nhật ký kiểm duyệt.</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Column 3: Decision Approval & Comments (25% Width) */}
                <div className="w-[25%] bg-white flex flex-col overflow-hidden">
                  <header className="px-5 py-3 border-b border-whisper-border bg-canvas-base shrink-0">
                    <span className="text-xs font-bold text-charcoal-ink uppercase tracking-wider font-display">Cột 3: Phê duyệt của Reviewer</span>
                  </header>

                  <div className="flex-1 overflow-y-auto p-5 space-y-5 flex flex-col justify-between">
                    <div className="space-y-4">
                      <div>
                        <span className="text-[10px] font-bold text-muted-steel uppercase tracking-widest block mb-1">Tóm tắt tệp</span>
                        <h4 className="font-display font-extrabold text-body-lg text-charcoal-ink">{selectedDoc.title}</h4>
                        <span className="text-xs font-semibold text-muted-steel font-mono">{selectedDoc.filename}</span>
                      </div>

                      <div className="space-y-1.5">
                        <label className="block text-xs font-bold text-slate-600 uppercase tracking-wider font-display">Ý kiến duyệt học thuật</label>
                        <textarea 
                          className="w-full h-32 bg-canvas-base border border-whisper-border rounded-xl p-3 text-body-sm outline-none focus:ring-2 focus:ring-hust-red focus:border-hust-red transition-all"
                          placeholder="Nhập ghi chú ý kiến duyệt cho sinh viên hoặc giải trình lý do từ chối..."
                          value={reviewNote}
                          onChange={(e) => setReviewNote(e.target.value)}
                        />
                      </div>
                    </div>

                    <div className="space-y-2.5">
                      <button
                        className="tactile-button tactile-button-primary w-full py-3 flex items-center justify-center gap-1.5 disabled:opacity-60"
                        onClick={() => handleDecisionClick("APPROVED")}
                        disabled={deciding}
                      >
                        <CheckCircle className="w-4.5 h-4.5" />
                        <span>Phê duyệt tài liệu</span>
                      </button>
                      <button
                        className="tactile-button w-full py-3 border-system-red text-system-red flex items-center justify-center gap-1.5 bg-white disabled:opacity-60"
                        onClick={() => handleDecisionClick("REJECTED")}
                        disabled={deciding}
                      >
                        <XCircle className="w-4.5 h-4.5" />
                        <span>Từ chối tài liệu</span>
                      </button>
                    </div>
                  </div>
                </div>

              </div>
            )
          ) : (
            /* ANALYTICS DASHBOARD VIEW */
            <div className="p-6 h-full overflow-y-auto max-w-4xl mx-auto space-y-6">
              <div className="pb-3 border-b border-whisper-border flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h2 className="font-display font-extrabold text-[18px] text-charcoal-ink">Thống kê hiệu suất Subject Reviewer</h2>
                  <p className="text-body-sm text-muted-steel mt-0.5">Biểu đồ giám sát SLA và tỷ lệ ghi đè thuật toán.</p>
                </div>
                <button
                  onClick={handleExportCsv}
                  disabled={exporting}
                  className="tactile-button text-[12px] py-2 px-4 bg-white border border-whisper-border text-charcoal-ink flex items-center gap-2 disabled:opacity-60"
                >
                  <Download className="w-4 h-4" />
                  {exporting ? "Đang xuất..." : "Export CSV"}
                </button>
              </div>

              {analytics ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Average SLA time card */}
                  <div className="tactile-card bg-white space-y-4">
                    <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink flex items-center gap-1.5">
                      <Clock className="w-5 h-5 text-hust-red" />
                      <span>Thời gian giải quyết SLA tuần này</span>
                    </h3>
                    <p className="text-[11px] text-muted-steel leading-relaxed">
                      Thời gian trung bình từ lúc nộp đến lúc duyệt xong của mỗi môn trong tuần.
                      Màu đỏ: chạm hoặc vượt hạn SLA của môn; màu vàng: gần hạn (trên nửa ngưỡng); màu xanh: trong hạn.
                    </p>
                    <div className="space-y-3 pt-2">
                      {Object.entries(analytics.average_sla_hours_per_course).map(([courseCode, hours]) => {
                        const threshold = analytics.sla_threshold_hours_per_course[courseCode] ?? 48;
                        const breached = hours >= threshold;
                        return (
                        <div key={courseCode} className="space-y-1">
                          <div className="flex justify-between text-xs text-charcoal-ink">
                            <span>{courseCode}</span>
                            <span className="font-bold">
                              {hours.toFixed(1)} giờ {breached ? `(Vượt hạn SLA ${threshold}h)` : `(Trong hạn SLA ${threshold}h)`}
                            </span>
                          </div>
                          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                            <div
                              className={`h-full ${breached ? "bg-system-red" : hours > threshold / 2 ? "bg-pear-yellow" : "bg-system-green"}`}
                              style={{ width: `${Math.min(100, (hours / threshold) * 100)}%` }}
                            ></div>
                          </div>
                        </div>
                        );
                      })}
                      {Object.keys(analytics.average_sla_hours_per_course).length === 0 && (
                        <p className="text-xs text-muted-steel italic">Không có dữ liệu SLA của khóa học.</p>
                      )}
                    </div>
                  </div>

                  {/* AI override rate card */}
                  <div className="tactile-card bg-white space-y-4">
                    <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink flex items-center gap-1.5">
                      <ShieldAlert className="w-5 h-5 text-hust-red" />
                      <span>Tỷ lệ ghi đè thuật toán</span>
                    </h3>
                    <div className="flex justify-around items-center pt-2">
                      <div className="text-center">
                        <span className="block text-[32px] font-black text-charcoal-ink">
                          {(analytics.ai_override_rate * 100).toFixed(1)}%
                        </span>
                        <span className="block text-[10px] text-muted-steel uppercase">Tần suất trung bình</span>
                      </div>
                      <div className="text-center">
                        <span className="block text-[32px] font-black text-system-green">
                          {(analytics.ai_agreement_rate * 100).toFixed(1)}%
                        </span>
                        <span className="block text-[10px] text-muted-steel uppercase">Đồng thuận AI</span>
                      </div>
                    </div>
                    <p className="text-xs text-muted-steel text-center leading-relaxed">
                      Sự khác biệt phản ánh ý kiến chuyên môn học thuật thực tế để tái đào tạo và tối ưu hóa hệ thống.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 bg-white border border-whisper-border rounded-xl">
                  <p className="text-muted-steel text-sm">Không thể nạp dữ liệu thống kê hiệu suất.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* OVERRIDE MODAL DIALOG GATES */}
      {showOverrideModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[1px]">
          <div className="w-full max-w-[440px] bg-white border border-whisper-border rounded-2xl p-6 shadow-xl space-y-4 animate-in zoom-in-95 duration-100">
            <div className="flex items-start gap-3 text-pear-yellow">
              <AlertTriangle className="w-6 h-6 shrink-0 mt-0.5" />
              <div>
                <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink">Cảnh báo: Ghi đè quyết định AI</h3>
                <p className="text-xs text-muted-steel mt-1 leading-relaxed">
                  Bạn đang quyết định **TỪ CHỐI** một tài liệu được hệ thống tự động kiểm định với chất lượng rất tốt. Hệ thống yêu cầu cung cấp lý do giải trình.
                </p>
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">Lý do ghi đè bắt buộc</label>
              <textarea 
                className="w-full h-24 bg-canvas-base border border-whisper-border rounded-xl p-3 text-body-sm outline-none focus:ring-2 focus:ring-hust-red focus:border-hust-red"
                placeholder="Ví dụ: Tài liệu này bị lệch định dạng chương trình giảng dạy của viện SOICT HUST..."
                id="override-reason-text"
              />
            </div>

            <div className="flex gap-3 pt-2">
              <button 
                type="button" 
                className="tactile-button bg-white border border-whisper-border text-charcoal-ink flex-1 py-2"
                onClick={() => setShowOverrideModal(false)}
              >
                Hủy bỏ
              </button>
              <button
                type="button"
                className="tactile-button tactile-button-primary flex-1 py-2 bg-hust-red text-white disabled:opacity-60"
                disabled={deciding}
                onClick={() => {
                  const reasonEl = document.getElementById("override-reason-text") as HTMLTextAreaElement;
                  if (reasonEl && reasonEl.value.trim().length > 5) {
                    submitDecision(pendingDecision as any, reasonEl.value);
                  } else {
                    showToast("Vui lòng nhập lý do ghi đè hợp lệ (tối thiểu 5 ký tự)!", "error");
                  }
                }}
              >
                Xác nhận ghi đè
              </button>
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
