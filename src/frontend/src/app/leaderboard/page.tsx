"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { 
  Trophy, 
  Award, 
  ChevronLeft, 
  ChevronRight, 
  ChevronsLeft, 
  ChevronsRight,
  Users,
  Star,
  Zap
} from "lucide-react";
import AppShell from "@/components/app-shell";
import api from "@/lib/api";

interface LeaderboardItem {
  rank: number;
  name: string;
  email: string;
  score: number;
  avatar: string;
  isCurrentUser?: boolean;
}

export default function LeaderboardPage() {
  const [user, setUser] = useState<any>(null);
  const [currentUserEntry, setCurrentUserEntry] = useState<LeaderboardItem | null>(null);
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardItem[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const itemsPerPage = 10;

  useEffect(() => {
    const fetchUserAndLeaderboard = async () => {
      setLoading(true);
      let loggedInUser = null;
      let userScore = null;
      try {
        loggedInUser = await api.get<any>("/auth/me");
        setUser(loggedInUser);
        if (loggedInUser && loggedInUser.role === "student") {
          try {
            userScore = await api.get<any>("/users/me/contribution-score");
          } catch (scoreErr) {
            console.error("Failed to load user score:", scoreErr);
          }
        }
      } catch (err) {
        console.error("Failed to load user info:", err);
      }

      let realLeaderboard: any[] = [];
      try {
        realLeaderboard = await api.get<any[]>("/leaderboard/global?limit=100");
      } catch (err) {
        console.error("Failed to load real leaderboard:", err);
      }

      // Seed list of 25 mock students with HUST credentials for rich UI demonstration (used only as fallback if DB is empty)
      const mockList: LeaderboardItem[] = [
        { rank: 1, name: "Lê Hoàng Hùng", email: "hung.lh226000@sis.hust.edu.vn", score: 4850, avatar: "LH" },
        { rank: 2, name: "Nguyễn Minh Đức", email: "duc.nm226123@sis.hust.edu.vn", score: 4120, avatar: "MD" },
        { rank: 3, name: "Trần Thu Trang", email: "trang.tt226234@sis.hust.edu.vn", score: 3500, avatar: "TT" },
        { rank: 4, name: "Phạm Tuấn Anh", email: "anh.pt226456@sis.hust.edu.vn", score: 3100, avatar: "PA" },
        { rank: 5, name: "Vũ Hải Đăng", email: "dang.vh226789@sis.hust.edu.vn", score: 2800, avatar: "HD" },
        { rank: 6, name: "Hoàng Quỳnh Chi", email: "chi.hq226012@sis.hust.edu.vn", score: 2650, avatar: "QC" },
        { rank: 7, name: "Nguyễn Trung Kiên", email: "kien.nt226134@sis.hust.edu.vn", score: 2400, avatar: "TK" },
        { rank: 8, name: "Đỗ Thùy Linh", email: "linh.dt226245@sis.hust.edu.vn", score: 2250, avatar: "TL" },
        { rank: 9, name: "Phạm Minh Quân", email: "quan.pm226356@sis.hust.edu.vn", score: 2100, avatar: "MQ" },
        { rank: 10, name: "Nguyễn Thị Mai", email: "mai.nt226467@sis.hust.edu.vn", score: 1950, avatar: "TM" },
        { rank: 11, name: "Bùi Việt Anh", email: "anh.bv226578@sis.hust.edu.vn", score: 1800, avatar: "VA" },
        { rank: 12, name: "Đinh Quang Huy", email: "huy.dq226689@sis.hust.edu.vn", score: 1700, avatar: "QH" },
        { rank: 13, name: "Lê Thị Vân", email: "van.lt226790@sis.hust.edu.vn", score: 1550, avatar: "LV" },
        { rank: 14, name: "Phan Thanh Bình", email: "binh.pt226801@sis.hust.edu.vn", score: 1450, avatar: "TB" },
        { rank: 15, name: "Nguyễn Quốc Khánh", email: "khanh.nq226912@sis.hust.edu.vn", score: 1350, avatar: "QK" },
        { rank: 16, name: "Trần Hữu Duy", email: "duy.th226023@sis.hust.edu.vn", score: 1250, avatar: "HD" },
        { rank: 17, name: "Vũ Thị Thủy", email: "thuy.vt226134@sis.hust.edu.vn", score: 1150, avatar: "VT" },
        { rank: 18, name: "Phạm Tiến Dũng", email: "dung.pt226245@sis.hust.edu.vn", score: 1050, avatar: "TD" },
        { rank: 19, name: "Nguyễn Hải Yến", email: "yen.nh226356@sis.hust.edu.vn", score: 980, avatar: "HY" },
        { rank: 20, name: "Đặng Văn Nam", email: "nam.dv226467@sis.hust.edu.vn", score: 900, avatar: "VN" },
        { rank: 21, name: "Ngô Gia Bảo", email: "bao.ng226578@sis.hust.edu.vn", score: 850, avatar: "GB" },
        { rank: 22, name: "Trịnh Ngọc Ánh", email: "anh.tn226689@sis.hust.edu.vn", score: 780, avatar: "NA" },
        { rank: 23, name: "Lý Minh Triết", email: "triet.lm226790@sis.hust.edu.vn", score: 700, avatar: "MT" },
        { rank: 24, name: "Phùng Thế Vinh", email: "vinh.pt226801@sis.hust.edu.vn", score: 620, avatar: "TV" },
        { rank: 25, name: "Dương Thu Hà", email: "ha.dt226912@sis.hust.edu.vn", score: 550, avatar: "TH" }
      ];

      let baseList: LeaderboardItem[] = [];
      const hasRealData = realLeaderboard && realLeaderboard.length > 0;

      if (hasRealData) {
        // Use ONLY real database data to prevent mock users from diluting real ranks
        realLeaderboard.forEach((realItem) => {
          const initials = realItem.full_name
            ? realItem.full_name.split(" ").map((n: string) => n[0]).join("").slice(0, 2).toUpperCase()
            : "SV";
          baseList.push({
            rank: realItem.rank || 99,
            name: realItem.full_name || "Thành viên SOICT",
            email: realItem.email,
            score: realItem.points,
            avatar: initials
          });
        });
      } else {
        // Use mock data if database leaderboard is empty (e.g. cold start)
        baseList = [...mockList];
      }

      // Handle logged in student
      if (loggedInUser) {
        const idx = baseList.findIndex(b => b.email.toLowerCase() === loggedInUser.email.toLowerCase());
        const initials = loggedInUser.full_name
          ? loggedInUser.full_name.split(" ").map((n: string) => n[0]).join("").slice(0, 2).toUpperCase()
          : "SV";
        const userPoints = userScore?.total_points ?? (idx !== -1 ? baseList[idx].score : 0);

        if (idx !== -1) {
          baseList[idx].isCurrentUser = true;
          baseList[idx].score = userPoints;
          baseList[idx].name = loggedInUser.full_name || baseList[idx].name;
          baseList[idx].avatar = initials;
        } else {
          baseList.push({
            rank: userScore?.global_rank || (baseList.length + 1),
            name: loggedInUser.full_name || "Bản thân",
            email: loggedInUser.email,
            score: userPoints,
            avatar: initials,
            isCurrentUser: true
          });
        }
      }

      // Re-sort baseList by score descending
      baseList.sort((a, b) => b.score - a.score);
      // Re-assign ranks
      baseList = baseList.map((item, index) => ({
        ...item,
        rank: index + 1
      }));

      // Find current user entry in the final sorted list
      if (loggedInUser) {
        const matched = baseList.find(e => e.email.toLowerCase() === loggedInUser.email.toLowerCase());
        if (matched) {
          setCurrentUserEntry(matched);
        }
      }
      
      setLeaderboardData(baseList);
      setLoading(false);
    };

    fetchUserAndLeaderboard();
  }, []);

  const obfuscateEmail = (email: string) => {
    if (!email) return "";
    const [local, domain] = email.split("@");
    if (!domain) return email;
    if (local.length <= 4) {
      return `${local.slice(0, 1)}***@${domain}`;
    }
    return `${local.slice(0, 3)}***${local.slice(-1)}@${domain}`;
  };

  // Pagination calculations
  const totalPages = Math.ceil(leaderboardData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedItems = leaderboardData.slice(startIndex, startIndex + itemsPerPage);

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const getRankBadge = (rank: number) => {
    switch (rank) {
      case 1:
        return (
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-amber-500 text-xs font-bold text-white shadow-xs" title="Gold">
            1
          </span>
        );
      case 2:
        return (
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-slate-400 text-xs font-bold text-white shadow-xs" title="Silver">
            2
          </span>
        );
      case 3:
        return (
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-amber-700 text-xs font-bold text-white shadow-xs" title="Bronze">
            3
          </span>
        );
      default:
        return <span className="font-mono text-xs text-muted-steel font-semibold w-6 h-6 flex items-center justify-center bg-slate-100 rounded-full">{rank}</span>;
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        
        {/* HUST Title Header */}
        <div className="relative overflow-hidden rounded-2xl border border-whisper-border bg-white p-6 shadow-sm">
          <div className="absolute top-0 right-0 h-24 w-24 translate-x-8 -translate-y-8 rounded-full bg-hust-red/5 blur-2xl" />
          
          <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <span className="font-label-mono text-[9px] font-extrabold tracking-widest uppercase text-hust-red bg-red-50 border border-red-100 rounded-md px-2 py-0.5">
                Academic Commons
              </span>
              <h1 className="mt-2 font-headline-lg text-2xl font-black text-slate-900 uppercase">
                BẢNG XẾP HẠNG ĐÓNG GÓP TOÀN CẦU
              </h1>
              <p className="mt-1 max-w-2xl font-body-sm text-xs text-muted-steel leading-relaxed">
                Vinh danh những thành viên tích cực đóng góp tài liệu học tập chuẩn hóa cho cộng đồng SOICT HUST.
              </p>
            </div>
            
            {/* Quick stats board */}
            <div className="grid grid-cols-2 gap-3 w-full md:w-auto min-w-[280px]">
              <div className="rounded-xl bg-canvas-base p-3 border border-whisper-border text-center">
                <Users className="mx-auto h-4 w-4 text-muted-steel mb-1" />
                <span className="block font-label-mono text-[8px] font-bold text-muted-steel uppercase tracking-wider">Thành viên</span>
                <span className="font-headline-md text-sm font-extrabold text-slate-900">{leaderboardData.length}</span>
              </div>
              <div className="rounded-xl bg-canvas-base p-3 border border-whisper-border text-center">
                <Star className="mx-auto h-4 w-4 text-pear-yellow mb-1" />
                <span className="block font-label-mono text-[8px] font-bold text-muted-steel uppercase tracking-wider">Tổng Điểm</span>
                <span className="font-headline-md text-sm font-extrabold text-slate-900">
                  {leaderboardData.reduce((sum, item) => sum + item.score, 0).toLocaleString("vi-VN")}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Student Pinned Top Banner Card */}
        {user?.role === "student" && currentUserEntry && (
          <div className="rounded-2xl border-2 border-hust-red bg-white p-6 shadow-md relative transition-all duration-200">
            <div className="absolute top-0 left-0 right-0 h-1.5 bg-linear-to-r from-hust-red to-pear-yellow" />
            
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div className="flex items-center gap-4">
                <div className="relative flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-hust-red font-headline-md text-lg font-extrabold text-white uppercase shadow-sm border border-whisper-border">
                  {currentUserEntry.avatar}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-headline-md text-base font-extrabold text-slate-900">{currentUserEntry.name}</span>
                    <span className="rounded-full bg-hust-red/10 border border-hust-red/35 px-2 py-0.5 text-[9px] font-extrabold text-hust-red font-label-mono uppercase tracking-wider flex items-center gap-0.5">
                      <Zap className="h-3 w-3 fill-hust-red" /> Vị trí của bạn
                    </span>
                  </div>
                  <p className="font-mono text-[10px] text-muted-steel font-semibold mt-0.5">{obfuscateEmail(currentUserEntry.email)}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-8 w-full md:w-auto justify-between md:justify-end border-t border-slate-50 pt-4 md:border-none md:pt-0">
                <div className="text-left md:text-right">
                  <span className="block text-[9px] text-muted-steel font-bold uppercase tracking-wider font-label-mono">Xếp hạng</span>
                  <span className="font-headline-lg text-2xl font-black text-slate-900">#{currentUserEntry.rank}</span>
                </div>
                <div className="text-right">
                  <span className="block text-[9px] text-muted-steel font-bold uppercase tracking-wider font-label-mono">Tổng điểm</span>
                  <span className="font-headline-lg text-2xl font-black text-hust-red">{currentUserEntry.score.toLocaleString()} <span className="text-[10px] text-muted-steel font-semibold font-label-mono">XP</span></span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Large Beautiful Leaderboard Table Card */}
        <div className="rounded-2xl border border-whisper-border bg-white overflow-hidden shadow-sm">
          
          <div className="border-b border-whisper-border px-6 py-5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h2 className="font-headline-md text-base font-extrabold text-slate-900 flex items-center gap-2">
              <Trophy className="h-5 w-5 text-pear-yellow" /> BẢNG VÀNG ĐÓNG GÓP
            </h2>
            <div className="font-label-mono text-[10px] font-bold text-muted-steel bg-canvas-base px-3 py-1.5 border border-whisper-border rounded-md">
              Hiển thị {startIndex + 1} - {Math.min(startIndex + itemsPerPage, leaderboardData.length)} trên tổng số {leaderboardData.length} thành viên
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr className="border-b border-whisper-border bg-slate-50 font-label-mono text-[10px] font-bold text-muted-steel uppercase tracking-wider select-none">
                  <th className="px-6 py-4 w-24">Hạng</th>
                  <th className="px-6 py-4">Thành viên</th>
                  <th className="px-6 py-4 hidden md:table-cell">Email</th>
                  <th className="px-6 py-4 text-right w-44">Điểm (XP)</th>
                  <th className="px-6 py-4 hidden sm:table-cell w-48">Cấp độ đóng góp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-whisper-border font-body-sm text-slate-800">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-muted-steel font-semibold">
                      Đang tải bảng xếp hạng...
                    </td>
                  </tr>
                ) : paginatedItems.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-muted-steel font-semibold">
                      Chưa có thành viên nào đóng góp.
                    </td>
                  </tr>
                ) : (
                  paginatedItems.map((item) => {
                    const percent = Math.min(100, Math.round((item.score / 5000) * 100));
                    return (
                      <tr 
                        key={item.email} 
                        className={`transition-colors hover:bg-slate-50/50 ${
                          item.isCurrentUser 
                            ? "bg-red-50/20 hover:bg-red-50/30 border-l-4 border-l-hust-red" 
                            : ""
                        }`}
                      >
                        {/* Rank Cell */}
                        <td className="px-6 py-4 align-middle whitespace-nowrap">
                          {getRankBadge(item.rank)}
                        </td>
                        
                        {/* Member Cell */}
                        <td className="px-6 py-4 align-middle">
                          <div className="flex items-center gap-3">
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-100 font-headline-md text-xs font-extrabold text-slate-900 uppercase border border-whisper-border">
                              {item.avatar}
                            </div>
                            <span className="font-headline-md text-sm font-extrabold text-slate-900 flex items-center gap-1.5">
                              {item.name} 
                              {item.isCurrentUser && <span className="text-[10px] font-bold font-label-mono text-hust-red bg-red-50 border border-red-100 px-1.5 py-0.2 rounded-md">BẠN</span>}
                            </span>
                          </div>
                        </td>
                        
                        {/* Email Cell */}
                        <td className="px-6 py-4 align-middle font-mono text-xs text-muted-steel hidden md:table-cell whitespace-nowrap">
                          {obfuscateEmail(item.email)}
                        </td>
                        
                        {/* Score Cell */}
                        <td className="px-6 py-4 align-middle text-right font-headline-md text-sm font-extrabold text-slate-900 whitespace-nowrap">
                          {item.score.toLocaleString()} <span className="text-[10px] text-muted-steel font-semibold font-label-mono">XP</span>
                        </td>

                        {/* Progress level */}
                        <td className="px-6 py-4 align-middle hidden sm:table-cell">
                          <div className="w-full">
                            <div className="flex justify-between items-center text-[9px] text-muted-steel font-bold uppercase tracking-wider font-label-mono mb-1">
                              <span>Cấp {Math.ceil(item.score / 1000)}</span>
                              <span>{percent}%</span>
                            </div>
                            <div className="h-2 w-full rounded-full bg-canvas-base overflow-hidden border border-whisper-border">
                              <div 
                                className="h-full rounded-full bg-hust-red transition-all duration-500" 
                                style={{ width: `${percent}%` }}
                              />
                            </div>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination buttons */}
          <div className="border-t border-whisper-border bg-slate-50/50 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
            
            {/* Quick jump left */}
            <div className="flex items-center gap-1">
              <button 
                onClick={() => handlePageChange(1)}
                disabled={currentPage === 1}
                className="tactile-button text-[12px] py-1.5 px-3 bg-white hover:bg-canvas-base border border-whisper-border text-slate-700 disabled:opacity-50"
                title="First Page"
              >
                <ChevronsLeft className="h-4 w-4" />
              </button>
              <button 
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="tactile-button text-[12px] py-1.5 px-3 bg-white hover:bg-canvas-base border border-whisper-border text-slate-700 disabled:opacity-50"
                title="Previous Page"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
            </div>

            {/* Page Numbers */}
            <div className="flex items-center gap-1.5">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => handlePageChange(page)}
                  className={
                    currentPage === page
                      ? "tactile-button-primary text-[11px] py-1.5 px-3.5 bg-hust-red text-white border-hust-red hover:bg-hust-red/90"
                      : "tactile-button text-[11px] py-1.5 px-3 bg-white hover:bg-canvas-base border border-whisper-border text-slate-800"
                  }
                >
                  {page}
                </button>
              ))}
            </div>

            {/* Next / Last buttons */}
            <div className="flex items-center gap-1">
              <button 
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="tactile-button text-[12px] py-1.5 px-3 bg-white hover:bg-canvas-base border border-whisper-border text-slate-700 disabled:opacity-50"
                title="Next Page"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
              <button 
                onClick={() => handlePageChange(totalPages)}
                disabled={currentPage === totalPages}
                className="tactile-button text-[12px] py-1.5 px-3 bg-white hover:bg-canvas-base border border-whisper-border text-slate-700 disabled:opacity-50"
                title="Last Page"
              >
                <ChevronsRight className="h-4 w-4" />
              </button>
            </div>

          </div>
        </div>

      </div>
    </AppShell>
  );
}
