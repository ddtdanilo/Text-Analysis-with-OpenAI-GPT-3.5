"""Shared pytest fixtures."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from openai_document_analyzer import DocumentAnalyzer


@pytest.fixture
def mock_client() -> SimpleNamespace:
    """Return a minimal mock of the OpenAI client."""
    return SimpleNamespace(responses=SimpleNamespace(create=Mock()))


@pytest.fixture
def analyzer(mock_client: SimpleNamespace) -> DocumentAnalyzer:
    """Return an analyzer that cannot make network requests."""
    return DocumentAnalyzer(client=mock_client)
