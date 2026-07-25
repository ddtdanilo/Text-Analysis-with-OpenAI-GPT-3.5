"""Compatibility imports for applications written against version 1.x.

New code should import from :mod:`openai_document_analyzer`.
"""

from openai_document_analyzer import (
    DEFAULT_MODEL,
    MODEL_PROFILES,
    DocumentAnalyzer,
)

AVAILABLE_MODELS = [model for model, _description in MODEL_PROFILES]

__all__ = ["AVAILABLE_MODELS", "DEFAULT_MODEL", "DocumentAnalyzer"]
