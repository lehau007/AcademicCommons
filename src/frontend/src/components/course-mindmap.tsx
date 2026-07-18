/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ZoomIn, ZoomOut, Maximize2, Download, X, Upload, Network } from "lucide-react";

// --- Types -----------------------------------------------------------------
interface RawNode {
  id: string;
  label: string;
  topic?: string;
  level?: number;
  [k: string]: any;
}
interface RawEdge {
  source: string;
  target: string;
  relation?: string;
}
interface Positioned extends RawNode {
  depth: number;
  x: number;
  y: number; // vertical center
  w: number;
  hasChildren: boolean;
  collapsed: boolean;
}

interface Props {
  nodes: RawNode[];
  edges: RawEdge[];
  sourceCount?: number;
  loading?: boolean;
  onAskTutor: (label: string) => void;
  onUpload: () => void;
}

// --- Layout constants ------------------------------------------------------
const NODE_H = 38;
const ROW_H = 56;
const X_GAP = 240;
const CHAR_W = 6.6;
const PAD_X = 34;

function pillWidth(label: string): number {
  return Math.min(Math.max(label.length * CHAR_W + PAD_X, 96), 230);
}
function truncate(label: string): string {
  return label.length > 30 ? `${label.slice(0, 29)}…` : label;
}

const CTRL_BTN =
  "w-9 h-9 flex items-center justify-center bg-white border border-whisper-border rounded-lg shadow-sm text-charcoal-ink hover:bg-canvas-base hover:border-charcoal-ink transition-colors";

