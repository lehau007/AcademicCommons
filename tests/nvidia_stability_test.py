"""
Stability test for NVIDIA NIM (build.nvidia.com) — embedding + reranking.

Goal: prove the hosted API is *usable and not constantly erroring* under a steady
load, NOT to benchmark throughput. Fires a fixed rate of requests for a fixed
duration, then reports success rate, latency percentiles, and an error histogram.

Default load: 40 requests/min for 2 min = 80 requests, run for embed then rerank.

Setup:
    export NVIDIA_API_KEY="nvapi-..."
    # optional overrides:
    export EMBED_MODEL="nvidia/llama-3.2-nv-embedqa-1b-v2"
    export RERANK_MODEL="nvidia/llama-3.2-nv-rerankqa-1b-v2"
    export RERANK_URL="https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-3_2-nv-rerankqa-1b-v2/reranking"
    export RATE_PER_MIN=40
    export DURATION_MIN=2
    export TARGET=both          # embed | rerank | both

Run:
    python tests/nvidia_stability_test.py
"""

import asyncio
import os
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from openai import AsyncOpenAI


def _load_local_env() -> None:
    """Load tests/.env (next to this script) into os.environ without extra deps.

    Existing environment variables win, so `export` / CLI overrides still apply.
    """
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_local_env()

