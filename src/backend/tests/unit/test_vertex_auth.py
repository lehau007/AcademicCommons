from unittest.mock import MagicMock, patch
import pytest

from app.config import settings
from app.llm.vertex_auth import get_vertex_credentials_and_project


def test_get_vertex_credentials_default_project(monkeypatch):
    """Test get_vertex_credentials_and_project returns credentials and default project ID when settings.vertex_project_id is None."""
    monkeypatch.setattr(settings, "vertex_project_id", None)
    mock_creds = MagicMock()
    with patch("google.auth.default", return_value=(mock_creds, "default-gcp-project")) as mock_default:
        creds, project_id = get_vertex_credentials_and_project()
        mock_default.assert_called_once_with(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        assert creds == mock_creds
        assert project_id == "default-gcp-project"


def test_get_vertex_credentials_custom_project_override(monkeypatch):
    """Test settings.vertex_project_id overrides default project ID when specified."""
    monkeypatch.setattr(settings, "vertex_project_id", "my-custom-project")
    mock_creds = MagicMock()
    with patch("google.auth.default", return_value=(mock_creds, "default-gcp-project")):
        creds, project_id = get_vertex_credentials_and_project()
        assert creds == mock_creds
        assert project_id == "my-custom-project"


def test_get_vertex_credentials_exception_handling(monkeypatch):
    """Test exception during google.auth.default returns (None, project_id)."""
    monkeypatch.setattr(settings, "vertex_project_id", None)
    with patch("google.auth.default", side_effect=Exception("No ADC found")):
        creds, project_id = get_vertex_credentials_and_project()
        assert creds is None
        assert project_id is None
