"use client";

import type { ReactElement, ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";
import "katex/dist/katex.min.css";
import MermaidDiagram from "./mermaid-diagram";
import CodeBlock, { nodeToText } from "./code-block";

/**
 * Renders Markdown produced by the OCR pipeline and the AI Tutor.
 * Supports GFM (tables, lists, task lists), LaTeX math ($...$ / $$...$$)
 * via KaTeX, per-language syntax highlighting via highlight.js, and
 * ```mermaid fenced code blocks rendered as live diagrams.
 */
export default function MarkdownRenderer({
  content,
  className = "",
}: {
  content: string;
  className?: string;
}) {
  return (
    <div
      className={`prose prose-slate max-w-none min-w-0 prose-headings:font-display prose-a:text-hust-red prose-code:before:content-none prose-code:after:content-none break-words ${className}`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[
          rehypeKatex,
          // Only highlight blocks that DECLARE a language (detect: false).
          // Auto-detection mislabels plain text / ASCII diagrams as SQL, R, etc.
          // `ignoreMissing` keeps unknown declared languages (e.g. ```pseudocode)
          // from throwing; they render uncolored but still styled.
          [rehypeHighlight, { ignoreMissing: true, detect: false }],
        ]}
        components={{
          // Inline code only — block code is handled by the `pre` renderer
          // below, so here we just style the inline `code` chip.
          code(props) {
            const { className: codeClassName, children, ...rest } = props;
            // A fenced block is either highlighted (hljs / language- class) or,
            // for a language-less fence (e.g. ASCII art), a multi-line string.
            // Inline code is always single-line and unclassed. Detecting the
            // newline keeps language-less blocks out of the inline-chip style.
            const isFenced =
              (codeClassName && /\bhljs\b|language-/.test(codeClassName)) ||
              nodeToText(children).includes("\n");
            if (isFenced) {
              // Pass through untouched so the highlight.js spans and our
              // CodeBlock wrapper stay intact.
              return (
                <code className={codeClassName} {...rest}>
                  {children}
                </code>
              );
            }
            return (
              <code
                className="rounded-md border border-charcoal-ink/10 bg-charcoal-ink/[0.06] px-1.5 py-0.5 font-mono text-[0.85em] text-hust-red"
                {...rest}
              >
                {children}
              </code>
            );
          },
          pre(props) {
            const codeEl = props.children as
              | ReactElement<{ className?: string; children?: ReactNode }>
              | undefined;
            const codeClassName = codeEl?.props?.className || "";

            if (/language-mermaid/.test(codeClassName)) {
              return <MermaidDiagram chart={nodeToText(codeEl?.props?.children)} />;
            }

            const language = /language-(\w+)/.exec(codeClassName)?.[1] ?? "";
            return <CodeBlock language={language}>{props.children}</CodeBlock>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
