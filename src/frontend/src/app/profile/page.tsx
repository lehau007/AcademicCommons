/* eslint-disable react-hooks/set-state-in-effect */
"use client";

import React, { useState, useEffect } from "react";
import AppShell from "../../components/app-shell";
import api from "../../lib/api";
import { RefreshCw, Trophy, Award, BookOpen, User, Info } from "lucide-react";

interface UserRead {
  id: string;
  email: string;
  role: string;
  full_name: string | null;
}

interface CourseScore {
  course_id: string;
  course_code: string;
  points: number;
  rank: number;
}

interface ContributionScoreResponse {
  user_id: string;
  courses: CourseScore[];
  global_rank: number | null;
  total_points: number;
}

export default function ProfilePage() {
  const [activeTab, setActiveTab] = useState<"contributions" | "settings">("contributions");
  const [user, setUser] = useState<UserRead | null>(null);
  const [scoreData, setScoreData] = useState<ContributionScoreResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  const fetchProfileData = async () => {
    setIsLoading(true);
    try {
      const me = await api.get<UserRead>("/auth/me");
      setUser(me);
      
      const score = await api.get<ContributionScoreResponse>("/users/me/contribution-score");
      setScoreData(score);
    } catch (err) {
      console.error("Error loading profile data:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProfileData();
  }, []);

  // Fallback / earned badges mock collection
  const badges = [
    { id: "b1", name: "Đăng Học Thuật", desc: "Tải lên tài liệu hợp lệ đầu tiên", icon: "Award", earned: true, color: "bg-hust-red text-white" },
    { id: "b2", name: "Chiến binh OCR", desc: "Đóng góp tài liệu đã qua xử lý OCR thành công", icon: "BookOpen", earned: true, color: "bg-emerald-600 text-white" },
    { id: "b3", name: "Thẩm định viên", desc: "Tham gia đánh giá chất lượng tài liệu học tập", icon: "Settings", earned: false, color: "bg-slate-200 text-slate-400" },
    { id: "b4", name: "Thượng Nghị Sĩ", desc: "Đạt Top 5 bảng xếp hạng học kỳ", icon: "Trophy", earned: (scoreData?.total_points || 0) > 100, color: (scoreData?.total_points || 0) > 100 ? "bg-amber-500 text-white" : "bg-slate-200 text-slate-400" },
  ];

  return (
    <AppShell>
      <div className="space-y-6">
        
        {isLoading ? (
          <div className="flex items-center justify-center py-20 bg-white border border-whisper-border rounded-2xl shadow-sm">
            <div className="flex flex-col items-center gap-3">
              <RefreshCw className="w-8 h-8 text-hust-red animate-spin" />
              <p className="text-body-sm font-semibold text-muted-steel">Đang tải hồ sơ sinh viên...</p>
            </div>
          </div>
        ) : (
          <>
            {/* Profile Card Header */}
            <div className="bg-white border border-whisper-border rounded-2xl p-6 md:p-8 shadow-sm flex flex-col md:flex-row items-center md:items-start gap-6 relative animate-in fade-in duration-200">
              <div className="w-20 h-20 rounded-full bg-hust-red/10 text-hust-red font-black text-2xl flex items-center justify-center border-2 border-whisper-border select-none">
                {user?.full_name ? user.full_name.split(" ").slice(-1)[0].substring(0, 2).toUpperCase() : "US"}
              </div>
              
              <div className="flex-1 text-center md:text-left space-y-2">
                <div>
                  <h2 className="text-xl font-black text-slate-900">{user?.full_name || "Sinh viên HUST"}</h2>
                  <p className="text-xs text-muted-steel font-label-mono font-semibold uppercase">
                    Quyền hạn: {user?.role} | ID: {user?.id.substring(0, 8)}...
                  </p>
                </div>
                <p className="text-xs text-slate-600 font-semibold max-w-lg leading-relaxed">
                  Thành viên tích cực của cộng đồng số hóa tri thức học tập HUST. Đóng góp bài tập, đề thi, slide và ghi chép học tập chất lượng cao để cùng xây dựng kho tài nguyên học thuật SOICT.
                </p>
                
                {/* Quick stats badges */}
                <div className="flex flex-wrap gap-4 justify-center md:justify-start pt-2">
                  <span className="text-[11px] font-bold text-hust-red bg-red-50 px-3 py-1 rounded-lg border border-red-100 flex items-center gap-1">
                    <Trophy className="w-3.5 h-3.5" />
                    {scoreData?.total_points || 0} Điểm tích lũy (Points)
                  </span>
                  <span className="text-[11px] font-bold text-slate-700 bg-slate-100 px-3 py-1 rounded-lg border border-whisper-border flex items-center gap-1">
                    <Award className="w-3.5 h-3.5" />
                    Hạng {scoreData?.global_rank ? `#${scoreData.global_rank}` : "N/A"} toàn cầu
                  </span>
                </div>
              </div>
            </div>

            {/* Tab Selection */}
            <div className="flex border-b border-whisper-border">
              <button
                onClick={() => setActiveTab("contributions")}
                className={`pb-3 px-4 text-xs font-bold border-b-2 transition-all ${
                  activeTab === "contributions"
                    ? "border-hust-red text-hust-red"
                    : "border-transparent text-muted-steel hover:text-slate-700"
                }`}
              >
                Thành tựu & Huy hiệu
              </button>
              <button
                onClick={() => setActiveTab("settings")}
                className={`pb-3 px-4 text-xs font-bold border-b-2 transition-all ${
                  activeTab === "settings"
                    ? "border-hust-red text-hust-red"
                    : "border-transparent text-muted-steel hover:text-slate-700"
                }`}
              >
                Cài đặt tài khoản
              </button>
            </div>

            {/* Content sections */}
            {activeTab === "contributions" ? (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                
                {/* Badges Panel (8 columns) */}
                <div className="lg:col-span-8 bg-white border border-whisper-border rounded-2xl p-6 shadow-sm space-y-6">
                  <div>
                    <h3 className="font-headline-md text-sm font-black text-slate-900">Bộ sưu tập huy hiệu</h3>
                    <p className="text-[10px] text-muted-steel font-semibold">
                      Tự động mở khóa khi bạn chia sẻ tài liệu và nhận lượt bình chọn từ cộng đồng.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {badges.map((badge) => (
                      <div
                        key={badge.id}
                        className={`border border-whisper-border rounded-xl p-4 flex gap-4 transition-all ${
                          badge.earned ? "bg-white" : "bg-slate-50/50 opacity-70"
                        }`}
                      >
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${badge.color}`}>
                          {badge.icon === "Trophy" && <Trophy className="w-6 h-6" />}
                          {badge.icon === "Award" && <Award className="w-6 h-6" />}
                          {badge.icon === "BookOpen" && <BookOpen className="w-6 h-6" />}
                          {badge.icon === "Settings" && <User className="w-6 h-6" />}
                        </div>
                        <div className="space-y-1">
                          <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                            {badge.name}
                            {!badge.earned && (
                              <span className="text-[9px] bg-slate-100 text-slate-500 font-bold px-1.5 py-0.5 rounded">
                                Khóa
                              </span>
                            )}
                          </h4>
                          <p className="text-[10px] text-slate-500 font-semibold leading-relaxed">
                            {badge.desc}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Dynamic course breakdown list */}
                  {scoreData?.courses && scoreData.courses.length > 0 && (
                    <div className="pt-4 border-t border-whisper-border space-y-3">
                      <div>
                        <h4 className="font-headline-md text-xs font-black text-slate-900">Chi tiết đóng góp theo môn học</h4>
                        <p className="text-[9px] text-muted-steel font-semibold">Số điểm tích lũy và thứ hạng của bạn trong từng học phần HUST</p>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {scoreData.courses.map(cs => (
                          <div key={cs.course_id} className="border border-whisper-border rounded-xl p-3 bg-slate-50/50 flex justify-between items-center">
                            <div>
                              <span className="font-mono font-bold text-hust-red block text-xs">{cs.course_code}</span>
                              <span className="text-[10px] text-muted-steel font-bold">Thứ hạng đóng góp: #{cs.rank}</span>
                            </div>
                            <span className="text-xs font-extrabold text-slate-800 bg-white border border-whisper-border px-2.5 py-1 rounded-lg">
                              +{cs.points} Points
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Info / instructions panel (4 columns) */}
                <div className="lg:col-span-4 bg-white border border-whisper-border rounded-2xl p-6 shadow-sm space-y-4">
                  <div>
                    <h3 className="font-headline-md text-sm font-black text-slate-900">Quy tắc cộng điểm</h3>
                    <p className="text-[10px] text-muted-steel font-semibold">Cơ chế tính XP & Contribution score</p>
                  </div>
                  <div className="space-y-3.5 text-xs text-slate-700 leading-relaxed font-medium">
                    <div className="flex gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-hust-red mt-1.5 shrink-0" />
                      <p><strong>+10 XP:</strong> Mỗi khi bạn tải lên tài liệu học thuật (Slide, Đề thi, Bài tập) được Subject Reviewer duyệt hợp lệ.</p>
                    </div>
                    <div className="flex gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-hust-red mt-1.5 shrink-0" />
                      <p><strong>+2 XP / Upvote:</strong> Nhận thêm điểm khi sinh viên khác Upvote tài liệu hữu ích của bạn trên course page.</p>
                    </div>
                    <div className="flex gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-hust-red mt-1.5 shrink-0" />
                      <p><strong>-2 XP / Downvote:</strong> Bị trừ điểm nếu tài liệu của bạn nhận phản hồi không tốt hoặc nội dung cũ.</p>
                    </div>
                    <div className="bg-red-50/40 border border-hust-red/20 rounded-xl p-3 text-[11px] text-hust-red font-semibold flex items-start gap-1.5 mt-2">
                      <Info className="w-4 h-4 shrink-0 mt-0.5" />
                      <span>Vi phạm tải lên tài liệu rác hoặc sai môn học nhiều lần có thể bị khóa quyền đóng góp tài liệu cộng đồng.</span>
                    </div>
                  </div>
                </div>

              </div>
            ) : (
              /* Profile Settings Form */
              <div className="max-w-2xl bg-white border border-whisper-border rounded-2xl p-6 md:p-8 shadow-sm space-y-6 animate-in fade-in duration-200">
                <div>
                  <h3 className="font-headline-md text-sm font-black text-slate-900">Thông tin tài khoản</h3>
                  <p className="text-[10px] text-muted-steel font-semibold">Chi tiết định danh sinh viên được đăng ký trên hệ thống</p>
                </div>
                
                <form onSubmit={(e) => e.preventDefault()} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="block text-xs font-bold text-slate-600">Họ và tên</label>
                      <input
                        type="text"
                        defaultValue={user?.full_name || ""}
                        disabled
                        className="w-full bg-slate-50 border border-whisper-border rounded-xl px-4 py-2.5 text-xs font-semibold outline-none cursor-not-allowed opacity-80"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="block text-xs font-bold text-slate-600">Vai trò người dùng</label>
                      <input
                        type="text"
                        disabled
                        defaultValue={user?.role.toUpperCase() || ""}
                        className="w-full bg-slate-50 border border-whisper-border rounded-xl px-4 py-2.5 text-xs font-semibold outline-none cursor-not-allowed opacity-80"
                      />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="block text-xs font-bold text-slate-600">Email (Tài khoản HUST)</label>
                    <input
                      type="email"
                      disabled
                      defaultValue={user?.email || ""}
                      className="w-full bg-slate-50 border border-whisper-border rounded-xl px-4 py-2.5 text-xs font-semibold outline-none cursor-not-allowed opacity-80"
                    />
                  </div>

                  <div className="bg-slate-50 rounded-xl p-4 border border-whisper-border">
                    <h4 className="text-xs font-bold text-slate-800 mb-1 flex items-center gap-1.5">
                      <Info className="w-4 h-4 text-muted-steel" />
                      <span>Thông tin đăng ký</span>
                    </h4>
                    <p className="text-[11px] text-muted-steel leading-relaxed">
                      Để thay đổi thông tin định danh (Tên hiển thị, Email HUST, Vai trò), vui lòng liên hệ với Quản trị viên của Trường SOICT hoặc gửi phản hồi hỗ trợ kỹ thuật.
                    </p>
                  </div>
                </form>
              </div>
            )}
          </>
        )}

      </div>
    </AppShell>
  );
}
