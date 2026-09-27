"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

const ASSET_RE =
  /^asset:\/\/([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\/(p\d{3,4}-(?:f\d{1,3}|page)\.(?:png|jpe?g))$/;
// Fallback when the API omits expires_in_seconds (signed URLs live 15 minutes).
const DEFAULT_EXPIRES_IN_SECONDS = 900;
// The batch endpoint accepts at most this many names per request.
const MAX_NAMES_PER_REQUEST = 200;

type AssetUrlsResponse = { urls: Record<string, string>; expires_in_seconds?: number };
type Signed = { url: string; maxAgeMs: number };
type Waiter = { resolve: (signed: Signed) => void; reject: (error: unknown) => void };
type CacheEntry = { promise: Promise<string>; meta: { expiresAt: number; url?: string } };

const urlCache = new Map<string, CacheEntry>();
// Names requested in the current tick, per document; flushed as one batch request.
const pendingBatches = new Map<string, Map<string, Waiter[]>>();

export function parseAssetSrc(src: string): { documentId: string; name: string } | null {
  const match = ASSET_RE.exec(src);
  return match ? { documentId: match[1], name: match[2] } : null;
}

function flushBatch(documentId: string) {
  const batch = pendingBatches.get(documentId);
  pendingBatches.delete(documentId);
  if (!batch) return;
  const names = [...batch.keys()];
  for (let start = 0; start < names.length; start += MAX_NAMES_PER_REQUEST) {
    const chunk = names.slice(start, start + MAX_NAMES_PER_REQUEST);
    api
      .get<AssetUrlsResponse>(`/documents/${documentId}/assets/urls`, { params: { names: chunk.join(",") } })
      .then(
        (res) => {
          // Refresh at 2/3 of the signed URL's lifetime.
          const maxAgeMs = ((res.expires_in_seconds || DEFAULT_EXPIRES_IN_SECONDS) * 1000 * 2) / 3;
          for (const name of chunk) {
            const url = res.urls?.[name];
            for (const waiter of batch.get(name) ?? []) {
              if (url) waiter.resolve({ url, maxAgeMs });
              else waiter.reject(new Error(`No signed URL returned for ${name}`));
            }
          }
        },
        (error: unknown) => {
          for (const name of chunk) for (const waiter of batch.get(name) ?? []) waiter.reject(error);
        },
      );
  }
}

function requestSignedUrl(documentId: string, name: string): Promise<Signed> {
  return new Promise<Signed>((resolve, reject) => {
    let batch = pendingBatches.get(documentId);
    if (!batch) {
      batch = new Map();
      pendingBatches.set(documentId, batch);
      setTimeout(() => flushBatch(documentId), 0);
    }
    const waiters = batch.get(name) ?? [];
    waiters.push({ resolve, reject });
    batch.set(name, waiters);
  });
}

function resolveAssetUrl(documentId: string, name: string): Promise<string> {
  const key = `${documentId}/${name}`;
  const cached = urlCache.get(key);
  if (cached && Date.now() < cached.meta.expiresAt) return cached.promise;
  const requestedAt = Date.now();
  // Pending entries never expire; the max-age starts from the request time once the URL arrives.
  const meta: CacheEntry["meta"] = { expiresAt: Number.POSITIVE_INFINITY };
  const promise = requestSignedUrl(documentId, name).then(
    ({ url, maxAgeMs }) => {
      meta.url = url;
      meta.expiresAt = requestedAt + maxAgeMs;
      return url;
    },
    (error: unknown) => {
      if (urlCache.get(key)?.meta === meta) urlCache.delete(key);
      throw error;
    },
  );
  urlCache.set(key, { promise, meta });
  return promise;
}

/** Drop a cached URL that failed to load (e.g. expired), unless it was already replaced. */
function invalidateAssetUrl(documentId: string, name: string, failedUrl: string) {
  const key = `${documentId}/${name}`;
  if (urlCache.get(key)?.meta.url === failedUrl) urlCache.delete(key);
}

type Status = { kind: "loading" } | { kind: "ready"; url: string } | { kind: "error" };
type State = { src: string; status: Status; retried: boolean };

export default function AssetImage({ src, alt }: { src: string; alt: string }) {
  const parsed = parseAssetSrc(src);
  const [state, setState] = useState<State>({ src, status: { kind: "loading" }, retried: false });

  useEffect(() => {
    if (!parsed) return;
    let cancelled = false;
    resolveAssetUrl(parsed.documentId, parsed.name).then(
      (url) => {
        if (!cancelled) setState({ src, status: { kind: "ready", url }, retried: false });
      },
      () => {
        if (!cancelled) setState({ src, status: { kind: "error" }, retried: false });
      },
    );
    return () => {
      cancelled = true;
    };
    // parsed is derived from src
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src]);

  const status: Status = !parsed
    ? { kind: "error" }
    : state.src === src
      ? state.status
      : { kind: "loading" };

  // A lazy image may first load long after its URL was signed: on failure, fetch a fresh URL once.
  const handleImageError = () => {
    if (!parsed || status.kind !== "ready") return;
    if (state.retried) {
      setState({ src, status: { kind: "error" }, retried: true });
      return;
    }
    invalidateAssetUrl(parsed.documentId, parsed.name, status.url);
    setState({ src, status: { kind: "loading" }, retried: true });
    const settle = (next: Status) =>
      setState((prev) => (prev.src === src ? { src, status: next, retried: true } : prev));
    resolveAssetUrl(parsed.documentId, parsed.name).then(
      (url) => settle({ kind: "ready", url }),
      () => settle({ kind: "error" }),
    );
  };

  if (status.kind === "ready") {
    return (
      <a href={status.url} target="_blank" rel="noopener noreferrer" className="not-prose my-3 block">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={status.url}
          alt={alt}
          loading="lazy"
          onError={handleImageError}
          className="mx-auto max-h-[480px] w-auto max-w-full rounded-lg border border-charcoal-ink/10 bg-white object-contain"
        />
      </a>
    );
  }
  if (status.kind === "error") {
    return (
      <span className="not-prose my-3 inline-block rounded-lg border border-dashed border-charcoal-ink/20 px-3 py-2 text-sm text-charcoal-ink/60">
        🖼 {alt || "Hình ảnh không khả dụng"}
      </span>
    );
  }
  return (
    <span
      role="img"
      aria-label={alt}
      className="not-prose my-3 block h-40 w-full animate-pulse rounded-lg bg-charcoal-ink/[0.06]"
    />
  );
}
