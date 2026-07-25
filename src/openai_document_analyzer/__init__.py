"""Public package interface for OpenAI Document Analyzer."""

from openai_document_analyzer.analyzer import (
    DEFAULT_MODEL,
    MODEL_PROFILES,
    DocumentAnalyzer,
)
from openai_document_analyzer.exceptions import (
    AnalysisError,
    ConfigurationError,
    DocumentAnalyzerError,
    DocumentReadError,
    DocumentTooLargeError,
    EmptyDocumentError,
    EmptyResponseError,
)

__version__ = "2.0.0"

__all__ = [
    "DEFAULT_MODEL",
    "MODEL_PROFILES",
    "AnalysisError",
    "ConfigurationError",
    "DocumentAnalyzer",
    "DocumentAnalyzerError",
    "DocumentReadError",
    "DocumentTooLargeError",
    "EmptyDocumentError",
    "EmptyResponseError",
    "__version__",
]
