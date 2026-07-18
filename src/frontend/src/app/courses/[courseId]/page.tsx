/* eslint-disable react-hooks/exhaustive-deps, @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars, prefer-const */
"use client";

import React, { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import AppShell from "../../../components/app-shell";
import { 
  mockCourses, 
  mockDocuments, 
  Document as DocType
} from "../../../lib/mockData";
import { 
  BookOpen, 
  FileText, 
  Network, 
  GraduationCap, 
  Send, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  Upload,
  X,
  FileCheck,
  ThumbsUp,
  ThumbsDown,
  Info,
  ZoomIn,
  ZoomOut,
  Maximize2,
  PanelLeftClose,
  PanelLeftOpen
} from "lucide-react";

import api, { streamTutorQuery } from "../../../lib/api";
import { useAsyncAction } from "../../../lib/useAsyncAction";
import MarkdownRenderer from "../../../components/markdown-renderer";
import CourseMindmap from "../../../components/course-mindmap";
import { useToast } from "../../../components/toast";

export default function CourseWorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;
  const { showToast } = useToast();

  // A document is viewable once it has been approved and/or indexed for RAG.
  const isViewable = (status: string) => status === "APPROVED" || status === "INDEXED";

  const [course, setCourse] = useState<any>(null);
  const [docsList, setDocsList] = useState<DocType[]>([]);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState<string>("tutor");
  
  // App states
  const [viewerDoc, setViewerDoc] = useState<any | null>(null);
  const [viewerMarkdown, setViewerMarkdown] = useState<string>("");
  const [viewerRawUrl, setViewerRawUrl] = useState<string>("");
  const [viewMode, setViewMode] = useState<"ocr" | "split" | "original">("split");
  const [viewerVote, setViewerVote] = useState<"up" | "down" | null>(null);
  const [voteCounts, setVoteCounts] = useState<{ up: number; down: number }>({ up: 0, down: 0 });
  
  // Image viewer zoom and position states
  const [imgScale, setImgScale] = useState(1);
  const [imgPosition, setImgPosition] = useState({ x: 0, y: 0 });
  const [imgIsDragging, setImgIsDragging] = useState(false);
  const imgDragStart = useRef({ x: 0, y: 0 });
  const imgContainerRef = useRef<HTMLDivElement>(null);
  
  // Tutor sessions & chat state
  const [sessionsList, setSessionsList] = useState<any[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<any[]>([]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  // Live agent status label shown while the tutor "thinks" (before streaming text).
  const [agentStatus, setAgentStatus] = useState<string | null>(null);
  // Assistant text accumulated from text_delta events while it streams in.
  const [streamingText, setStreamingText] = useState<string>("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  // User details
  const [currentUser, setCurrentUser] = useState<any>(null);

  // Upload state
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadType, setUploadType] = useState("lecture_slides");
  const [uploadConsent, setUploadConsent] = useState(false);
  const [uploadErrors, setUploadErrors] = useState<{ title?: string; file?: string; consent?: string }>({});

  // Mindmap state
  const [mindmapGraph, setMindmapGraph] = useState<{ nodes: any[]; edges: any[] }>({ nodes: [], edges: [] });
  const [mindmapLoading, setMindmapLoading] = useState(false);

  // Mock test state
  const [testSettings, setTestSettings] = useState({ difficulty: "medium", count: 5 });
  const [testStarted, setTestStarted] = useState(false);
  const [questions, setQuestions] = useState<any[]>([]);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [testSubmitted, setTestSubmitted] = useState(false);
  const [testScore, setTestScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [noQuestionsAvailable, setNoQuestionsAvailable] = useState(false);

  // Fetch course metadata, user profile, documents, sessions, and mindmap
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const user = await api.get<any>("/auth/me");
        setCurrentUser(user);
        
        // Adjust default upload types based on role
        if (user.role === "student") {
          setUploadType("summary_note");
        } else {
          setUploadType("lecture_slides");
        }
      } catch (err) {
        console.error("Failed to load user profile", err);
      }
    };
    fetchUserProfile();
  }, []);

  const fetchDocuments = async () => {
    try {
      const data = await api.get<any>(`/courses/${courseId}/documents`);
      const docs = data.items || [];
      // Map database Document model to frontend type properties
      const mappedDocs = docs.map((d: any) => ({
        id: d.id,
        course_code: d.course_code,
        title: d.original_filename || d.filename || d.title || "Tài liệu học thuật",
        filename: d.original_filename || d.filename,
        file_format: d.file_format,
        uploaded_by: d.uploader_id,
        uploaded_at: d.uploaded_at,
        status: d.status,
        tier: d.document_tier === "official" ? 1 : 2,
        file_type: d.material_type || d.contribution_type || "lecture_slides",
        file_size_bytes: d.file_size_bytes || 1024 * 1024,
      }));
      setDocsList(mappedDocs);

      // Auto select first approved doc for viewer if none is selected
      const approved = mappedDocs.filter((d: any) => isViewable(d.status));
      if (approved.length > 0 && !viewerDoc) {
        handleSelectViewerDoc(approved[0]);
      }
    } catch (err) {
      console.error("Failed to load course documents", err);
    }
  };

  const fetchSessions = async () => {
    try {
      const sessions = await api.get<any[]>(`/tutor/sessions?course_code=${courseId}`);
      setSessionsList(sessions || []);
      if (sessions && sessions.length > 0 && !activeSessionId) {
        setActiveSessionId(sessions[0].id);
      }
    } catch (err) {
      console.error("Failed to load tutor sessions", err);
    }
  };

  useEffect(() => {
    const fetchCourseAndData = async () => {
      try {
        const c = await api.get<any>(`/courses/${courseId}`);
        setCourse(c);
      } catch (err) {
        console.error("Failed to load course details", err);
      }
      await Promise.all([fetchDocuments(), fetchSessions()]);
    };
    if (courseId) {
      fetchCourseAndData();
    }
  }, [courseId]);

  // Load chat messages when active session changes
  useEffect(() => {
    const fetchMessages = async () => {
      if (!activeSessionId) {
        // Reset or show welcome message
        setChatMessages([
          {
            id: "msg-welcome",
            role: "assistant",
            content: `Chào bạn! Tôi là Virtual Tutor hỗ trợ học tập cho học phần **${course?.name || courseId}**. Hãy nhập câu hỏi thảo luận hoặc chọn cuộc hội thoại cũ ở danh sách bên dưới nhé.`,
            timestamp: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
          }
        ]);
        return;
      }
      try {
        const messages = await api.get<any[]>(`/tutor/sessions/${activeSessionId}/messages`);
        const formatted = messages.map((m: any) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          timestamp: new Date(m.created_at || Date.now()).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
          citations: m.citations,
        }));
        setChatMessages(formatted);
      } catch (err) {
        console.error("Failed to load chat messages", err);
      }
    };
    fetchMessages();
  }, [activeSessionId, course]);

  // Fetch the raw concept graph; the CourseMindmap component handles layout.
  useEffect(() => {
    const fetchMindmap = async () => {
      if (activeTab === "mindmap") {
        setMindmapLoading(true);
        try {
          const mapData = await api.get<any>(`/courses/${courseId}/mindmap`);
          const graph = mapData.concept_graph || { nodes: [], edges: [] };
          setMindmapGraph({ nodes: graph.nodes || [], edges: graph.edges || [] });
        } catch (err) {
          console.error("Failed to load course mindmap", err);
        } finally {
          setMindmapLoading(false);
        }
      }
    };
    fetchMindmap();
  }, [activeTab, courseId]);

  // Scroll to bottom of chat
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatMessages, streamingText, agentStatus]);

  // Handle countdown timer for Mock Test
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (testStarted && timeLeft > 0 && !testSubmitted) {
      timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
    } else if (testStarted && timeLeft === 0 && !testSubmitted) {
      handleSubmittingTest();
    }
    return () => clearTimeout(timer);
  }, [testStarted, timeLeft, testSubmitted]);

  // Detect image documents from the reliable backend file_format, falling back
  // to the filename extension. PDFs (and anything else) use the iframe viewer.
  const isImageDoc = (doc: any) => {
    const fmt = (doc?.file_format || "").toLowerCase();
    if (["jpg", "jpeg", "png"].includes(fmt)) return true;
    return /\.(png|jpe?g)$/i.test(doc?.filename || "");
  };

  // Wheel zoom effect for image viewer (non-passive listener)
  useEffect(() => {
    const container = imgContainerRef.current;
    if (!container) return;

    const handleWheel = (e: WheelEvent) => {
      if (isImageDoc(viewerDoc)) {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.1 : -0.1;
        setImgScale(prev => {
          const next = Math.min(Math.max(prev + delta, 0.5), 4);
          if (next <= 1) {
            setImgPosition({ x: 0, y: 0 });
          }
          return next;
        });
      }
    };

    container.addEventListener("wheel", handleWheel, { passive: false });
    return () => {
      container.removeEventListener("wheel", handleWheel);
    };
  }, [viewerDoc]);

  const handleImgMouseDown = (e: React.MouseEvent) => {
    if (imgScale <= 1) return; // Only pan when zoomed in
    e.preventDefault();
    setImgIsDragging(true);
    imgDragStart.current = { x: e.clientX - imgPosition.x, y: e.clientY - imgPosition.y };
  };

  const handleImgMouseMove = (e: React.MouseEvent) => {
    if (!imgIsDragging) return;
    e.preventDefault();
    setImgPosition({
      x: e.clientX - imgDragStart.current.x,
      y: e.clientY - imgDragStart.current.y
    });
  };

  const handleImgMouseUp = () => {
    setImgIsDragging(false);
  };

  const handleZoomIn = () => {
    setImgScale(prev => Math.min(prev + 0.25, 4));
  };

  const handleZoomOut = () => {
    setImgScale(prev => {
      const next = Math.max(prev - 0.25, 0.5);
      if (next <= 1) {
        setImgPosition({ x: 0, y: 0 });
      }
      return next;
    });
  };

  const handleZoomReset = () => {
    setImgScale(1);
    setImgPosition({ x: 0, y: 0 });
  };

  // Handle selecting document in viewer
  async function handleSelectViewerDoc(doc: any) {
    setViewerDoc(doc);
    setViewerMarkdown("Đang tải nội dung văn bản trích xuất (OCR)...");
    setViewerRawUrl("");
    setViewerVote(null);
    setVoteCounts({ up: 0, down: 0 });
    setImgScale(1);
    setImgPosition({ x: 0, y: 0 });
    try {
      const [markdownText, signedData] = await Promise.all([
        api.get<string>(`/documents/${doc.id}/markdown`),
        api.get<any>(`/documents/${doc.id}/raw-url`),
      ]);
      setViewerMarkdown(markdownText || "Tài liệu này không có nội dung markdown.");
      setViewerRawUrl(signedData.url || "");
    } catch (err) {
      console.error("Failed to fetch document contents", err);
      setViewerMarkdown("Không thể tải nội dung OCR của tài liệu này.");
    }
    // Vote tallies + the user's existing vote (only meaningful for indexed docs)
    if (doc.status === "INDEXED") {
      try {
        const summary = await api.get<any>(`/documents/${doc.id}/vote`);
        setViewerVote(summary.my_vote ?? null);
        setVoteCounts({ up: summary.up_count ?? 0, down: summary.down_count ?? 0 });
      } catch (err) {
        console.error("Failed to fetch vote summary", err);
      }
    }
  }

  // Cast / retract an up or down vote on the document being viewed (students only)
  const { pending: isVoting, run: handleVote } = useAsyncAction(async (direction: "up" | "down") => {
    if (!viewerDoc) return;
    // Clicking the active direction again retracts the vote
    const nextVote = viewerVote === direction ? null : direction;
    try {
      const res = await api.post<any>(`/documents/${viewerDoc.id}/vote`, { vote: nextVote });
      setViewerVote(res.my_vote ?? null);
      setVoteCounts({ up: res.up_count ?? 0, down: res.down_count ?? 0 });
    } catch (err: any) {
      console.error("Failed to cast vote", err);
      showToast(`Không thể bình chọn: ${err.message || "Lỗi kết nối."}`, "error");
    }
  });

  // Virtual Tutor Submit
  const handleSendChat = async () => {
    if (!inputText.trim()) return;

    const userMsg = {
      id: `msg-user-${Date.now()}`,
      role: "user",
      content: inputText,
      timestamp: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
    };

    setChatMessages(prev => [...prev, userMsg]);
    setInputText("");
    setIsTyping(true);
    setAgentStatus(null);
    setStreamingText("");

    // Local accumulators (avoid stale-closure reads of state inside handlers).
    let accumulated = "";
    let streamedSessionId: string | null = null;
    let finished = false;

    const nowTime = () => new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });

    // Tutor always retrieves over the whole course corpus (no per-document scoping).
    await streamTutorQuery(
      {
        course_code: courseId,
        question: userMsg.content,
        session_id: activeSessionId || undefined,
      },
      {
        onSession: (sessionId) => {
          streamedSessionId = sessionId;
        },
        onStatus: (_step, label) => {
          // Replace the blinking "..." with a live status label.
          setAgentStatus(label);
        },
        onTextDelta: (text) => {
          accumulated += text;
          // First delta switches from status block to the streaming answer bubble.
          setAgentStatus(null);
          setStreamingText(accumulated);
        },
        onReset: () => {
          // A streamed turn turned out to be an internal tool call: discard it.
          accumulated = "";
          setStreamingText("");
        },
        onDone: ({ session_id, answer, citations }) => {
          finished = true;
          setStreamingText("");
          setAgentStatus(null);
          setChatMessages(prev => [...prev, {
            id: `msg-reply-${Date.now()}`,
            role: "assistant",
            content: answer,
            timestamp: nowTime(),
            citations,
          }]);

          const finalSessionId = session_id || streamedSessionId;
          if (finalSessionId && finalSessionId !== activeSessionId) {
            setActiveSessionId(finalSessionId);
            fetchSessions();
          }
        },
        onError: (message) => {
          finished = true;
          setStreamingText("");
          setAgentStatus(null);
          setChatMessages(prev => [...prev, {
            id: `msg-error-${Date.now()}`,
            role: "assistant",
            content: `Lỗi kết nối: ${message || "Không thể gửi câu hỏi đến AI Tutor."}`,
            timestamp: nowTime(),
          }]);
        },
      }
    );

    // Safety net: if the stream ended without a terminal done/error event,
    // commit whatever text was streamed so the bubble is not lost.
    if (!finished) {
      setStreamingText("");
      setAgentStatus(null);
      if (accumulated.trim()) {
        setChatMessages(prev => [...prev, {
          id: `msg-reply-${Date.now()}`,
          role: "assistant",
          content: accumulated,
          timestamp: nowTime(),
          // Connection dropped before a done/error event arrived: this text is
          // a partial answer, not a finished one — flag it so the UI doesn't
          // present it as trustworthy and complete.
          interrupted: true,
        }]);
      }
    }

    setIsTyping(false);
  };

  const { pending: deletingSession, run: handleDeleteSession } = useAsyncAction(async (id: string) => {
    if (!confirm("Bạn có chắc chắn muốn xóa cuộc trò chuyện này?")) return;
    try {
      await api.del(`/tutor/sessions/${id}`);
      showToast("Đã xóa cuộc trò chuyện", "success");
      if (activeSessionId === id) {
        setActiveSessionId(null);
        setChatMessages([
          {
            id: "msg-welcome",
            role: "assistant",
            content: `Chào bạn! Tôi là Virtual Tutor hỗ trợ học tập cho học phần **${course?.name || courseId}**. Hãy bắt đầu cuộc hội thoại mới bằng cách đặt câu hỏi.`,
            timestamp: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
          }
        ]);
      }
      fetchSessions();
    } catch (err: any) {
      console.error("Failed to delete session", err);
      showToast(`Lỗi xóa cuộc trò chuyện: ${err.message}`, "error");
    }
  });

  // Document Upload Submit Handler
  const { pending: uploadingDoc, run: handleUploadSubmit } = useAsyncAction(async (e: React.FormEvent) => {
    e.preventDefault();

    // Lightweight Vietnamese validation (form uses noValidate to avoid English browser messages)
    const MAX_FILE_BYTES = 30 * 1024 * 1024; // 30MB
    const ALLOWED_EXTENSIONS = [".pdf", ".pptx", ".png", ".jpg", ".jpeg"];

    const errors: { title?: string; file?: string; consent?: string } = {};
    if (!uploadTitle.trim()) {
      errors.title = "Vui lòng nhập tên tài liệu.";
    }
    if (!uploadFile) {
      errors.file = "Vui lòng chọn tệp tin để tải lên.";
    } else {
      const ext = uploadFile.name.slice(uploadFile.name.lastIndexOf(".")).toLowerCase();
      if (!ALLOWED_EXTENSIONS.includes(ext)) {
        errors.file = "Định dạng tệp không hợp lệ. Chỉ chấp nhận .pdf, .pptx, .png, .jpg, .jpeg.";
      } else if (uploadFile.size > MAX_FILE_BYTES) {
        errors.file = "Tệp vượt quá dung lượng cho phép (tối đa 30MB).";
      }
    }
    if (!uploadConsent) {
      errors.consent = "Bạn cần xác nhận quyền chia sẻ và đồng ý với chính sách trước khi tải lên.";
    }
    if (Object.keys(errors).length > 0) {
      setUploadErrors(errors);
      return;
    }
    setUploadErrors({});

    const formData = new FormData();
    formData.append("course_code", courseId);
    formData.append("file", uploadFile!); // validated non-null above
    formData.append("display_name", uploadTitle);
    formData.append("shared_rights_confirmed", String(uploadConsent));

    const isStaff = currentUser?.role === "admin" || currentUser?.role === "reviewer";
    const endpoint = isStaff ? "/documents/official" : "/documents/community";

    if (isStaff) {
      formData.append("material_type", uploadType); // official material type
    } else {
      formData.append("contribution_type", uploadType); // community contribution type
      formData.append("topic_tags", JSON.stringify([])); // community topic tags JSON
    }

    try {
      const response = await api.post<any>(endpoint, formData);
      setShowUploadModal(false);
      setUploadTitle("");
      setUploadFile(null);
      setUploadConsent(false);
      setUploadErrors({});
      showToast("Tài liệu đóng góp của bạn đã được tải lên thành công và đang được đưa vào hàng đợi xử lý tự động (OCR & Đánh giá chất lượng)!", "success");
      await fetchDocuments();
    } catch (err: any) {
      console.error("Failed to upload document", err);
      showToast(`Lỗi tải lên tài liệu: ${err.message}`, "error");
    }
  });

  // Click on citation links
  const handleCitationClick = (docId: string, pageNum?: number) => {
    const foundDoc = docsList.find(d => d.id === docId);
    if (foundDoc) {
      handleSelectViewerDoc(foundDoc);
      setActiveTab("viewer");
    }
  };

  // Mock Test Generator
  const { pending: generatingTest, run: generateMockQuiz } = useAsyncAction(async () => {
    try {
      setQuestions([]);
      setTestSubmitted(false);
      setNoQuestionsAvailable(false);

      // Map single difficulty selected into distribution
      const difficulty = testSettings.difficulty;
      const count = testSettings.count;
      let easy = 0, medium = 0, hard = 0;
      if (difficulty === "easy") {
        easy = count;
      } else if (difficulty === "hard") {
        medium = Math.floor(count * 0.3);
        hard = Math.ceil(count * 0.7);
      } else {
        easy = Math.floor(count * 0.3);
        medium = Math.ceil(count * 0.7);
      }

      const payload = {
        total_questions: count,
        difficulty_distribution: { easy, medium, hard }
      };

      const response = await api.post<any>(`/courses/${courseId}/mock-tests/generate`, payload);
      const fetchedQuestions = response.questions || [];
      const mapped = fetchedQuestions.map((q: any, idx: number) => ({
        id: q.id,
        question: q.question_text || `Câu hỏi ôn tập ${idx + 1}`,
        options: (q.options || []).map((o: any) => ({
          key: o.key,
          val: o.text || o.val || ""
        })),
        correct: q.correct_answer,
        rationale: q.explanation && q.explanation.trim()
          ? q.explanation
          : "Đáp án đúng dựa trên nội dung tài liệu nguồn của môn học.",
        // Backend citations only carry chunk_id + excerpt (no reliable doc/page),
        // so we surface the excerpt text rather than a navigation link.
        citation: q.citations && q.citations.length > 0 && q.citations[0].excerpt
          ? { excerpt: q.citations[0].excerpt }
          : null
      }));

      if (mapped.length === 0) {
        setNoQuestionsAvailable(true);
        return;
      }

      setQuestions(mapped);
      setSelectedAnswers({});
      setTimeLeft(mapped.length * 60);
      setTestStarted(true);
    } catch (err: any) {
      console.error("Failed to generate mock test", err);
      showToast(`Lỗi sinh đề thi thử: ${err.message}`, "error");
      setTestStarted(false);
    }
  });

  function handleSubmittingTest() {
    let score = 0;
    questions.forEach((q, idx) => {
      if (selectedAnswers[idx] === q.correct) {
        score++;
      }
    });
    setTestScore(score);
    setTestSubmitted(true);
  }

  // Mock test / mindmap features require at least one viewable (approved/indexed) document.
  const hasViewableDocs = docsList.some(d => isViewable(d.status));

  if (!course) {
    return (
      <AppShell fullBleed>
        <div className="flex flex-col items-center justify-center h-full p-8 text-center">
          <div className="w-10 h-10 border-4 border-hust-red border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-muted-steel text-sm font-semibold">Đang tải cấu trúc học phần...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell fullBleed>
      <div className="flex h-full overflow-hidden">
        
        {/* LEFT PANEL: Document list sidebar (collapsible) */}
        {sidebarCollapsed ? (
          <aside className="w-12 border-r-1.5 border-whisper-border bg-white flex flex-col items-center py-4 shrink-0">
            <button
              type="button"
              title="Mở rộng danh sách tài liệu"
              aria-label="Mở rộng danh sách tài liệu"
              className="p-2 rounded-lg text-muted-steel hover:bg-canvas-base hover:text-hust-red transition-colors"
              onClick={() => setSidebarCollapsed(false)}
            >
              <PanelLeftOpen className="w-5 h-5" />
            </button>
          </aside>
        ) : (
          <aside className="w-1/4 border-r-1.5 border-whisper-border bg-white flex flex-col justify-between overflow-y-auto shrink-0">
          <div className="p-4 space-y-5">
            <div className="flex items-center justify-between pb-2 border-b border-whisper-border">
              <h2 className="font-display font-extrabold text-[16px] text-charcoal-ink">Tài liệu môn học</h2>
              <button
                type="button"
                title="Thu gọn thanh tài liệu"
                aria-label="Thu gọn thanh tài liệu"
                className="p-1.5 rounded-lg text-muted-steel hover:bg-canvas-base hover:text-hust-red transition-colors"
                onClick={() => setSidebarCollapsed(true)}
              >
                <PanelLeftClose className="w-4 h-4" />
              </button>
            </div>

            {/* Official Tier 1 Documents */}
            <div className="space-y-2.5">
              <span className="block text-[11px] font-bold text-muted-steel tracking-wider uppercase font-display">Tài liệu chính thống (Tier 1)</span>
              <div className="space-y-1.5">
                {docsList.filter(d => d.tier === 1).map(doc => (
                  <button
                    key={doc.id}
                    type="button"
                    disabled={!isViewable(doc.status)}
                    onClick={() => { handleSelectViewerDoc(doc); setActiveTab("viewer"); }}
                    className={`w-full text-left flex items-start gap-2.5 p-2 rounded-lg transition-colors border ${
                      viewerDoc?.id === doc.id ? "bg-[#FFF8F6] border-hust-red/20" : "border-transparent hover:bg-canvas-base"
                    } ${isViewable(doc.status) ? "cursor-pointer" : "opacity-50 cursor-not-allowed"}`}
                  >
                    <div className="flex-1 min-w-0">
                      <span className="block text-body-sm font-semibold text-charcoal-ink truncate">{doc.title}</span>
                      <span className="block text-[10px] text-muted-steel font-mono">{doc.filename}</span>
                    </div>
                  </button>
                ))}
                {docsList.filter(d => d.tier === 1).length === 0 && (
                  <div className="px-2 py-3 space-y-2">
                    <span className="block text-xs text-muted-steel italic leading-relaxed">
                      Chưa có tài liệu chính thống nào được duyệt. Hãy đóng góp tài liệu đầu tiên cho môn học này!
                    </span>
                    <button
                      className="tactile-button tactile-button-primary w-full flex items-center justify-center gap-1.5 py-1.5 text-xs"
                      onClick={() => setShowUploadModal(true)}
                    >
                      <Upload className="w-3.5 h-3.5" />
                      <span>Tải lên tài liệu mới</span>
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Community Tier 2 Documents */}
            <div className="space-y-2.5">
              <span className="block text-[11px] font-bold text-muted-steel tracking-wider uppercase font-display">Đóng góp cộng đồng (Tier 2)</span>
              <div className="space-y-1.5">
                {docsList.filter(d => d.tier === 2).map(doc => (
                  <button
                    key={doc.id}
                    type="button"
                    disabled={!isViewable(doc.status)}
                    onClick={() => { handleSelectViewerDoc(doc); setActiveTab("viewer"); }}
                    className={`w-full text-left flex items-start gap-2.5 p-2 rounded-lg transition-colors border ${
                      viewerDoc?.id === doc.id ? "bg-[#FFF8F6] border-hust-red/20" : "border-transparent hover:bg-canvas-base"
                    } ${isViewable(doc.status) ? "cursor-pointer" : "cursor-not-allowed"}`}
                  >
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1">
                        <span className="text-body-sm font-semibold text-charcoal-ink truncate">{doc.title}</span>
                        {!isViewable(doc.status) && doc.status !== "REJECTED" && doc.status !== "FAILED" && (
                          <span className="w-1.5 h-1.5 rounded-full bg-pear-yellow animate-pulse shrink-0"></span>
                        )}
                      </div>
                      <div className="flex justify-between items-center text-[10px] text-muted-steel">
                        <span className="font-mono">{doc.filename}</span>
                        <span className={`font-semibold ${
                          isViewable(doc.status) ? "text-system-green" :
                          (doc.status === "REJECTED" || doc.status === "FAILED") ? "text-system-red" : "text-pear-yellow"
                        }`}>{doc.status}</span>
                      </div>
                    </div>
                  </button>
                ))}
                {docsList.filter(d => d.tier === 2).length === 0 && (
                  <span className="block text-xs text-muted-steel italic px-2">Chưa có tài liệu đóng góp.</span>
                )}
              </div>
            </div>
          </div>

          {/* Student Upload Action Trigger */}
          <div className="p-4 border-t border-whisper-border bg-canvas-base">
            <button 
              className="tactile-button tactile-button-primary w-full flex items-center justify-center gap-2 py-2.5"
              onClick={() => setShowUploadModal(true)}
            >
              <Upload className="w-4 h-4" />
              <span>Đóng góp tài liệu mới</span>
            </button>
          </div>
          </aside>
        )}

        {/* RIGHT PANEL: Workspace Canvas & Tabs Panel (fills remaining width) */}
        <main className="flex-1 min-w-0 flex flex-col overflow-hidden">
          
          {/* Tab Navigation Menu */}
          <header className="flex justify-between items-center bg-white border-b-1.5 border-whisper-border px-6 py-2">
            <div className="flex gap-1.5">
              <button 
                className={`flex items-center gap-2 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-colors ${
                  activeTab === "tutor" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
                }`}
                onClick={() => setActiveTab("tutor")}
              >
                <BookOpen className="w-4 h-4" />
                <span>AI Tutor Chat</span>
              </button>
              <button 
                className={`flex items-center gap-2 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-colors ${
                  activeTab === "viewer" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
                }`}
                onClick={() => setActiveTab("viewer")}
              >
                <FileText className="w-4 h-4" />
                <span>Xem tài liệu</span>
              </button>
              <button 
                className={`flex items-center gap-2 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-colors ${
                  activeTab === "mindmap" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
                }`}
                onClick={() => setActiveTab("mindmap")}
              >
                <Network className="w-4 h-4" />
                <span>Mindmap</span>
              </button>
              <button 
                className={`flex items-center gap-2 px-4 py-2 border-b-2 font-display text-body-sm font-bold transition-colors ${
                  activeTab === "mocktest" ? "border-hust-red text-hust-red" : "border-transparent text-muted-steel hover:text-charcoal-ink"
                }`}
                onClick={() => setActiveTab("mocktest")}
              >
                <GraduationCap className="w-4 h-4" />
                <span>Thi thử trắc nghiệm</span>
              </button>
            </div>

            <div className="text-right">
              <span className="block font-display font-extrabold text-body-sm text-charcoal-ink">{course.course_code}</span>
              <span className="block text-[11px] text-muted-steel truncate max-w-[240px]">{course.name}</span>
            </div>
          </header>

          {/* Tab Content Display Container */}
          <section className="flex-1 overflow-hidden bg-canvas-base">
            
            {/* TAB 1: AI VIRTUAL TUTOR CHAT */}
            {activeTab === "tutor" && (
              <div className="flex h-full overflow-hidden bg-white">
                {/* Session Sidebar (Left 25%) */}
                <div className="w-1/4 border-r border-whisper-border bg-slate-50 flex flex-col justify-between overflow-y-auto">
                  <div className="p-3 space-y-3">
                    <button
                      className="tactile-button bg-white border border-whisper-border text-charcoal-ink font-bold text-xs py-2 w-full flex items-center justify-center gap-1 hover:bg-slate-100 transition-colors"
                      onClick={() => {
                        setActiveSessionId(null);
                        setChatMessages([
                          {
                            id: "msg-welcome",
                            role: "assistant",
                            content: `Chào bạn! Tôi là Virtual Tutor hỗ trợ học tập cho học phần **${course?.name || courseId}**. Hãy bắt đầu cuộc hội thoại mới bằng cách đặt câu hỏi.`,
                            timestamp: new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" }),
                          }
                        ]);
                      }}
                    >
                      <span className="material-symbols-outlined text-xs">add</span>
                      <span>Hội thoại mới</span>
                    </button>

                    <div className="space-y-1.5">
                      <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-wider px-1">Lịch sử thảo luận</span>
                      <div className="space-y-1">
                        {sessionsList.map(s => (
                          <div
                            key={s.id}
                            className={`group w-full text-left relative p-2.5 rounded-lg border text-xs transition-all flex flex-col gap-1 cursor-pointer ${
                              activeSessionId === s.id
                                ? "bg-hust-red/5 border-hust-red/20 text-hust-red font-bold"
                                : "bg-white border-whisper-border text-slate-700 hover:bg-canvas-base"
                            }`}
                            onClick={() => setActiveSessionId(s.id)}
                          >
                            <span className="truncate block font-semibold pr-6">
                              {s.summary || `Hội thoại ${new Date(s.created_at).toLocaleDateString()}`}
                            </span>
                            <span className="text-[9px] text-muted-steel font-mono">
                              {new Date(s.updated_at).toLocaleDateString()}
                            </span>
                            <button
                              className="absolute top-2 right-2 p-1 text-muted-steel hover:text-system-red opacity-0 group-hover:opacity-100 transition-opacity disabled:opacity-40"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteSession(s.id);
                              }}
                              disabled={deletingSession}
                              title="Xóa cuộc trò chuyện"
                            >
                              <X className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ))}
                        {sessionsList.length === 0 && (
                          <span className="block text-[11px] text-muted-steel italic px-2">Chưa có cuộc hội thoại nào.</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Chat Log (Right 75%) */}
                <div className="flex-1 flex flex-col h-full overflow-hidden">
                  <div className="flex-1 p-6 overflow-y-auto space-y-4">
                    {chatMessages.map((msg) => (
                      <div 
                        key={msg.id}
                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                      >
                        <div className={
                          msg.role === "user"
                            ? "max-w-[70%] min-w-0 p-4 rounded-xl border bg-[#FFF8F6] border-hust-red/20 text-charcoal-ink"
                            : "w-full min-w-0 text-charcoal-ink"
                        }>
                          <div className="flex items-center justify-between gap-6 mb-1 text-[10px] text-muted-steel font-bold">
                            <span className="uppercase tracking-wider">{msg.role === "user" ? "Sinh Viên" : "AI Tutor"}</span>
                            <span>{msg.timestamp}</span>
                          </div>
                          
                          {/* Message body: full Markdown + LaTeX + Mermaid rendering */}
                          <MarkdownRenderer content={msg.content} className="text-body-md leading-relaxed" />

                          {/* Citations references display footer */}
                          {msg.citations && msg.citations.length > 0 && (
                            <div className="mt-4 pt-3 border-t border-whisper-border space-y-1.5">
                              <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-widest">Nguồn đối chiếu:</span>
                              <div className="flex flex-wrap gap-2">
                                {msg.citations.map((cite: any, cIdx: number) => (
                                  <button 
                                    key={cIdx}
                                    className="text-[11px] bg-canvas-base hover:bg-hust-red/5 border border-whisper-border hover:border-hust-red/30 rounded px-2.5 py-1 text-left flex items-center gap-1.5 transition-colors"
                                    onClick={() => handleCitationClick(cite.document_id || cite.doc_id, cite.page_number)}
                                  >
                                    <FileCheck className="w-3 h-3 text-hust-red" />
                                    <span className="font-semibold text-charcoal-ink truncate max-w-[120px]">
                                      {cite.document_title || docsList.find(d => d.id === cite.document_id || d.id === cite.doc_id)?.title || "Tài liệu"}
                                    </span>
                                    <span className="text-muted-steel font-mono">Trang {cite.page_number}</span>
                                  </button>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Interrupted-stream warning: connection dropped before the answer
                              finished, so this text is partial, not a complete answer. */}
                          {msg.interrupted && (
                            <div className="mt-3 flex items-start gap-1.5 text-[11px] text-pear-yellow font-semibold">
                              <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-px" />
                              <span className="leading-relaxed">
                                Phản hồi bị gián đoạn giữa chừng do mất kết nối. Vui lòng gửi lại câu hỏi để nhận câu trả lời đầy đủ.
                              </span>
                            </div>
                          )}

                          {/* General-knowledge notice: assistant answer with no source citations */}
                          {msg.role === "assistant" &&
                            !msg.interrupted &&
                            (!msg.citations || msg.citations.length === 0) &&
                            msg.id !== "msg-welcome" &&
                            !msg.id.startsWith("msg-error-") && (
                            <div className="mt-3 flex items-start gap-1.5 text-[11px] text-muted-steel">
                              <Info className="w-3.5 h-3.5 shrink-0 mt-px" />
                              <span className="leading-relaxed">
                                Câu trả lời dựa trên kiến thức chung..
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                    {/* Live streaming assistant answer (flows in token-by-token) */}
                    {streamingText && (
                      <div className="flex justify-start">
                        <div className="w-full min-w-0 text-charcoal-ink">
                          <div className="flex items-center justify-between gap-6 mb-1 text-[10px] text-muted-steel font-bold">
                            <span className="uppercase tracking-wider">AI Tutor</span>
                          </div>
                          <MarkdownRenderer content={streamingText} className="text-body-md leading-relaxed" />
                        </div>
                      </div>
                    )}

                    {/* Thinking indicator: dynamic agent status block, or generic "..." */}
                    {isTyping && !streamingText && (
                      <div className="flex justify-start">
                        <div className="bg-white border border-whisper-border p-4 rounded-xl">
                          <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-wider mb-2">AI Tutor</span>
                          {agentStatus ? (
                            <div className="flex items-center gap-2.5">
                              <span className="w-4 h-4 border-2 border-hust-red border-t-transparent rounded-full animate-spin shrink-0"></span>
                              <span className="text-body-sm font-semibold text-charcoal-ink">{agentStatus}</span>
                            </div>
                          ) : (
                            <div className="flex items-center gap-1">
                              <span className="w-2 h-2 rounded-full bg-muted-steel animate-bounce" style={{ animationDelay: "0ms" }}></span>
                              <span className="w-2 h-2 rounded-full bg-muted-steel animate-bounce" style={{ animationDelay: "150ms" }}></span>
                              <span className="w-2 h-2 rounded-full bg-muted-steel animate-bounce" style={{ animationDelay: "300ms" }}></span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                    <div ref={chatEndRef} />
                  </div>

                  {/* Input Text Form Area */}
                  <div className="p-4 border-t border-whisper-border bg-white flex gap-3">
                    <input 
                      className="flex-1 bg-[#F8FAFC] border-1.5 border-whisper-border rounded-xl px-4 py-3 text-body-md outline-none focus:ring-2 focus:ring-hust-red focus:border-hust-red transition-all"
                      placeholder="Nhập câu hỏi thảo luận về môn học này..."
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyDown={(e) => { if (e.key === "Enter") handleSendChat(); }}
                    />
                    <button 
                      className="tactile-button tactile-button-primary px-5"
                      onClick={handleSendChat}
                      disabled={isTyping}
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: DUAL-TAB / SPLIT-VIEW DOCUMENT VIEWER */}
            {activeTab === "viewer" && (
              <div className="h-full flex flex-col overflow-hidden bg-white">
                {viewerDoc ? (
                  <>
                    <header className="flex justify-between items-center bg-canvas-base border-b border-whisper-border px-6 py-2.5">
                      <div className="min-w-0">
                        <span className="block font-display font-extrabold text-body-sm text-charcoal-ink truncate">{viewerDoc.title}</span>
                        <span className="block text-[10px] text-muted-steel font-mono">{viewerDoc.filename} ({viewerDoc.file_type})</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {/* Community vote tallies — interactive for students, read-only otherwise */}
                        {viewerDoc.status === "INDEXED" && (() => {
                          const canVote = currentUser?.role === "student";
                          return (
                            <div className="flex items-center gap-1 mr-1">
                              <button
                                className={`tactile-button text-xs py-1.5 px-2.5 flex items-center gap-1.5 ${
                                  viewerVote === "up" ? "!bg-system-green/10 !border-system-green !border-b-system-green !text-system-green" : ""
                                } ${canVote ? "" : "cursor-default"}`}
                                onClick={() => canVote && handleVote("up")}
                                disabled={isVoting || !canVote}
                                title={canVote ? "Đánh dấu tài liệu hữu ích" : "Số lượt đánh giá hữu ích"}
                              >
                                <ThumbsUp className="w-3.5 h-3.5" />
                                <span>{voteCounts.up}</span>
                              </button>
                              <button
                                className={`tactile-button text-xs py-1.5 px-2.5 flex items-center gap-1.5 ${
                                  viewerVote === "down" ? "!bg-system-red/10 !border-system-red !border-b-system-red !text-system-red" : ""
                                } ${canVote ? "" : "cursor-default"}`}
                                onClick={() => canVote && handleVote("down")}
                                disabled={isVoting || !canVote}
                                title={canVote ? "Đánh dấu tài liệu chưa tốt" : "Số lượt đánh giá chưa tốt"}
                              >
                                <ThumbsDown className="w-3.5 h-3.5" />
                                <span>{voteCounts.down}</span>
                              </button>
                            </div>
                          );
                        })()}
                        <div className="flex items-center gap-1">
                          <button
                            className={`tactile-button text-xs py-1.5 px-3.5 ${viewMode === "ocr" ? "!bg-hust-red/10 !border-hust-red !border-b-hust-red !text-hust-red" : ""}`}
                            onClick={() => setViewMode("ocr")}
                          >
                            Bản đã xử lý
                          </button>
                          <button
                            className={`tactile-button text-xs py-1.5 px-3.5 ${viewMode === "split" ? "!bg-hust-red/10 !border-hust-red !border-b-hust-red !text-hust-red" : ""}`}
                            onClick={() => setViewMode("split")}
                          >
                            Xem đối chiếu
                          </button>
                          <button
                            className={`tactile-button text-xs py-1.5 px-3.5 ${viewMode === "original" ? "!bg-hust-red/10 !border-hust-red !border-b-hust-red !text-hust-red" : ""}`}
                            onClick={() => setViewMode("original")}
                          >
                            Tài liệu gốc
                          </button>
                        </div>
                      </div>
                    </header>

                    <div className="flex-1 flex overflow-hidden">
                      {/* Left side: Markdown OCR translation content */}
                      {viewMode !== "original" && (
                        <div className={`${viewMode === "split" ? "w-1/2" : "w-full"} h-full overflow-y-auto p-8 border-r border-whisper-border`}>
                          <div className="space-y-4">
                            <span className="text-[10px] bg-system-green/10 text-system-green font-bold px-2 py-0.5 rounded border border-system-green/20">OCR Normalized Content</span>
                            <MarkdownRenderer content={viewerMarkdown || `# ${viewerDoc.title}\n\nNội dung văn bản gốc chưa trích xuất hoặc đang chạy tiến trình tự động.`} />
                          </div>
                        </div>
                      )}

                      {/* Right side: Original PDF URL / Image Preview */}
                      {viewMode !== "ocr" && (
                        <div className={`${viewMode === "split" ? "w-1/2" : "w-full"} h-full bg-slate-100 flex flex-col border-l border-whisper-border relative overflow-hidden`}>
                          {viewerRawUrl ? (
                            isImageDoc(viewerDoc) ? (
                              <div className="flex-1 flex flex-col relative overflow-hidden select-none">
                                {/* Image Zoom Controls */}
                                <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 flex items-center gap-2 bg-white/90 backdrop-blur border border-whisper-border px-3 py-1.5 rounded-full shadow-md">
                                  <button
                                    onClick={handleZoomOut}
                                    className="p-1 hover:bg-slate-200 rounded transition-colors text-charcoal-ink"
                                    title="Thu nhỏ"
                                  >
                                    <ZoomOut className="w-4 h-4" />
                                  </button>
                                  <span className="text-xs font-mono font-bold text-charcoal-ink min-w-[36px] text-center">
                                    {Math.round(imgScale * 100)}%
                                  </span>
                                  <button
                                    onClick={handleZoomIn}
                                    className="p-1 hover:bg-slate-200 rounded transition-colors text-charcoal-ink"
                                    title="Phóng to"
                                  >
                                    <ZoomIn className="w-4 h-4" />
                                  </button>
                                  <div className="w-[1px] h-3.5 bg-slate-300 mx-1" />
                                  <button
                                    onClick={handleZoomReset}
                                    className="p-1 hover:bg-slate-200 rounded transition-colors text-charcoal-ink"
                                    title="Đặt lại"
                                  >
                                    <Maximize2 className="w-4 h-4" />
                                  </button>
                                </div>

                                {/* Drag-to-pan Canvas Container */}
                                <div 
                                  ref={imgContainerRef}
                                  className="flex-1 overflow-hidden flex items-center justify-center p-8 bg-slate-200 relative cursor-grab active:cursor-grabbing"
                                  onMouseDown={handleImgMouseDown}
                                  onMouseMove={handleImgMouseMove}
                                  onMouseUp={handleImgMouseUp}
                                  onMouseLeave={handleImgMouseUp}
                                >
                                  <img 
                                    src={viewerRawUrl} 
                                    alt={viewerDoc.title} 
                                    style={{
                                      transform: `translate(${imgPosition.x}px, ${imgPosition.y}px) scale(${imgScale})`,
                                      transformOrigin: "center center",
                                      transition: imgIsDragging ? "none" : "transform 0.15s ease-out"
                                    }}
                                    className="max-w-full max-h-full object-contain pointer-events-none shadow-lg rounded"
                                  />
                                </div>
                              </div>
                            ) : (
                              <iframe 
                                src={viewerRawUrl} 
                                className="w-full h-full border-0"
                                title="Tài liệu gốc PDF"
                              />
                            )
                          ) : (
                            <div className="m-auto text-center space-y-4 p-8">
                              <BookOpen className="w-16 h-16 text-muted-steel mx-auto" />
                              <h3 className="text-body-lg font-bold text-charcoal-ink">Bản Gốc Tài Liệu</h3>
                              <p className="text-body-sm text-muted-steel leading-relaxed">
                                Đang chuẩn bị tải liên kết PDF gốc từ bộ lưu trữ...
                              </p>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </>
                ) : (
                  <div className="flex flex-col items-center justify-center h-full text-center p-8">
                    <FileText className="w-16 h-16 text-muted-steel mb-4" />
                    <h3 className="text-body-lg font-bold text-charcoal-ink">Chưa chọn tài liệu xem</h3>
                    <p className="text-body-sm text-muted-steel mt-1">Vui lòng click vào các tài liệu trong danh sách bên trái để mở.</p>
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: CONCEPT NETWORK MINDMAP */}
            {activeTab === "mindmap" && (
              <CourseMindmap
                nodes={mindmapGraph.nodes}
                edges={mindmapGraph.edges}
                loading={mindmapLoading}
                sourceCount={docsList.filter((d) => isViewable(d.status)).length}
                onUpload={() => setShowUploadModal(true)}
                onAskTutor={(label) => {
                  setInputText(`Giải thích chi tiết cho tôi về khái niệm "${label}"`);
                  setActiveTab("tutor");
                }}
              />
            )}

            {/* TAB 4: MOCK TEST PRACTICE */}
            {activeTab === "mocktest" && (
              <div className="h-full p-6 overflow-y-auto">
                {!testStarted ? (
                  <div className="max-w-xl mx-auto bg-white border-1.5 border-whisper-border rounded-2xl p-8 space-y-6">
                    <div className="text-center space-y-2">
                      <GraduationCap className="w-16 h-16 text-hust-red mx-auto" />
                      <h2 className="font-display font-extrabold text-xl text-charcoal-ink">Tạo đề thi thử tự động</h2>
                      <p className="text-body-sm text-muted-steel max-w-sm mx-auto">
                        Đề trắc nghiệm sinh ngẫu nhiên từ kho câu hỏi chất lượng cao của các tài liệu nguồn đã được duyệt.
                      </p>
                    </div>

                    <div className="space-y-4 pt-4 border-t border-whisper-border">
                      <div className="space-y-1.5">
                        <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">Độ khó đề thi</label>
                        <select 
                          className="w-full bg-[#F8FAFC] border border-whisper-border rounded-xl px-4 py-3 text-body-md"
                          value={testSettings.difficulty}
                          onChange={(e) => setTestSettings(prev => ({ ...prev, difficulty: e.target.value }))}
                        >
                          <option value="easy">Dễ (Kiến thức cơ bản)</option>
                          <option value="medium">Trung bình (Tổng hợp nội dung)</option>
                          <option value="hard">Khó (Vận dụng & Phân tích cấu trúc)</option>
                        </select>
                      </div>

                      <div className="space-y-1.5">
                        <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">Số lượng câu hỏi</label>
                        <select 
                          className="w-full bg-[#F8FAFC] border border-whisper-border rounded-xl px-4 py-3 text-body-md"
                          value={testSettings.count}
                          onChange={(e) => setTestSettings(prev => ({ ...prev, count: parseInt(e.target.value) }))}
                        >
                          <option value={3}>3 Câu hỏi nhanh</option>
                          <option value={5}>5 Câu hỏi tiêu chuẩn</option>
                          <option value={10}>10 Câu hỏi chuyên sâu</option>
                        </select>
                      </div>

                      <button
                        className="tactile-button tactile-button-primary w-full py-3.5 mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
                        onClick={generateMockQuiz}
                        disabled={!hasViewableDocs || generatingTest}
                      >
                        {generatingTest ? (
                          <span className="flex items-center justify-center gap-2">
                            <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                            Đang sinh đề thi thử...
                          </span>
                        ) : (
                          "Bắt đầu làm bài thi thử"
                        )}
                      </button>
                      {generatingTest && (
                        <p className="text-xs text-muted-steel text-center leading-relaxed -mt-1">
                          AI đang tạo câu hỏi từ tài liệu nguồn, quá trình này có thể mất tới một phút.
                        </p>
                      )}
                      {!hasViewableDocs && (
                        <p className="text-xs text-system-red text-center leading-relaxed -mt-1">
                          Chưa có câu hỏi cho môn học này. Vui lòng đóng góp tài liệu đã được duyệt để kích hoạt tính năng thi thử.
                        </p>
                      )}
                      {hasViewableDocs && noQuestionsAvailable && (
                        <p className="text-xs text-system-red text-center leading-relaxed -mt-1">
                          Chưa có câu hỏi cho môn học này. Vui lòng đóng góp tài liệu đã được duyệt để kích hoạt tính năng thi thử.
                        </p>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="max-w-2xl mx-auto space-y-6">
                    <header className="flex justify-between items-center bg-white border border-whisper-border rounded-xl px-5 py-3 shadow-sm">
                      <div className="flex items-center gap-2">
                        <Clock className="w-5 h-5 text-hust-red" />
                        <span className="font-mono font-bold text-charcoal-ink">
                          Thời gian còn lại: {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, "0")}
                        </span>
                      </div>
                      {!testSubmitted ? (
                        <button 
                          className="tactile-button tactile-button-primary text-xs py-1.5 px-4"
                          onClick={handleSubmittingTest}
                        >
                          Nộp bài làm
                        </button>
                      ) : (
                        <button 
                          className="tactile-button text-xs py-1.5 px-4"
                          onClick={() => setTestStarted(false)}
                        >
                          Tạo đề thi mới
                        </button>
                      )}
                    </header>

                    {/* List of quiz questions */}
                    <div className="space-y-6">
                      {questions.map((q, idx) => (
                        <div key={q.id} className="tactile-card space-y-4">
                          <h4 className="font-display font-extrabold text-body-lg text-charcoal-ink">
                            Câu {idx + 1}: {q.question}
                          </h4>

                          <div className="grid grid-cols-1 gap-2.5">
                            {q.options.map((opt: any) => {
                              const isSelected = selectedAnswers[idx] === opt.key;
                              const isCorrect = opt.key === q.correct;
                              let borderClass = "border-whisper-border hover:border-charcoal-ink";
                              let bgClass = "bg-white";

                              if (testSubmitted) {
                                if (isCorrect) {
                                  borderClass = "border-system-green bg-green-50";
                                } else if (isSelected) {
                                  borderClass = "border-system-red bg-red-50";
                                }
                              } else if (isSelected) {
                                borderClass = "border-hust-red bg-[#FEF2F2]";
                              }

                              return (
                                <button
                                  key={opt.key}
                                  className={`w-full text-left p-3.5 rounded-xl border-1.5 transition-all flex items-start gap-3 ${borderClass} ${bgClass}`}
                                  disabled={testSubmitted}
                                  onClick={() => setSelectedAnswers(prev => ({ ...prev, [idx]: opt.key }))}
                                >
                                  <span className={`font-mono font-bold border rounded w-6 h-6 flex items-center justify-center shrink-0 ${
                                    isSelected ? "border-hust-red bg-hust-red text-white" : "border-whisper-border bg-canvas-base"
                                  }`}>
                                    {opt.key}
                                  </span>
                                  <span className="text-body-md text-charcoal-ink">{opt.val}</span>
                                </button>
                              );
                            })}
                          </div>

                          {/* Justifications comments panel */}
                          {testSubmitted && (
                            <div className="p-4 bg-canvas-base border border-whisper-border rounded-xl space-y-2.5">
                              <div className="flex items-center gap-1.5">
                                {selectedAnswers[idx] === q.correct ? (
                                  <CheckCircle className="w-4.5 h-4.5 text-system-green shrink-0" />
                                ) : (
                                  <AlertCircle className="w-4.5 h-4.5 text-system-red shrink-0" />
                                )}
                                <span className="font-display font-extrabold text-xs">
                                  {selectedAnswers[idx] === q.correct ? "Trả lời chính xác" : "Trả lời chưa chính xác"}
                                </span>
                              </div>
                              <div>
                                <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-wider mb-0.5">Giải thích</span>
                                <p className="text-xs text-charcoal-ink leading-relaxed">{q.rationale}</p>
                              </div>
                              {q.citation?.excerpt && (
                                <div className="pt-2 border-t border-whisper-border">
                                  <span className="block text-[10px] font-bold text-muted-steel uppercase tracking-wider mb-1">Trích dẫn nguồn</span>
                                  <blockquote className="text-[11px] text-charcoal-ink italic border-l-2 border-hust-red/40 pl-2.5 leading-relaxed">
                                    “{q.citation.excerpt}”
                                  </blockquote>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>

                    {testSubmitted && questions.length > 0 && (
                      <div className="tactile-card bg-white text-center space-y-3">
                        <span className="text-xs uppercase tracking-widest text-muted-steel font-bold">Kết quả thi thử</span>
                        <div className="text-[48px] font-black text-hust-red">
                          {testScore} / {questions.length}
                        </div>
                        <p className="text-body-md font-semibold text-charcoal-ink">
                          {testScore === questions.length ? "Tuyệt vời! Bạn đã nắm vững toàn bộ kiến thức." : "Bạn hãy xem lại giải thích chi tiết ở các câu làm sai nhé."}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </section>
        </main>
      </div>

      {/* MODAL: Upload panel layout */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-[1px]">
          <div className="w-full max-w-[480px] bg-white border border-whisper-border rounded-2xl p-6 shadow-xl space-y-4 animate-in zoom-in-95 duration-100">
            <div className="flex justify-between items-center pb-2 border-b border-whisper-border">
              <div className="min-w-0 pr-2">
                <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink">Tải lên tài liệu mới</h3>
                {course && (
                  <p className="text-[11px] text-muted-steel mt-0.5 truncate">
                    Đóng góp cho học phần <span className="font-bold text-charcoal-ink">{course.course_code}</span> — {course.name}
                  </p>
                )}
              </div>
              <button onClick={() => { setShowUploadModal(false); setUploadConsent(false); setUploadErrors({}); }}>
                <X className="w-5 h-5 text-muted-steel" />
              </button>
            </div>

            <form onSubmit={handleUploadSubmit} className="space-y-4" noValidate>
              <div className="space-y-1">
                <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">Tên tài liệu hiển thị</label>
                <input
                  type="text"
                  className={`w-full bg-[#F8FAFC] border rounded-xl px-4 py-2.5 text-body-md focus:ring-2 focus:ring-hust-red focus:border-hust-red outline-none ${uploadErrors.title ? "border-system-red" : "border-whisper-border"}`}
                  placeholder="Ví dụ: Bài tập tuần 5 Quy hoạch động"
                  value={uploadTitle}
                  onChange={(e) => { setUploadTitle(e.target.value); if (uploadErrors.title) setUploadErrors(prev => ({ ...prev, title: undefined })); }}
                />
                {uploadErrors.title && (
                  <span className="block text-[11px] text-system-red font-semibold mt-1">{uploadErrors.title}</span>
                )}
              </div>

              <div className="space-y-1">
                <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider">Phân loại tài liệu</label>
                <select
                  className="w-full bg-[#F8FAFC] border border-whisper-border rounded-xl px-4 py-2.5 text-body-md"
                  value={uploadType}
                  onChange={(e) => setUploadType(e.target.value)}
                >
                  {currentUser?.role === "admin" || currentUser?.role === "reviewer" ? (
                    <>
                      <option value="syllabus">Đề Cương Học Phần</option>
                      <option value="textbook">Giáo Trình</option>
                      <option value="lecture_slides">Slide Bài Giảng</option>
                    </>
                  ) : (
                    <>
                      <option value="summary_note">Ghi Chú Tổng Hợp</option>
                      <option value="review_note">Ghi Chú Ôn Tập</option>
                      <option value="past_exam">Đề Thi / Bài Kiểm Tra</option>
                      <option value="solved_exercise">Bài Tập Có Lời Giải</option>
                    </>
                  )}
                </select>
              </div>

              <div className="space-y-1">
                <label className="block text-xs font-bold text-muted-steel uppercase tracking-wider font-display">Tệp tin (.pdf, .pptx, .png)</label>
                <div className="border-2 border-dashed border-whisper-border rounded-xl p-6 text-center hover:bg-canvas-base transition-colors cursor-pointer relative">
                  <input
                    type="file"
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    accept=".pdf,.pptx,.png,.jpg,.jpeg"
                    onChange={(e) => { setUploadFile(e.target.files?.[0] || null); if (uploadErrors.file) setUploadErrors(prev => ({ ...prev, file: undefined })); }}
                  />
                  <Upload className="w-8 h-8 text-muted-steel mx-auto mb-2" />
                  <span className="block text-xs font-bold text-charcoal-ink">
                    {uploadFile ? uploadFile.name : "Kéo thả hoặc nhấp để chọn tệp"}
                  </span>
                  <span className="block text-[10px] text-muted-steel mt-0.5">Dung lượng tối đa 30MB</span>
                </div>
                {uploadErrors.file && (
                  <span className="block text-[11px] text-system-red font-semibold mt-1">{uploadErrors.file}</span>
                )}
              </div>

              <div className="space-y-1">
                <label className="flex items-start gap-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    className="mt-0.5 accent-hust-red rounded shrink-0"
                    checked={uploadConsent}
                    onChange={(e) => { setUploadConsent(e.target.checked); if (uploadErrors.consent) setUploadErrors(prev => ({ ...prev, consent: undefined })); }}
                  />
                  <span className="text-[12px] text-charcoal-ink leading-relaxed">
                    Tôi xác nhận mình có quyền chia sẻ tài liệu này và đồng ý với chính sách sử dụng học thuật nội bộ.
                  </span>
                </label>
                {uploadErrors.consent && (
                  <span className="block text-[11px] text-system-red font-semibold mt-1">{uploadErrors.consent}</span>
                )}
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  className="tactile-button bg-white border border-whisper-border text-charcoal-ink flex-1 py-2"
                  onClick={() => { setShowUploadModal(false); setUploadConsent(false); setUploadErrors({}); }}
                >
                  Hủy bỏ
                </button>
                <button
                  type="submit"
                  disabled={uploadingDoc}
                  className="tactile-button tactile-button-primary flex-1 py-2 disabled:opacity-60"
                >
                  {uploadingDoc ? "Đang tải lên..." : "Tải lên tài liệu"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </AppShell>
  );
}
