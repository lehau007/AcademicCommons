import os
# botocore reads AWS_PROFILE and AWS_DEFAULT_PROFILE straight from the process env
# and treats "" as a literal (invalid) profile name. Scrub blank values defensively
# at startup so a misconfigured container env can't crash session/client creation.
for env_key in ("AWS_PROFILE", "AWS_DEFAULT_PROFILE"):
    if os.environ.get(env_key) == "":
        os.environ.pop(env_key, None)

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Academic Knowledge Backend"
    environment: str = "local"
    api_v1_prefix: str = "/api/v1"

    # Error file logging. On by default so failures land in a file (no need to
    # exec into the container to read them). Set ERROR_LOG_FILE_ENABLED=false in
    # production to avoid filling the server disk. The handler is ERROR-level and
    # rotates, so even when left on it stays bounded.
    error_log_file_enabled: bool = True
    error_log_file_path: str = "logs/backend-errors.log"
    error_log_file_max_bytes: int = 5_000_000
    error_log_file_backup_count: int = 3

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "academic_kb"
    postgres_user: str = "postgres"
    postgres_password: str = "changeme"
    database_url: str | None = None

    redis_url: str = "redis://localhost:6379/0"

    # Email verification (Resend). `console` backend logs the verification
    # link/OTP to stdout so local dev and tests can read them from docker logs
    # without an external mail provider. Switch to `resend` once RESEND_API_KEY
    # is set.
    email_backend: str = "console"
    resend_api_key: str | None = None
    resend_from: str = "Academic Commons <onboarding@resend.dev>"
    app_base_url: str = "http://localhost:3000"
    email_verification_ttl_minutes: int = 60
    email_verification_resend_cooldown_seconds: int = 60

    storage_endpoint: str = "http://localhost:9000"
    storage_access_key: str = "minioadmin"
    storage_secret_key: str = "minioadmin"
    storage_bucket: str = "documents"
    storage_public_host: str = "http://localhost:9000"

    jwt_secret: str = Field(default="changeme_in_prod_minimum_32_bytes", min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_ttl_hours: int = 24
    jwt_refresh_ttl_days: int = 7

    # Comma-separated list of browser origins allowed by CORS.
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Per-IP sliding-window rate limits.
    #   backend="memory" — in-process, correct only for a single instance.
    #   backend="redis"  — shared state across instances behind a load balancer.
    rate_limit_enabled: bool = True
    rate_limit_backend: str = "memory"
    rate_limit_per_minute: int = 120
    rate_limit_login_per_minute: int = 10

    azure_ai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_deployment: str | None = None
    azure_openai_api_version: str = "2024-08-01-preview"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.1-flash-lite"
    groq_api_key: str | None = None
    groq_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"

    # OpenCode (opencode.ai) Go-plan gateway, OpenAI-compatible
    opencode_api_key: str | None = None
    opencode_model: str = "minimax-m3"
    opencode_base_url: str = "https://opencode.ai/zen/go/v1"

    # OpenRouter (openrouter.ai) gateway, OpenAI-compatible
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-5.4-mini"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_embedding_model: str = "openai/text-embedding-3-small"
    openrouter_rerank_model: str = "cohere/rerank-v3.5"

    # AWS Bedrock (Amazon Nova)
    bedrock_api_key: str | None = None
    bedrock_base_url: str | None = None
    aws_region: str = "us-east-1"
    aws_profile: str | None = None
    bedrock_model_id: str | None = None

    # Provider failover order; missing-credential providers are skipped
    llm_provider_order: str = "bedrock,gemini,groq"
    llm_optimizer_enabled: bool = False
    llm_optimizer_enabled_flows: str = ""
    llm_optimizer_prompt_version: str = "v1"
    llm_optimizer_model_version: str = "default"
    llm_optimizer_prefix_cache_enabled: bool = False
    llm_optimizer_semantic_cache_enabled: bool = False
    llm_optimizer_cascade_routing_enabled: bool = False
    llm_optimizer_shadow_enabled: bool = False
    llm_optimizer_provider_fallback_enabled: bool = False
    llm_optimizer_budget_cap_usd: float | None = None
    llm_optimizer_on_budget_exceeded: str = "warn"
    # Cost reporting: JSONL log of every optimizer invocation (cost/usage/cache).
    # Empty path keeps the SDK default file; set False to disable logging entirely.
    llm_optimizer_logging_enabled: bool = True
    llm_optimizer_log_path: str = "data/pipeline_outputs/optimizer_logs/optimizer.jsonl"
    # Price overrides for models missing from the SDK's DEFAULT_PRICE_TABLE, as JSON:
    # {"provider:model_id": [input_per_mtok_usd, output_per_mtok_usd]}. Merged over defaults.
    llm_optimizer_price_table_json: str = ""
    llm_optimizer_profile_default: str = "default"
    llm_optimizer_profile_eval_pipeline: str | None = None
    llm_optimizer_profile_tutor: str | None = None
    llm_optimizer_profile_mindmap: str | None = None
    llm_optimizer_profile_mock_test: str | None = None
    llm_optimizer_profile_course: str | None = None
    llm_optimizer_profile_topic_tags: str | None = None
    llm_optimizer_profile_summarization: str | None = None

    nvidia_api_key: str | None = None
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    embedding_model: str = "nvidia/nv-embedqa-e5-v5"
    embedding_dim: int = 1536
    rerank_model: str = "nvidia/llama-nemotron-rerank-vl-1b-v2"
    rerank_enabled: bool = True
    # Reranking lives on a different host/path than embeddings:
    #   {base}/{rerank_model}/reranking  (e.g. https://ai.api.nvidia.com/v1/retrieval/<model>/reranking)
    nvidia_rerank_base: str = "https://ai.api.nvidia.com/v1/retrieval"

    tavily_api_key: str | None = None
    agent2_enabled: bool = True
    agent2_timeout_seconds: int = 15

    tutor_mmr_k: int = 6
    tutor_mmr_lambda: float = 0.7
    tutor_tier_boost: float = 1.15
    # Hybrid retrieval: fuse dense (pgvector) with a BM25-style lexical branch via
    # Reciprocal Rank Fusion before reranking. Falls back to dense-only when the lexical
    # branch returns nothing, so turning this off restores the pure-dense behavior.
    tutor_hybrid_enabled: bool = True
    # Minimum cosine similarity a candidate must clear to be retrieved. 0.0 = disabled
    # (current behavior). Raise it (e.g. ~0.35–0.45 for the NVIDIA/OpenRouter embedders)
    # to drop weak matches so the tutor says "not covered" instead of citing noise.
    tutor_sim_threshold: float = 0.0
    # Minimum cross-encoder rerank relevance (cohere/rerank-v3.5, ~0.0–1.0) a chunk must
    # clear AFTER reranking → dynamic k. 0.0 = disabled. This is the discriminative floor
    # (cosine cannot separate adjacent subtopics; the reranker score can). Tune from the
    # observed rerank_score distribution; ~0.2–0.4 is a reasonable starting range.
    tutor_rerank_threshold: float = 0.0

    worker_ocr_concurrency: int = 1
    worker_eval_concurrency: int = 4
    worker_index_concurrency: int = 4
    worker_ocr_job_timeout_seconds: int = 1800

    # Hard cap on a single upload's byte size. Enforced in the documents API
    # before `file.read()` to avoid loading oversized files into memory.
    max_upload_bytes: int = 30 * 1024 * 1024  # 30 MB (students / community)
    # Higher cap for privileged roles (admin/reviewer) uploading official
    # lecture material, which is often image-heavy and exceeds 30 MB.
    max_upload_bytes_privileged: int = 50 * 1024 * 1024  # 50 MB

    # Document processing (OCR/parsing) pipeline
    ocr_enable_real_vision: bool = False
    # Concurrent VLM calls per document during extraction (classify + content calls for
    # embedded images/pages). Vision calls are otherwise fully sequential, which dominates
    # OCR runtime on image-heavy PPTX/scanned PDFs.
    ocr_vision_max_workers: int = 6
    azure_openai_input_cost_per_1m: float = 0.15
    azure_openai_output_cost_per_1m: float = 0.60
    document_processing_normalize_char_budget: int = 24000
    # Concurrency for the per-batch normalization LLM calls. Kept below
    # ocr_vision_max_workers: too many parallel calls throttle the primary
    # provider (bedrock) and cascade batches onto slower fallbacks.
    document_processing_normalize_max_workers: int = 4

    @field_validator(
        "azure_ai_api_key",
        "azure_openai_endpoint",
        "azure_openai_deployment",
        "gemini_api_key",
        "groq_api_key",
        "opencode_api_key",
        "openrouter_api_key",
        "bedrock_api_key",
        "bedrock_base_url",
        "aws_profile",
        "bedrock_model_id",
        "nvidia_api_key",
        "resend_api_key",
        mode="before",
    )
    @classmethod
    def _blank_string_to_none(cls, value: str | None) -> str | None:
        # Some .env lines carry an inline `# comment` that the dotenv/compose parser
        # does not strip (e.g. `BEDROCK_BASE_URL=   # optional ...`); treat a blank or
        # comment-only value as unset so it falls back to the field default.
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped or stripped.startswith("#"):
                return None
        return value

    @field_validator("llm_optimizer_budget_cap_usd", mode="before")
    @classmethod
    def _blank_budget_to_none(cls, value: float | str | None) -> float | str | None:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def llm_provider_order_list(self) -> list[str]:
        return [name.strip().lower() for name in self.llm_provider_order.split(",") if name.strip()]

    @property
    def llm_optimizer_enabled_flow_list(self) -> list[str]:
        return [
            name.strip().lower().replace("-", "_")
            for name in self.llm_optimizer_enabled_flows.split(",")
            if name.strip()
        ]

    def llm_optimizer_enabled_for_flow(self, flow_name: str | None = None) -> bool:
        if not self.llm_optimizer_enabled:
            return False
        enabled_flows = self.llm_optimizer_enabled_flow_list
        if not enabled_flows:
            return True
        normalized = (flow_name or "default").strip().lower().replace("-", "_")
        return normalized in enabled_flows

    def llm_optimizer_profile_for_flow(self, flow_name: str | None = None) -> str:
        if not flow_name:
            return self.llm_optimizer_profile_default

        normalized = flow_name.strip().lower().replace("-", "_")
        profile = getattr(self, f"llm_optimizer_profile_{normalized}", None)
        return profile or self.llm_optimizer_profile_default

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
