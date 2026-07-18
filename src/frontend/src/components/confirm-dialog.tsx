"use client";

import React, { useEffect } from "react";
import { AlertTriangle } from "lucide-react";

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  message: React.ReactNode;
  confirmLabel?: string;
  cancelLabel?: string;
  variant?: "danger" | "default";
  busy?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

/**
 * Styled confirmation modal, consistent with the app's design system and Toast
 * notifications. Replaces the browser-native `confirm()` for destructive or
 * important actions (e.g. deactivating a user account).
 */
export default function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = "Xác nhận",
  cancelLabel = "Hủy",
  variant = "default",
  busy = false,
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !busy) onCancel();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, busy, onCancel]);

  if (!open) return null;

  const confirmClass =
    variant === "danger"
      ? "bg-system-red text-white hover:bg-red-700"
      : "bg-hust-red text-white hover:bg-red-800";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-charcoal-ink/40 p-4 animate-in fade-in duration-150"
      onClick={() => !busy && onCancel()}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="w-full max-w-md bg-white rounded-2xl border border-whisper-border shadow-xl p-6 space-y-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start gap-3">
          <div
            className={`shrink-0 w-9 h-9 rounded-full flex items-center justify-center ${
              variant === "danger" ? "bg-red-50 text-system-red" : "bg-[#FFF8F6] text-hust-red"
            }`}
          >
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <h3 className="font-display font-extrabold text-[16px] text-charcoal-ink">{title}</h3>
            <div className="text-body-sm text-muted-steel leading-relaxed">{message}</div>
          </div>
        </div>
        <div className="flex justify-end gap-2.5 pt-1">
          <button
            className="px-4 py-2 rounded-xl border border-whisper-border text-body-sm font-semibold text-charcoal-ink hover:bg-canvas-base disabled:opacity-50"
            onClick={onCancel}
            disabled={busy}
          >
            {cancelLabel}
          </button>
          <button
            className={`px-4 py-2 rounded-xl text-body-sm font-bold disabled:opacity-60 ${confirmClass}`}
            onClick={onConfirm}
            disabled={busy}
          >
            {busy ? "Đang xử lý..." : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
