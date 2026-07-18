/* eslint-disable react-hooks/set-state-in-effect, @typescript-eslint/no-explicit-any, react-hooks/exhaustive-deps */
"use client";

import React, { useState, useEffect } from "react";
import AppShell from "../../components/app-shell";
import api from "../../lib/api";
import { useAsyncAction } from "../../lib/useAsyncAction";
import { useToast } from "../../components/toast";
import {
  UserCheck,
  AlertTriangle,
  RefreshCw,
  XCircle,
  Database,
  Info,
  Copy,
  RotateCcw
} from "lucide-react";

interface CourseRead {
  id: string;
  code: string;
  name: string;
  description: string | null;
  topic_summary: string | null;
  short_description: string | null;
  topic_tags: string[];
  review_sla_hours: number;
  is_active: boolean;
}

interface UserRead {
  id: string;
  email: string;
  role: string;
  full_name: string | null;
}

interface FailedDocumentEntry {
  document_id: string;
  original_filename: string;
  failure_reason: string | null;
  raw_failure_output: Record<string, any> | null;
  attempt_count: number;
  failed_at: string | null;
  job_type: string;
}

interface AssignmentUI {
  id: string;
  course_code: string;
  user_id: string;
  reviewer: string;
}

export default function AdminControlPanel() {
  const { showToast } = useToast();
  const [activeTab, setActiveTab] = useState<"seeds" | "assignments" | "dlq">("seeds");
  
  // Data states
  const [courses, setCourses] = useState<CourseRead[]>([]);
  const [reviewers, setReviewers] = useState<UserRead[]>([]);
  const [assignments, setAssignments] = useState<AssignmentUI[]>([]);
  const [dlqJobs, setDlqJobs] = useState<FailedDocumentEntry[]>([]);
  const [selectedJob, setSelectedJob] = useState<FailedDocumentEntry | null>(null);

  // Form states
  const [newCourseCodeSeed, setNewCourseCodeSeed] = useState("");
  const [newCourseNameSeed, setNewCourseNameSeed] = useState("");
  const [newCourseDescSeed, setNewCourseDescSeed] = useState("");
  const [newCourseSlaSeed, setNewCourseSlaSeed] = useState(48);

  const [assignCourseCode, setAssignCourseCode] = useState("");
  const [assignReviewerId, setAssignReviewerId] = useState("");

  // Create-reviewer modal states
  const [showCreateReviewer, setShowCreateReviewer] = useState(false);
  const [newReviewerName, setNewReviewerName] = useState("");
  const [newReviewerEmail, setNewReviewerEmail] = useState("");

  const [slaEdits, setSlaEdits] = useState<Record<string, number>>({});
  const [bulkSla, setBulkSla] = useState(48);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch initial data
  const fetchData = async () => {
    setIsLoading(true);
    try {
      const coursesRes = await api.get<CourseRead[]>("/courses");
      setCourses(coursesRes);

      const reviewersRes = await api.get<UserRead[]>("/admin/users?role=reviewer");
      setReviewers(reviewersRes);

      const dlqRes = await api.get<FailedDocumentEntry[]>("/admin/dead-letter");
      setDlqJobs(dlqRes);

      // Fetch reviewer assignments for all courses
      await fetchAssignments(coursesRes);
    } catch (err: any) {
      console.error("Error loading admin data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchAssignments = async (coursesList: CourseRead[]) => {
    try {
      const list: AssignmentUI[] = [];
      await Promise.all(
        coursesList.map(async (course) => {
          try {
            const res = await api.get<any[]>(`/courses/${course.code}/reviewers`);
            if (res && res.length > 0) {
              res.forEach((assignment) => {
                list.push({
                  id: assignment.id,
                  course_code: course.code,
                  user_id: assignment.user_id,
                  reviewer: assignment.reviewer_email || "Đã phân công",
                });
              });
            } else {
              list.push({
                id: `no-assign-${course.code}`,
                course_code: course.code,
                user_id: "",
                reviewer: "Chưa phân công",
              });
            }
          } catch (err) {
            console.error(`Failed to fetch reviewers for ${course.code}`, err);
            list.push({
              id: `no-assign-${course.code}`,
              course_code: course.code,
              user_id: "",
              reviewer: "Chưa phân công",
            });
          }
        })
      );
      // Sort by course code
      list.sort((a, b) => a.course_code.localeCompare(b.course_code));
      setAssignments(list);
    } catch (error) {
      console.error("Error building assignments list:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Create course seed helper
  const { pending: creatingSeed, run: handleCreateCourseSeed } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCourseCodeSeed.trim() || !newCourseNameSeed.trim()) return;

    try {
      const payload = {
        code: newCourseCodeSeed.trim().toUpperCase(),
        name: newCourseNameSeed.trim(),
        description: newCourseDescSeed.trim() || null,
        review_sla_hours: newCourseSlaSeed,
      };
      await api.post<CourseRead>("/courses", payload);
      showToast(`Đã khởi tạo môn học ${payload.code} thành công!`, "success");
      setNewCourseCodeSeed("");
      setNewCourseNameSeed("");
      setNewCourseDescSeed("");
      setNewCourseSlaSeed(48);
      
      // Refresh course list
      const updatedCourses = await api.get<CourseRead[]>("/courses");
      setCourses(updatedCourses);
      await fetchAssignments(updatedCourses);
    } catch (err: any) {
      showToast(`Lỗi khi tạo môn học: ${err.message}`, "error");
    }
  });

  // Update SLA helper
  const { pending: updatingSla, run: handleUpdateSla } = useAsyncAction(async (courseCode: string) => {
    const hours = slaEdits[courseCode];
    if (!hours || hours < 24 || hours > 72) {
      showToast("SLA phải nằm trong khoảng từ 24 đến 72 giờ.", "error");
      return;
    }

    try {
      await api.put(`/courses/${courseCode}/sla`, { sla_hours: hours });
      showToast(`Đã cập nhật SLA thành công cho môn ${courseCode} thành ${hours}h!`, "success");
      const updatedCourses = await api.get<CourseRead[]>("/courses");
      setCourses(updatedCourses);
    } catch (err: any) {
      showToast(`Lỗi khi cập nhật SLA: ${err.message}`, "error");
    }
  });

  // Bulk SLA helper — applies one default SLA to every loaded course via the existing endpoint
  const { pending: isBulkUpdating, run: handleBulkUpdateSla } = useAsyncAction(async () => {
    if (!bulkSla || bulkSla < 24 || bulkSla > 72) {
      showToast("SLA phải nằm trong khoảng từ 24 đến 72 giờ.", "error");
      return;
    }
    if (!confirm(`Đặt SLA mặc định ${bulkSla}h cho toàn bộ ${courses.length} học phần?`)) return;

    let failures = 0;
    await Promise.all(
      courses.map(async (course) => {
        try {
          await api.put(`/courses/${course.code}/sla`, { sla_hours: bulkSla });
        } catch (err) {
          console.error(`Failed to update SLA for ${course.code}`, err);
          failures++;
        }
      })
    );

    try {
      const updatedCourses = await api.get<CourseRead[]>("/courses");
      setCourses(updatedCourses);
    } catch (err) {
      console.error("Failed to refresh courses after bulk SLA update", err);
    }
    setSlaEdits({});

    if (failures === 0) {
      showToast(`Đã đặt SLA mặc định ${bulkSla}h cho toàn bộ ${courses.length} học phần!`, "success");
    } else {
      showToast(`Đã cập nhật SLA với ${failures}/${courses.length} học phần thất bại. Vui lòng thử lại.`, "error");
    }
  });

  // Assign Reviewer helper
  const { pending: addingAssignment, run: handleAddAssignment } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assignCourseCode || !assignReviewerId) {
      showToast("Vui lòng chọn cả mã học phần và Reviewer.", "error");
      return;
    }

    try {
      await api.post(`/courses/${assignCourseCode}/reviewers`, { user_id: assignReviewerId });
      showToast(`Đã gán Reviewer thành công cho môn ${assignCourseCode}!`, "success");
      setAssignCourseCode("");
      setAssignReviewerId("");
      await fetchAssignments(courses);
    } catch (err: any) {
      showToast(`Lỗi khi phân công Reviewer: ${err.message}`, "error");
    }
  });

  // Create Reviewer account helper
  const { pending: isCreatingReviewer, run: handleCreateReviewer } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReviewerName.trim() || !newReviewerEmail.trim()) {
      showToast("Vui lòng nhập đầy đủ họ tên và email.", "error");
      return;
    }

    try {
      await api.post<UserRead>("/admin/users", {
        full_name: newReviewerName.trim(),
        email: newReviewerEmail.trim(),
        password: "changeme123",
        role: "reviewer",
      });
      showToast(`Đã tạo tài khoản Reviewer cho ${newReviewerEmail.trim()} (mật khẩu mặc định: changeme123)!`, "success");
      setNewReviewerName("");
      setNewReviewerEmail("");
      setShowCreateReviewer(false);

      // Refresh reviewers so the new account appears in the assignment dropdown
      const reviewersRes = await api.get<UserRead[]>("/admin/users?role=reviewer");
      setReviewers(reviewersRes);
    } catch (err: any) {
      showToast(`Lỗi khi tạo Reviewer: ${err.message}`, "error");
    }
  });

  // Unassign Reviewer helper
  const { pending: unassigning, run: handleUnassignReviewer } = useAsyncAction(async (courseCode: string, userId: string) => {
    if (!userId) return;
    if (!confirm(`Bạn có chắc chắn muốn xóa phân công cho môn ${courseCode}?`)) return;

    try {
      await api.del(`/courses/${courseCode}/reviewers/${userId}`);
      showToast(`Đã xóa phân công Reviewer cho môn ${courseCode}!`, "success");
      await fetchAssignments(courses);
    } catch (err: any) {
      showToast(`Lỗi khi xóa phân công: ${err.message}`, "error");
    }
  });

  // DLQ Reprocess job helper
  const { pending: reprocessing, run: handleReprocessJob } = useAsyncAction(async (documentId: string, jobType: string) => {
    const fromState = jobType === "eval" ? "EVALUATING" : "PARSING";
    try {
      await api.post(`/admin/documents/${documentId}/reprocess`, { from_state: fromState });
      showToast(`Đã gửi lệnh Reprocess tái khởi chạy lại Document [${documentId}] thành công!`, "success");

      const dlqRes = await api.get<FailedDocumentEntry[]>("/admin/dead-letter");
      setDlqJobs(dlqRes);
      setSelectedJob(null);
    } catch (err: any) {
      showToast(`Lỗi khi thực hiện reprocess: ${err.message}`, "error");
    }
  });

  // Copy the raw failure log (JSON) or exception message to the clipboard
  const handleCopyLog = async (job: FailedDocumentEntry) => {
    const payload = job.raw_failure_output
      ? JSON.stringify(job.raw_failure_output, null, 2)
      : job.failure_reason || "";
    try {
      await navigator.clipboard.writeText(payload);
      showToast("Đã sao chép log lỗi vào clipboard.", "success");
    } catch {
      showToast("Không thể sao chép log lỗi.", "error");
    }
  };

  // Permanently delete job helper
  const { pending: markingFailed, run: handleMarkFailedJob } = useAsyncAction(async (documentId: string) => {
    if (!confirm("Bạn có chắc chắn muốn đánh dấu Document này thất bại vĩnh viễn?")) return;
    try {
      await api.post(`/admin/documents/${documentId}/mark-permanently-failed`);
      showToast(`Đã đánh dấu Document thất bại vĩnh viễn [${documentId}]!`, "success");

      const dlqRes = await api.get<FailedDocumentEntry[]>("/admin/dead-letter");
      setDlqJobs(dlqRes);
      setSelectedJob(null);
    } catch (err: any) {
      showToast(`Lỗi khi đánh dấu thất bại vĩnh viễn: ${err.message}`, "error");
    }
  });

  return (
    <AppShell>
      <div className="flex flex-col h-full bg-canvas-base overflow-hidden">
        
        {/* Sub-header navigation tabs */}
        <header className="flex bg-white border-b border-whisper-border px-6 py-2.5 shrink-0 justify-between items-center">
          <div className="flex gap-1.5">
            <button 
              className={`flex items-center gap-1.5 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-all ${
                activeTab === "seeds" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
              }`}
              onClick={() => setActiveTab("seeds")}
            >
              <Database className="w-4 h-4" />
              <span>Cấu hình Course Seeds & SLA</span>
            </button>
            <button 
              className={`flex items-center gap-1.5 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-all ${
                activeTab === "assignments" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
              }`}
              onClick={() => setActiveTab("assignments")}
            >
              <UserCheck className="w-4 h-4" />
              <span>Phân công Reviewer</span>
            </button>
            <button 
              className={`flex items-center gap-1.5 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-all ${
                activeTab === "dlq" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
              }`}
              onClick={() => setActiveTab("dlq")}
            >
              <AlertTriangle className="w-4 h-4" />
              <span>Hàng đợi lỗi DLQ ({dlqJobs.length})</span>
            </button>
          </div>
          <div className="text-xs font-display font-extrabold text-charcoal-ink bg-slate-100 px-3 py-1 rounded-full border border-whisper-border">
            HUST ADMIN DASHBOARD
          </div>
        </header>

        {/* Workspace Canvas tab sections */}
        <div className="flex-1 overflow-hidden relative">
          
          {isLoading ? (
            <div className="flex items-center justify-center h-full">
              <div className="flex flex-col items-center gap-3">
                <RefreshCw className="w-8 h-8 text-hust-red animate-spin" />
                <p className="text-body-sm font-semibold text-muted-steel">Đang tải dữ liệu cấu hình...</p>
              </div>
            </div>
          ) : (
            <>
              {/* TAB 1: SEEDS & SLA CONFIG */}
              {activeTab === "seeds" && (
                <div className="p-6 h-full overflow-y-auto max-w-4xl mx-auto space-y-6 animate-in fade-in duration-200">
                  <div className="pb-3 border-b border-whisper-border">
                    <h2 className="font-display font-extrabold text-[18px] text-charcoal-ink">Quản lý Học phần và SLA mặc định</h2>
                    <p className="text-body-sm text-muted-steel mt-0.5">Khởi tạo các mã học phần và thời hạn kiểm duyệt (SLA).</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="md:col-span-2 space-y-4">
                      <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink">Học phần HUST đang kích hoạt ({courses.length} môn)</h3>

                      {/* Bulk default SLA control */}
                      <div className="border border-whisper-border rounded-xl p-4 bg-canvas-base flex flex-wrap items-end gap-3">
                        <div className="flex flex-col">
                          <label className="text-[9px] font-bold text-muted-steel uppercase mb-0.5">SLA mặc định (Giờ)</label>
                          <input
                            type="number"
                            min={24}
                            max={72}
                            value={bulkSla}
                            onChange={(e) => setBulkSla(parseInt(e.target.value) || 24)}
                            className="w-20 bg-white border border-whisper-border rounded p-1.5 text-xs font-bold text-center"
                          />
                        </div>
                        <button
                          onClick={handleBulkUpdateSla}
                          disabled={isBulkUpdating}
                          className="tactile-button tactile-button-primary text-xs py-2 px-3 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          {isBulkUpdating ? "Đang cập nhật..." : "Đặt SLA mặc định cho tất cả"}
                        </button>
                        <span className="text-[11px] text-muted-steel leading-relaxed flex-1 min-w-[160px]">
                          Áp dụng cùng một giá trị SLA cho toàn bộ {courses.length} học phần đang kích hoạt.
                        </span>
                      </div>

                      <div className="grid grid-cols-1 gap-2.5 max-h-[400px] overflow-y-auto pr-2">
                        {courses.map(course => (
                          <div key={course.id} className="border border-whisper-border rounded-xl p-4 bg-white flex justify-between items-center shadow-sm">
                            <div className="min-w-0 pr-4">
                              <span className="font-mono font-bold text-hust-red block text-xs">{course.code}</span>
                              <span className="font-display font-extrabold text-body-md text-charcoal-ink truncate block">{course.name}</span>
                              <span className="text-[10px] text-muted-steel block truncate mt-0.5">{course.description || "Chưa có mô tả"}</span>
                            </div>
                            <div className="flex items-center gap-2 shrink-0">
                              <div className="flex flex-col items-end">
                                <label className="text-[9px] font-bold text-muted-steel uppercase mb-0.5">SLA (Giờ)</label>
                                <input
                                  type="number"
                                  min={24}
                                  max={72}
                                  value={slaEdits[course.code] ?? course.review_sla_hours}
                                  onChange={(e) => setSlaEdits({ ...slaEdits, [course.code]: parseInt(e.target.value) || 24 })}
                                  className="w-16 bg-canvas-base border border-whisper-border rounded p-1 text-xs font-bold text-center"
                                />
                              </div>
                              <button
                                onClick={() => handleUpdateSla(course.code)}
                                disabled={updatingSla}
                                className="text-xs bg-hust-red text-white px-2.5 py-1.5 rounded font-bold hover:bg-red-700 transition disabled:opacity-60"
                              >
                                Lưu
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="tactile-card bg-white h-fit space-y-4">
                      <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink">Thêm Seed Học phần mới</h3>
                      <form onSubmit={handleCreateCourseSeed} className="space-y-4">
                        <div className="space-y-1">
                          <label className="block text-xs font-bold text-muted-steel uppercase">Mã lớp/Học phần</label>
                          <input 
                            type="text" 
                            className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md" 
                            placeholder="Ví dụ: IT4062" 
                            value={newCourseCodeSeed}
                            onChange={(e) => setNewCourseCodeSeed(e.target.value)}
                            required 
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="block text-xs font-bold text-muted-steel uppercase">Tên học phần</label>
                          <input 
                            type="text" 
                            className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md" 
                            placeholder="Ví dụ: Lập trình mạng" 
                            value={newCourseNameSeed}
                            onChange={(e) => setNewCourseNameSeed(e.target.value)}
                            required 
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="block text-xs font-bold text-muted-steel uppercase">Mô tả học phần</label>
                          <textarea 
                            className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md h-20 resize-none" 
                            placeholder="Mô tả tóm tắt môn học..." 
                            value={newCourseDescSeed}
                            onChange={(e) => setNewCourseDescSeed(e.target.value)}
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="block text-xs font-bold text-muted-steel uppercase">SLA Phê duyệt (Giờ)</label>
                          <input 
                            type="number" 
                            min={24} 
                            max={72} 
                            className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md" 
                            value={newCourseSlaSeed}
                            onChange={(e) => setNewCourseSlaSeed(parseInt(e.target.value) || 48)}
                          />
                        </div>
                        <button className="tactile-button tactile-button-primary w-full py-2.5 disabled:opacity-60" type="submit" disabled={creatingSeed}>
                          Khởi tạo môn học
                        </button>
                      </form>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: REVIEWER ASSIGNMENTS GRID */}
              {activeTab === "assignments" && (
                <div className="p-6 h-full overflow-y-auto max-w-4xl mx-auto space-y-6 animate-in fade-in duration-200">
                  <div className="pb-3 border-b border-whisper-border">
                    <h2 className="font-display font-extrabold text-[18px] text-charcoal-ink">Phân công Subject Reviewer</h2>
                    <p className="text-body-sm text-muted-steel mt-0.5">Phân quyền giảng viên / trợ giảng chịu trách nhiệm kiểm duyệt cho từng khóa học.</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="md:col-span-2 space-y-4">
                      <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink">Phân công hiện tại</h3>
                      <div className="border border-whisper-border rounded-xl overflow-hidden bg-white shadow-sm">
                        <table className="w-full text-left text-body-sm">
                          <thead className="bg-canvas-base border-b border-whisper-border text-muted-steel font-bold uppercase tracking-wider text-[10px]">
                            <tr>
                              <th className="p-3">Môn học</th>
                              <th className="p-3">Reviewer đảm nhiệm</th>
                              <th className="p-3 text-right">Hành động</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-whisper-border">
                            {assignments.map(a => (
                              <tr key={a.id}>
                                <td className="p-3 font-mono font-bold">{a.course_code}</td>
                                <td className="p-3">
                                  <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                                    a.reviewer === "Chưa phân công" ? "bg-red-50 text-system-red border border-system-red/20" : "text-charcoal-ink"
                                  }`}>
                                    {a.reviewer}
                                  </span>
                                </td>
                                <td className="p-3 text-right font-display font-extrabold text-body-sm">
                                  {a.user_id ? (
                                    <button
                                      className="text-hust-red hover:underline text-xs font-bold disabled:opacity-60"
                                      onClick={() => handleUnassignReviewer(a.course_code, a.user_id)}
                                      disabled={unassigning}
                                    >
                                      Xóa phân công
                                    </button>
                                  ) : (
                                    <span className="text-muted-steel text-xs font-normal">N/A</span>
                                  )}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    <div className="tactile-card bg-white h-fit space-y-4">
                      <h3 className="font-display font-extrabold text-body-lg text-charcoal-ink">Cập nhật phân công</h3>
                      <form onSubmit={handleAddAssignment} className="space-y-4">
                        <div className="space-y-1">
                          <label className="block text-xs font-bold text-muted-steel uppercase">Mã học phần</label>
                          <select 
                            className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md"
                            value={assignCourseCode}
                            onChange={(e) => setAssignCourseCode(e.target.value)}
                            required
                          >
                            <option value="">-- Chọn mã môn học --</option>
                            {courses.map(c => (
                              <option key={c.id} value={c.code}>{c.code} - {c.name}</option>
                            ))}
                          </select>
                        </div>

                        <div className="space-y-1">
                          <label className="block text-xs font-bold text-muted-steel uppercase">Reviewer phân công</label>
                          <select 
                            className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md"
                            value={assignReviewerId}
                            onChange={(e) => setAssignReviewerId(e.target.value)}
                            required
                          >
                            <option value="">-- Chọn reviewer --</option>
                            {reviewers.map(user => (
                              <option key={user.id} value={user.id}>{user.full_name || user.email} ({user.email})</option>
                            ))}
                          </select>
                          <button
                            type="button"
                            className="text-xs font-bold text-hust-red hover:underline mt-1"
                            onClick={() => setShowCreateReviewer(true)}
                          >
                            + Tạo tài khoản Reviewer mới
                          </button>
                        </div>

                        <button className="tactile-button tactile-button-primary w-full py-2.5 animate-pulse-slow disabled:opacity-60" type="submit" disabled={addingAssignment}>
                          Cập nhật Reviewer
                        </button>
                      </form>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 3: DEAD-LETTER QUEUE (DLQ) LIST */}
              {activeTab === "dlq" && (
                <div className="p-6 h-full overflow-y-auto max-w-4xl mx-auto space-y-6 animate-in fade-in duration-200">
                  <div className="pb-3 border-b border-whisper-border">
                    <h2 className="font-display font-extrabold text-[18px] text-charcoal-ink">Dead-Letter Queue (DLQ) Monitor</h2>
                    <p className="text-body-sm text-muted-steel mt-0.5">Hàng đợi xử lý lỗi nền (OCR, Đánh giá, Index). Xem lịch sử vết chạy và khôi phục.</p>
                  </div>

                  {dlqJobs.length === 0 ? (
                    <div className="text-center py-16 bg-white border border-whisper-border rounded-2xl">
                      <Info className="w-12 h-12 text-system-green mx-auto mb-2" />
                      <h3 className="text-body-lg font-bold text-charcoal-ink">Không có lỗi nền nào</h3>
                      <p className="text-body-sm text-muted-steel">Tất cả các job xử lý tài liệu nền đều chạy mượt mà.</p>
                    </div>
                  ) : (
                    <div className="border border-whisper-border rounded-2xl overflow-hidden bg-white shadow-sm">
                      <div className="overflow-x-auto">
                        <table className="w-full text-left text-body-sm">
                          <thead className="bg-canvas-base border-b border-whisper-border text-muted-steel font-bold uppercase tracking-wider text-[10px]">
                            <tr>
                              <th className="p-3">Loại</th>
                              <th className="p-3">Tệp / Document</th>
                              <th className="p-3">Lỗi</th>
                              <th className="p-3 whitespace-nowrap">Thất bại lúc</th>
                              <th className="p-3 text-center">Số lần thử</th>
                              <th className="p-3 text-right">Thao tác</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-whisper-border">
                            {dlqJobs.map(job => (
                              <tr key={job.document_id} className="hover:bg-red-50/20 transition-colors">
                                <td className="p-3">
                                  <span className="bg-system-red text-white text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded">
                                    {job.job_type}
                                  </span>
                                </td>
                                <td className="p-3">
                                  <span className="block font-mono text-xs text-charcoal-ink truncate max-w-[220px]" title={job.original_filename}>
                                    {job.original_filename}
                                  </span>
                                  <span className="block font-mono text-[10px] text-muted-steel truncate max-w-[220px]" title={job.document_id}>
                                    {job.document_id}
                                  </span>
                                </td>
                                <td className="p-3">
                                  <span className="block text-xs text-system-red font-semibold truncate max-w-[300px]" title={job.failure_reason || ""}>
                                    {job.failure_reason || "Không có thông tin chi tiết lỗi."}
                                  </span>
                                </td>
                                <td className="p-3 text-[11px] text-muted-steel font-mono whitespace-nowrap">
                                  {job.failed_at ? new Date(job.failed_at).toLocaleString("vi-VN") : "N/A"}
                                </td>
                                <td className="p-3 text-center font-bold text-charcoal-ink">{job.attempt_count}</td>
                                <td className="p-3">
                                  <div className="flex items-center justify-end gap-1.5">
                                    <button
                                      title="Xem vết chi tiết"
                                      onClick={() => setSelectedJob(job)}
                                      className="inline-flex items-center justify-center h-8 w-8 rounded-lg border border-whisper-border bg-white text-muted-steel hover:bg-charcoal-ink hover:text-white transition-all"
                                    >
                                      <AlertTriangle className="h-4 w-4" />
                                    </button>
                                    <button
                                      title="Copy log lỗi"
                                      onClick={() => handleCopyLog(job)}
                                      className="inline-flex items-center justify-center h-8 w-8 rounded-lg border border-whisper-border bg-white text-muted-steel hover:bg-charcoal-ink hover:text-white transition-all"
                                    >
                                      <Copy className="h-4 w-4" />
                                    </button>
                                    <button
                                      title="Thử lại (Retry Job)"
                                      onClick={() => handleReprocessJob(job.document_id, job.job_type)}
                                      disabled={reprocessing}
                                      className="inline-flex items-center justify-center h-8 w-8 rounded-lg border border-hust-red/20 bg-[#FFF8F6] text-hust-red hover:bg-hust-red hover:text-white transition-all disabled:opacity-60"
                                    >
                                      <RotateCcw className="h-4 w-4" />
                                    </button>
                                  </div>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* DLQ DETAIL DRAWER INTERACTION */}
              {selectedJob && (
                <div className="fixed inset-0 z-50 bg-black/45 backdrop-blur-[1px] flex justify-end">
                  <div className="w-full max-w-md bg-white h-full shadow-2xl p-6 flex flex-col justify-between overflow-y-auto animate-in slide-in-from-right duration-200">
                    <div className="space-y-5">
                      <div className="flex justify-between items-center pb-2 border-b border-whisper-border">
                        <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink flex items-center gap-1.5">
                          <AlertTriangle className="w-5 h-5 text-hust-red" />
                          <span>Vết chạy chi tiết DLQ Job</span>
                        </h3>
                        <button onClick={() => setSelectedJob(null)}>
                          <XCircle className="w-6 h-6 text-muted-steel" />
                        </button>
                      </div>

                      <div className="space-y-3">
                        <div>
                          <span className="text-[10px] font-bold text-muted-steel uppercase block">Tệp tin bị lỗi</span>
                          <span className="text-body-sm font-semibold text-charcoal-ink font-mono">{selectedJob.original_filename}</span>
                        </div>
                        <div>
                          <span className="text-[10px] font-bold text-muted-steel uppercase block">Mã Document ID</span>
                          <span className="text-body-sm font-bold text-hust-red font-mono">{selectedJob.document_id}</span>
                        </div>
                        <div>
                          <span className="text-[10px] font-bold text-muted-steel uppercase block">Ngoại lệ (Exception message)</span>
                          <p className="text-xs text-system-red bg-red-50/40 border border-system-red/20 rounded p-2.5 font-mono leading-relaxed mt-1">
                            {selectedJob.failure_reason || "Không có thông tin chi tiết lỗi."}
                          </p>
                        </div>
                      </div>

                      {/* Visual list step history trace */}
                      {selectedJob.raw_failure_output && (
                        <div className="space-y-3">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold text-charcoal-ink uppercase block tracking-wider font-display">Thông tin thô (Raw Failure Output)</span>
                            <button
                              onClick={() => handleCopyLog(selectedJob)}
                              className="inline-flex items-center gap-1.5 text-[11px] font-bold text-hust-red hover:underline"
                            >
                              <Copy className="h-3.5 w-3.5" /> Copy log
                            </button>
                          </div>
                          <pre className="border border-whisper-border rounded-xl p-4 text-xs font-mono bg-canvas-base overflow-x-auto max-h-[300px]">
                            {JSON.stringify(selectedJob.raw_failure_output, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>

                    <div className="flex gap-3 pt-6 border-t border-whisper-border mt-6">
                      <button
                        className="tactile-button bg-white text-system-red border border-system-red/20 hover:bg-red-50/20 flex-1 py-2 font-bold disabled:opacity-60"
                        onClick={() => handleMarkFailedJob(selectedJob.document_id)}
                        disabled={markingFailed}
                      >
                        Xóa vĩnh viễn Job
                      </button>
                      <button
                        className="tactile-button tactile-button-primary flex-1 py-2 bg-hust-red text-white font-bold disabled:opacity-60"
                        onClick={() => handleReprocessJob(selectedJob.document_id, selectedJob.job_type)}
                        disabled={reprocessing}
                      >
                        Thử lại ngay
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {/* CREATE REVIEWER MODAL */}
          {showCreateReviewer && (
            <div className="fixed inset-0 z-50 bg-black/45 backdrop-blur-[1px] flex items-center justify-center p-4">
              <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-6 space-y-5 animate-in fade-in zoom-in duration-200">
                <div className="flex justify-between items-center pb-2 border-b border-whisper-border">
                  <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink flex items-center gap-1.5">
                    <UserCheck className="w-5 h-5 text-hust-red" />
                    <span>Tạo tài khoản Reviewer</span>
                  </h3>
                  <button onClick={() => setShowCreateReviewer(false)}>
                    <XCircle className="w-6 h-6 text-muted-steel" />
                  </button>
                </div>

                <form onSubmit={handleCreateReviewer} className="space-y-4">
                  <div className="space-y-1">
                    <label className="block text-xs font-bold text-muted-steel uppercase">Họ và tên</label>
                    <input
                      type="text"
                      className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md"
                      value={newReviewerName}
                      onChange={(e) => setNewReviewerName(e.target.value)}
                      placeholder="Ví dụ: Nguyễn Thị Linh"
                      required
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="block text-xs font-bold text-muted-steel uppercase">Email</label>
                    <input
                      type="email"
                      className="w-full bg-canvas-base border border-whisper-border rounded-xl p-2.5 text-body-md"
                      value={newReviewerEmail}
                      onChange={(e) => setNewReviewerEmail(e.target.value)}
                      placeholder="Ví dụ: reviewer@soict.hust.edu.vn"
                      required
                    />
                  </div>

                  <p className="text-[10px] text-muted-steel font-medium">
                    Mật khẩu mặc định là &quot;changeme123&quot;. Reviewer sẽ đổi mật khẩu khi đăng nhập lần đầu.
                  </p>

                  <div className="flex gap-3 pt-2">
                    <button
                      type="button"
                      className="tactile-button bg-white border border-whisper-border flex-1 py-2 font-bold"
                      onClick={() => setShowCreateReviewer(false)}
                    >
                      Hủy
                    </button>
                    <button
                      type="submit"
                      disabled={isCreatingReviewer}
                      className="tactile-button tactile-button-primary flex-1 py-2 font-bold disabled:opacity-60"
                    >
                      {isCreatingReviewer ? "Đang tạo..." : "Tạo tài khoản"}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

        </div>
      </div>
    </AppShell>
  );
}
