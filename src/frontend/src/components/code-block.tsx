"use client";

import { useState, type ReactNode } from "react";
import { Check, Copy } from "lucide-react";

/**
 * Human-friendly display names for the languages we expect from the AI Tutor
 * and the OCR pipeline. Keyed by the token after the ``` fence
 * (e.g. ```python -> "python"). Unknown tokens fall back to a capitalized
 * version of the raw token, matching ChatGPT's "show the language" behaviour.
 */
const LANGUAGE_LABELS: Record<string, string> = {
  c: "C",
  h: "C",
  cpp: "C++",
  "c++": "C++",
  cc: "C++",
  hpp: "C++",
  cs: "C#",
  csharp: "C#",
  py: "Python",
  python: "Python",
  js: "JavaScript",
  javascript: "JavaScript",
  jsx: "JavaScript",
  ts: "TypeScript",
  typescript: "TypeScript",
  tsx: "TypeScript",
  java: "Java",
  go: "Go",
  golang: "Go",
  rs: "Rust",
  rust: "Rust",
  rb: "Ruby",
  ruby: "Ruby",
  php: "PHP",
  sh: "Bash",
  bash: "Bash",
  shell: "Shell",
  zsh: "Zsh",
  console: "Shell",
  ps1: "PowerShell",
  powershell: "PowerShell",
  sql: "SQL",
  json: "JSON",
  yaml: "YAML",
  yml: "YAML",
  toml: "TOML",
  ini: "INI",
  xml: "XML",
  html: "HTML",
  css: "CSS",
  scss: "SCSS",
  md: "Markdown",
  markdown: "Markdown",
  dockerfile: "Dockerfile",
  docker: "Dockerfile",
  makefile: "Makefile",
  make: "Makefile",
  kt: "Kotlin",
  kotlin: "Kotlin",
  swift: "Swift",
  r: "R",
  matlab: "MATLAB",
  m: "MATLAB",
  scala: "Scala",
  dart: "Dart",
  lua: "Lua",
  perl: "Perl",
  pl: "Perl",
  diff: "Diff",
  graphql: "GraphQL",
  text: "Text",
  plaintext: "Text",
};

export function getLanguageLabel(lang: string): string {
  const key = lang.toLowerCase().trim();
  if (LANGUAGE_LABELS[key]) return LANGUAGE_LABELS[key];
  if (!key) return "Text";
  return key.charAt(0).toUpperCase() + key.slice(1);
}

/** Recursively flatten React children into plain text for the copy button. */
export function nodeToText(node: ReactNode): string {
  if (node == null || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(nodeToText).join("");
  if (typeof node === "object" && "props" in node) {
    return nodeToText((node as { props: { children?: ReactNode } }).props.children);
  }
  return "";
}

export default function CodeBlock({
  language,
  children,
}: {
  language: string;
  /** The highlighted <code> element produced by react-markdown + rehype-highlight. */
  children: ReactNode;
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(nodeToText(children));
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      /* clipboard blocked — fail silently */
    }
  };

  return (
    <div className="not-prose my-4 overflow-hidden rounded-xl border border-charcoal-ink/15 bg-[#0d1117] shadow-sm">
      <div className="flex items-center justify-between border-b border-white/10 bg-[#161b22] px-4 py-2">
        <span className="font-mono text-xs font-semibold tracking-wide text-slate-300">
          {getLanguageLabel(language)}
        </span>
        <button
          type="button"
          onClick={handleCopy}
          className="flex items-center gap-1.5 rounded-md px-2 py-1 font-mono text-xs text-slate-400 transition-colors hover:bg-white/10 hover:text-slate-100"
          aria-label={copied ? "Đã sao chép" : "Sao chép mã"}
        >
          {copied ? (
            <>
              <Check className="h-3.5 w-3.5 text-system-green" />
              Đã sao chép
            </>
          ) : (
            <>
              <Copy className="h-3.5 w-3.5" />
              Sao chép
            </>
          )}
        </button>
      </div>
      <div className="overflow-x-auto">
        <pre className="hljs m-0 bg-transparent px-4 py-3.5 text-[13px] leading-relaxed">
          {children}
        </pre>
      </div>
    </div>
  );
}
