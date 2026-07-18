"use client";

import { useEffect, useId, useState } from "react";
import mermaid from "mermaid";

let initialized = false;

function ensureInit() {
  if (initialized) return;
  mermaid.initialize({
    startOnLoad: false,
    theme: "neutral",
    securityLevel: "strict",
    fontFamily: "inherit",
  });
  initialized = true;
}

export default function MermaidDiagram({ chart }: { chart: string }) {
  const reactId = useId();
  const [svg, setSvg] = useState<string>("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    let cancelled = false;
    ensureInit();
    // Mermaid requires a DOM-safe id (no colons from useId()).
    const id = `mermaid-${reactId.replace(/[^a-zA-Z0-9]/g, "")}`;
    mermaid
      .render(id, chart.trim())
      .then(({ svg }) => {
        if (!cancelled) {
          setSvg(svg);
          setError("");
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err?.message || "Không thể hiển thị sơ đồ Mermaid.");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [chart, reactId]);

  if (error) {
    return (
      <div className="my-3 border border-system-red/30 rounded-lg bg-system-red/5 p-3">
        <p className="text-xs font-bold text-system-red mb-1">Lỗi sơ đồ Mermaid</p>
        <pre className="text-[11px] text-muted-steel whitespace-pre-wrap font-mono overflow-x-auto">
          {chart.trim()}
        </pre>
      </div>
    );
  }

  return (
    <div
      className="my-3 flex justify-center overflow-x-auto rounded-lg border border-whisper-border bg-canvas-base p-3 [&_svg]:max-w-full [&_svg]:h-auto"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}