API_KEY = os.environ.get("NVIDIA_API_KEY", "")
BASE_URL = os.environ.get("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

EMBED_MODEL = os.environ.get("EMBED_MODEL", "nvidia/llama-3.2-nv-embedqa-1b-v2")
RERANK_MODEL = os.environ.get("RERANK_MODEL", "nvidia/llama-nemotron-rerank-vl-1b-v2")
RERANK_URL = os.environ.get(
    "RERANK_URL",
    "https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-nemotron-rerank-vl-1b-v2/reranking",
)

RATE_PER_MIN = int(os.environ.get("RATE_PER_MIN", "40"))
DURATION_MIN = float(os.environ.get("DURATION_MIN", "2"))
TARGET = os.environ.get("TARGET", "both").lower()

TOTAL = int(round(RATE_PER_MIN * DURATION_MIN))
INTERVAL = 60.0 / RATE_PER_MIN  # seconds between request launches

SAMPLE_TEXT = "Phương pháp RAG kết hợp truy hồi tài liệu và sinh câu trả lời có trích dẫn nguồn."
SAMPLE_PASSAGES = [
    "RAG nối retrieval với một mô hình ngôn ngữ để trả lời kèm dẫn nguồn.",
    "Hệ thống quản lý tài liệu học thuật của cộng đồng sinh viên.",
    "Embedding chuyển văn bản thành vector để tìm kiếm theo ngữ nghĩa.",
]


@dataclass
class Result:
    ok: bool
    status: int
    latency_ms: float
    err: str = ""


@dataclass
class Report:
    name: str
    results: list[Result] = field(default_factory=list)

    def render(self) -> str:
        n = len(self.results)
        oks = [r for r in self.results if r.ok]
        fails = [r for r in self.results if not r.ok]
        lat = sorted(r.latency_ms for r in oks)

        def pct(p: float) -> float:
            if not lat:
                return 0.0
            i = min(len(lat) - 1, int(round(p / 100 * (len(lat) - 1))))
            return lat[i]

        lines = [
            f"\n===== {self.name} =====",
            f"requests   : {n}",
            f"success    : {len(oks)} ({100 * len(oks) / max(n, 1):.1f}%)",
            f"failed     : {len(fails)}",
        ]
        if lat:
            lines += [
                f"latency ms : min={lat[0]:.0f}  p50={pct(50):.0f}  p95={pct(95):.0f}  "
                f"max={lat[-1]:.0f}  mean={statistics.mean(lat):.0f}",
            ]
        if fails:
            hist: dict[str, int] = {}
            for r in fails:
                key = r.err.splitlines()[0][:80] if r.err else f"HTTP {r.status}"
                hist[key] = hist.get(key, 0) + 1
            lines.append("errors     :")
            for key, cnt in sorted(hist.items(), key=lambda kv: -kv[1]):
                lines.append(f"   {cnt:>3}x  {key}")
        return "\n".join(lines)


async def embed_once(client: AsyncOpenAI) -> Result:
    t0 = time.perf_counter()
    try:
        r = await client.embeddings.create(
            model=EMBED_MODEL,
            input=SAMPLE_TEXT,
            extra_body={"input_type": "query", "truncate": "END"},
        )
        ms = (time.perf_counter() - t0) * 1000
        dim = len(r.data[0].embedding)
        return Result(ok=True, status=200, latency_ms=ms, err=f"dim={dim}")
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        status = getattr(e, "status_code", 0) or 0
        return Result(ok=False, status=status, latency_ms=ms, err=f"{type(e).__name__}: {e}")


async def rerank_once(http: httpx.AsyncClient) -> Result:
    payload = {
        "model": RERANK_MODEL,
        "query": {"text": SAMPLE_TEXT},
        "passages": [{"text": p} for p in SAMPLE_PASSAGES],
        "truncate": "END",
    }
    t0 = time.perf_counter()
    try:
        resp = await http.post(RERANK_URL, json=payload)
        ms = (time.perf_counter() - t0) * 1000
        if resp.status_code == 200:
            return Result(ok=True, status=200, latency_ms=ms)
        return Result(ok=False, status=resp.status_code, latency_ms=ms, err=f"HTTP {resp.status_code}: {resp.text[:120]}")
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        return Result(ok=False, status=0, latency_ms=ms, err=f"{type(e).__name__}: {e}")


async def run_load(name: str, fire) -> Report:
    report = Report(name=name)
    print(f"\n>>> {name}: {TOTAL} requests @ {RATE_PER_MIN}/min (every {INTERVAL:.2f}s) for {DURATION_MIN} min")
    tasks: list[asyncio.Task[Result]] = []
    start = time.perf_counter()
    for i in range(TOTAL):
        target = start + i * INTERVAL
        now = time.perf_counter()
        if target > now:
            await asyncio.sleep(target - now)
        tasks.append(asyncio.create_task(fire()))
        # live heartbeat so a hang is visible
        print(f"  [{i + 1:>3}/{TOTAL}] launched at +{time.perf_counter() - start:5.1f}s", end="\r", flush=True)
    report.results = await asyncio.gather(*tasks)
    print(f"\n  done in {time.perf_counter() - start:.1f}s")
    return report


async def main() -> None:
    if not API_KEY:
        raise SystemExit("NVIDIA_API_KEY not set (export NVIDIA_API_KEY=nvapi-...)")

    print(f"Base URL    : {BASE_URL}")
    print(f"Embed model : {EMBED_MODEL}")
    print(f"Rerank model: {RERANK_MODEL}")
    print(f"Rerank URL  : {RERANK_URL}")
    print(f"Load        : {RATE_PER_MIN}/min x {DURATION_MIN}min = {TOTAL} req/target  (target={TARGET})")

    reports: list[Report] = []

    if TARGET in ("embed", "both"):
        client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=40.0)
        reports.append(await run_load(f"EMBED · {EMBED_MODEL}", lambda: embed_once(client)))

    if TARGET in ("rerank", "both"):
        headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
        async with httpx.AsyncClient(headers=headers, timeout=40.0) as http:
            reports.append(await run_load(f"RERANK · {RERANK_MODEL}", lambda: rerank_once(http)))

    print("\n" + "=" * 60)
    for rep in reports:
        print(rep.render())

    # final verdict
    print("\n" + "=" * 60)
    for rep in reports:
        ok = sum(1 for r in rep.results if r.ok)
        rate = 100 * ok / max(len(rep.results), 1)
        verdict = "USABLE" if rate >= 95 else ("FLAKY" if rate >= 70 else "UNRELIABLE")
        print(f"{rep.name:<45} {rate:5.1f}% success -> {verdict}")


if __name__ == "__main__":
    asyncio.run(main())
