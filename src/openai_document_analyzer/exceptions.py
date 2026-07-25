"""Domain-specific exceptions raised by OpenAI Document Analyzer."""


class DocumentAnalyzerError(Exception):
    """Base exception for expected application failures."""


class ConfigurationError(DocumentAnalyzerError):
    """Raised when required application configuration is missing or invalid."""


class DocumentReadError(DocumentAnalyzerError):
    """Raised when a document exists but cannot be read."""


class DocumentTooLargeError(DocumentAnalyzerError):
    """Raised when a document exceeds a configured safety limit."""


class EmptyDocumentError(DocumentAnalyzerError):
    """Raised when a document contains no extractable text."""


class AnalysisError(DocumentAnalyzerError):
    """Raised when the OpenAI API cannot complete an analysis."""


class EmptyResponseError(AnalysisError):
    """Raised when the API response contains no output text."""
