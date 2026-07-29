from __future__ import annotations

import logging
from typing import Any

import google.auth
from app.config import settings

logger = logging.getLogger(__name__)


def get_vertex_credentials_and_project() -> tuple[Any | None, str | None]:
    """Retrieve Google Cloud credentials and project ID using gcloud CLI / ADC."""
    project_id = settings.vertex_project_id
    credentials = None
    try:
        credentials, default_project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        if not project_id:
            project_id = default_project
    except Exception as exc:
        logger.warning(f"Could not load Google Cloud ADC credentials: {exc}")
    return credentials, project_id