export default function CourseMindmap({ nodes, edges, sourceCount, loading, onAskTutor, onUpload }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState({ x: 0, y: 0, k: 1 });
  // Explicit per-node overrides (true = collapsed, false = expanded). Absence = default rule.
  const [userToggle, setUserToggle] = useState<Map<string, boolean>>(new Map());
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // adjacency + lookups
  const childrenMap = useMemo(() => {
    const m = new Map<string, string[]>();
    for (const e of edges) {
      if (!m.has(e.source)) m.set(e.source, []);
      m.get(e.source)!.push(e.target);
    }
    return m;
  }, [edges]);

  const nodeById = useMemo(() => new Map(nodes.map((n) => [n.id, n])), [nodes]);

  const rootId = useMemo(() => {
    if (nodes.length === 0) return null;
    const lvl0 = nodes.find((n) => n.level === 0);
    if (lvl0) return lvl0.id;
    const targets = new Set(edges.map((e) => e.target));
    return (nodes.find((n) => !targets.has(n.id)) ?? nodes[0]).id;
  }, [nodes, edges]);

  // BFS depth (full tree, ignoring collapse) for default-collapse + colouring
  const depthMap = useMemo(() => {
    const d = new Map<string, number>();
    if (!rootId) return d;
    const queue: Array<[string, number]> = [[rootId, 0]];
    while (queue.length) {
      const [id, depth] = queue.shift()!;
      if (d.has(id)) continue;
      d.set(id, depth);
      for (const c of childrenMap.get(id) ?? []) {
        if (!d.has(c)) queue.push([c, depth + 1]);
      }
    }
    return d;
  }, [rootId, childrenMap]);

  // Default view: root + level-1 visible, everything deeper folded behind chevrons.
  // A node is collapsed if the user toggled it, otherwise by the depth>=1 default rule.
  const isCollapsed = useCallback(
    (id: string) => {
      if (userToggle.has(id)) return userToggle.get(id)!;
      const depth = depthMap.get(id) ?? 0;
      const hasKids = (childrenMap.get(id)?.length ?? 0) > 0;
      return depth >= 1 && hasKids;
    },
    [userToggle, depthMap, childrenMap],
  );

  // Tidy horizontal-tree layout respecting collapsed nodes.
  const layout = useMemo(() => {
    const positioned: Positioned[] = [];
    const result = new Map<string, Positioned>();
    if (!rootId) return { nodes: positioned, result, width: 0, height: 0 };

    const visited = new Set<string>();
    let leaf = 0;

    function dfs(id: string, depth: number): number {
      if (visited.has(id)) return leaf * ROW_H + NODE_H;
      visited.add(id);
      const node = nodeById.get(id);
      if (!node) return leaf * ROW_H + NODE_H;

      const kids = (childrenMap.get(id) ?? []).filter((c) => nodeById.has(c));
      const collapsed = isCollapsed(id);

      let y: number;
      if (kids.length === 0 || collapsed) {
        y = leaf * ROW_H + NODE_H;
        leaf += 1;
      } else {
        const ys = kids.map((k) => dfs(k, depth + 1));
        y = (ys[0] + ys[ys.length - 1]) / 2;
      }

      const p: Positioned = {
        ...node,
        depth,
        x: depth * X_GAP,
        y,
        w: pillWidth(truncate(node.label)),
        hasChildren: kids.length > 0,
        collapsed,
      };
      result.set(id, p);
      positioned.push(p);
      return y;
    }

    dfs(rootId, 0);

    const width = Math.max(...positioned.map((p) => p.x + p.w), 0) + 40;
    const height = Math.max(...positioned.map((p) => p.y), 0) + NODE_H + 20;
    return { nodes: positioned, result, width, height };
  }, [rootId, childrenMap, nodeById, isCollapsed]);

  const links = useMemo(() => {
    const out: Array<{ from: Positioned; to: Positioned }> = [];
    for (const p of layout.nodes) {
      if (p.collapsed) continue;
      for (const cid of childrenMap.get(p.id) ?? []) {
        const c = layout.result.get(cid);
        if (c) out.push({ from: p, to: c });
      }
    }
    return out;
  }, [layout, childrenMap]);

  // --- Fit-to-view ---------------------------------------------------------
  const fit = useCallback(() => {
    const el = containerRef.current;
    if (!el || layout.nodes.length === 0) return;
    const cw = el.clientWidth;
    const ch = el.clientHeight;
    const pad = 48;
    const k = Math.max(Math.min((cw - pad * 2) / layout.width, (ch - pad * 2) / layout.height, 1.1), 0.2);
    setTransform({ x: (cw - layout.width * k) / 2, y: (ch - layout.height * k) / 2, k });
  }, [layout.width, layout.height, layout.nodes.length]);

  // Auto-fit only when the underlying graph changes (not on collapse/pan).
  const fittedRef = useRef<RawNode[] | null>(null);
  useEffect(() => {
    if (fittedRef.current !== nodes) {
      fittedRef.current = nodes;
      // wait a frame so the container has its measured size
      requestAnimationFrame(fit);
    }
  }, [nodes, fit]);

  // --- Pan & zoom ----------------------------------------------------------
  const panState = useRef<{ active: boolean; x: number; y: number }>({ active: false, x: 0, y: 0 });

  const onPointerDown = (e: React.PointerEvent) => {
    if ((e.target as HTMLElement).closest("[data-node]")) return; // let nodes handle their own clicks
    panState.current = { active: true, x: e.clientX, y: e.clientY };
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
  };
  const onPointerMove = (e: React.PointerEvent) => {
    if (!panState.current.active) return;
    const dx = e.clientX - panState.current.x;
    const dy = e.clientY - panState.current.y;
    panState.current.x = e.clientX;
    panState.current.y = e.clientY;
    setTransform((t) => ({ ...t, x: t.x + dx, y: t.y + dy }));
  };
  const onPointerUp = () => {
    panState.current.active = false;
  };

  const onWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const el = containerRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const cx = e.clientX - rect.left;
    const cy = e.clientY - rect.top;
    setTransform((t) => {
      const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      const k = Math.max(0.2, Math.min(2.5, t.k * factor));
      // zoom toward cursor
      const x = cx - ((cx - t.x) * k) / t.k;
      const y = cy - ((cy - t.y) * k) / t.k;
      return { x, y, k };
    });
  };

  const zoomBy = useCallback(
    (factor: number) =>
      setTransform((t) => {
        const el = containerRef.current;
        const cx = el ? el.clientWidth / 2 : 0;
        const cy = el ? el.clientHeight / 2 : 0;
        const k = Math.max(0.2, Math.min(2.5, t.k * factor));
        return { x: cx - ((cx - t.x) * k) / t.k, y: cy - ((cy - t.y) * k) / t.k, k };
      }),
    [],
  );

  const toggle = (id: string) =>
    setUserToggle((prev) => {
      const next = new Map(prev);
      next.set(id, !isCollapsed(id));
      return next;
    });

  const selected = selectedId ? layout.result.get(selectedId) ?? null : null;

  const downloadSvg = useCallback(() => {
    const svg = containerRef.current?.querySelector("svg");
    if (!svg) return;
    const clone = svg.cloneNode(true) as SVGElement;
    clone.setAttribute("viewBox", `0 0 ${layout.width} ${layout.height}`);
    clone.setAttribute("width", String(layout.width));
    clone.setAttribute("height", String(layout.height));
    const g = clone.querySelector("g");
    if (g) g.removeAttribute("transform");
    const blob = new Blob([new XMLSerializer().serializeToString(clone)], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "mindmap.svg";
    a.click();
    URL.revokeObjectURL(url);
  }, [layout.width, layout.height]);

  // Colour by depth — HUST red root, pear-yellow topics, slate concepts.
  const styleFor = (p: Positioned) => {
    if (p.depth === 0) return { fill: "#990000", stroke: "#0F172A", text: "#FFFFFF", bold: true };
    if (p.depth === 1) return { fill: "#FFFFFF", stroke: "#F59E0B", text: "#0F172A", bold: true };
    return { fill: "#FFFFFF", stroke: "#E2E8F0", text: "#0F172A", bold: false };
  };

  // --- Loading state -------------------------------------------------------
  if (loading && nodes.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center p-8 bg-white">
        <div className="w-10 h-10 border-4 border-hust-red border-t-transparent rounded-full animate-spin mb-4"></div>
        <h3 className="text-body-lg font-bold text-charcoal-ink">Đang tạo mindmap...</h3>
        <p className="text-body-sm text-muted-steel mt-1 max-w-sm leading-relaxed">
          AI đang tổng hợp khái niệm từ các tài liệu đã duyệt của môn học.
        </p>
      </div>
    );
  }

  // --- Empty state ---------------------------------------------------------
  if (nodes.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-center p-8 bg-white">
        <Network className="w-16 h-16 text-muted-steel mb-4" />
        <h3 className="text-body-lg font-bold text-charcoal-ink">Chưa có mindmap</h3>
        <p className="text-body-sm text-muted-steel mt-1 max-w-sm leading-relaxed">
          Chưa có tài liệu nào được duyệt để tạo mindmap. Hãy đóng góp tài liệu đầu tiên cho môn học này!
        </p>
        <button className="tactile-button tactile-button-primary mt-5 flex items-center gap-2 px-5 py-2.5" onClick={onUpload}>
          <Upload className="w-4 h-4" />
          <span>Tải lên tài liệu mới</span>
        </button>
      </div>
    );
  }

  return (
    <div className="h-full flex overflow-hidden relative">
      <div ref={containerRef} className="flex-1 h-full bg-white relative overflow-hidden">
        {/* Header chip */}
        <div className="absolute top-4 left-4 z-10 flex items-center gap-2">
          <span className="bg-white/85 backdrop-blur-sm border border-whisper-border px-3 py-1.5 rounded-lg text-sm font-bold text-charcoal-ink shadow-sm">
            AI Mindmap
          </span>
          {typeof sourceCount === "number" && sourceCount > 0 && (
            <span className="bg-white/85 backdrop-blur-sm border border-whisper-border px-2.5 py-1.5 rounded-lg text-xs text-muted-steel shadow-sm">
              Xem {sourceCount} nguồn
            </span>
          )}
        </div>

        {/* Legend */}
        <div className="absolute bottom-4 left-4 z-10 bg-white/85 backdrop-blur-sm border border-whisper-border p-3 rounded-lg text-xs space-y-1.5 shadow-sm">
          <span className="font-bold text-charcoal-ink block">Chú giải:</span>
          <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-hust-red"></span><span>Học phần chính</span></div>
          <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-pear-yellow"></span><span>Chủ đề trọng tâm</span></div>
          <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-slate-400"></span><span>Khái niệm phụ thuộc</span></div>
        </div>

        {/* Controls */}
        <div className="absolute top-4 right-4 z-10 flex flex-col gap-1.5">
          <button title="Phóng to" onClick={() => zoomBy(1.2)} className={CTRL_BTN}>
            <ZoomIn className="w-4 h-4" />
          </button>
          <button title="Thu nhỏ" onClick={() => zoomBy(1 / 1.2)} className={CTRL_BTN}>
            <ZoomOut className="w-4 h-4" />
          </button>
          <button title="Vừa màn hình" onClick={fit} className={CTRL_BTN}>
            <Maximize2 className="w-4 h-4" />
          </button>
          <button title="Tải SVG" onClick={downloadSvg} className={CTRL_BTN}>
            <Download className="w-4 h-4" />
          </button>
        </div>

        <svg
          className="w-full h-full touch-none select-none cursor-grab active:cursor-grabbing"
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerLeave={onPointerUp}
          onWheel={onWheel}
        >
          <g transform={`translate(${transform.x},${transform.y}) scale(${transform.k})`}>
            {/* Connectors (curved) */}
            {links.map(({ from, to }, idx) => {
              const x1 = from.x + from.w;
              const y1 = from.y;
              const x2 = to.x;
              const y2 = to.y;
              const mx = (x1 + x2) / 2;
              return (
                <path
                  key={idx}
                  d={`M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`}
                  fill="none"
                  stroke="#CBD5E1"
                  strokeWidth={2}
                />
              );
            })}

            {/* Nodes */}
            {layout.nodes.map((p) => {
              const s = styleFor(p);
              return (
                <g key={p.id} data-node className="cursor-pointer">
                  <rect
                    x={p.x}
                    y={p.y - NODE_H / 2}
                    width={p.w}
                    height={NODE_H}
                    rx={10}
                    fill={s.fill}
                    stroke={s.stroke}
                    strokeWidth={p.depth === 0 ? 1.5 : 1.5}
                    className="transition-[filter] hover:brightness-95"
                    onClick={() => setSelectedId(p.id)}
                  />
                  <text
                    x={p.x + (p.hasChildren ? p.w / 2 - 6 : p.w / 2)}
                    y={p.y + 4}
                    textAnchor="middle"
                    fontSize={11}
                    fontWeight={s.bold ? 700 : 500}
                    fill={s.text}
                    style={{ pointerEvents: "none" }}
                  >
                    {truncate(p.label)}
                  </text>
                  <title>{p.label}</title>

                  {/* Expand / collapse chevron */}
                  {p.hasChildren && (
                    <g
                      onClick={(e) => {
                        e.stopPropagation();
                        toggle(p.id);
                      }}
                    >
                      <circle
                        cx={p.x + p.w}
                        cy={p.y}
                        r={9}
                        fill={p.depth === 0 ? "#990000" : "#FFFFFF"}
                        stroke={p.depth === 0 ? "#0F172A" : "#94A3B8"}
                        strokeWidth={1.25}
                      />
                      <text
                        x={p.x + p.w}
                        y={p.y + 4}
                        textAnchor="middle"
                        fontSize={12}
                        fontWeight={700}
                        fill={p.depth === 0 ? "#FFFFFF" : "#64748B"}
                        style={{ pointerEvents: "none" }}
                      >
                        {p.collapsed ? "›" : "‹"}
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </g>
        </svg>
      </div>

      {/* Detail drawer */}
      {selected && (
        <div className="w-80 border-l border-whisper-border bg-white p-6 overflow-y-auto space-y-4 shadow-lg animate-in slide-in-from-right duration-200">
          <div className="flex justify-between items-start">
            <h3 className="font-display font-extrabold text-[18px] text-charcoal-ink">{selected.label}</h3>
            <button className="text-muted-steel hover:text-charcoal-ink" onClick={() => setSelectedId(null)}>
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="h-[1px] bg-whisper-border"></div>
          <div>
            <span className="text-[10px] font-bold text-muted-steel uppercase tracking-widest block mb-1">Mô tả chủ đề</span>
            <p className="text-body-sm text-charcoal-ink leading-relaxed">
              {selected.topic || (selected.depth === 0 ? "Học phần cốt lõi" : "Khái niệm thuộc học phần")}
            </p>
          </div>
          <div>
            <span className="text-[10px] font-bold text-muted-steel uppercase tracking-widest block mb-1">Phân cấp</span>
            <div className="flex items-center gap-1.5">
              <span
                className={`w-2.5 h-2.5 rounded-full ${
                  selected.depth === 0 ? "bg-hust-red" : selected.depth === 1 ? "bg-pear-yellow" : "bg-slate-400"
                }`}
              ></span>
              <span className="text-body-sm font-semibold">
                {selected.depth === 0 ? "Học phần chính" : selected.depth === 1 ? "Chủ đề trọng tâm" : "Khái niệm phụ thuộc"}
              </span>
            </div>
          </div>
          <button
            className="tactile-button text-xs py-2 w-full mt-4"
            onClick={() => {
              onAskTutor(selected.label);
              setSelectedId(null);
            }}
          >
            Hỏi AI Tutor về khái niệm này
          </button>
        </div>
      )}
    </div>
  );
}
