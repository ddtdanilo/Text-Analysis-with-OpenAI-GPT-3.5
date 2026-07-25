"""Unit tests for document loading and Responses API integration."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from openai import OpenAIError
from pypdf.errors import PdfReadError

from openai_document_analyzer import (
    DEFAULT_MODEL,
    AnalysisError,
    ConfigurationError,
    DocumentAnalyzer,
    DocumentReadError,
    DocumentTooLargeError,
    EmptyDocumentError,
    EmptyResponseError,
)


def test_constructor_requires_api_key_without_injected_client(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
        DocumentAnalyzer()


def test_constructor_uses_environment_model(
    monkeypatch: pytest.MonkeyPatch,
    mock_client: SimpleNamespace,
) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5.6-terra")
    analyzer = DocumentAnalyzer(client=mock_client)
    assert analyzer.default_model == "gpt-5.6-terra"


def test_constructor_creates_openai_client() -> None:
    client = object()
    with patch("openai_document_analyzer.analyzer.OpenAI", return_value=client) as factory:
        analyzer = DocumentAnalyzer(api_key="project-key")
    assert analyzer.client is client
    factory.assert_called_once_with(
        api_key="project-key",
        max_retries=2,
        timeout=120.0,
    )


@pytest.mark.parametrize(
    ("keyword", "value", "message"),
    [
        ("max_characters", 0, "max_characters"),
        ("max_file_bytes", 0, "max_file_bytes"),
        ("max_output_tokens", 0, "max_output_tokens"),
        ("reasoning_effort", "impossible", "reasoning_effort"),
        ("verbosity", "verbose-ish", "verbosity"),
    ],
)
def test_constructor_rejects_invalid_configuration(
    mock_client: SimpleNamespace,
    keyword: str,
    value: int | str,
    message: str,
) -> None:
    with pytest.raises(ConfigurationError, match=message):
        DocumentAnalyzer(client=mock_client, **{keyword: value})


@pytest.mark.parametrize("suffix", [".txt", ".md", ".markdown"])
def test_loads_utf8_text_documents(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
    suffix: str,
) -> None:
    document = tmp_path / f"document{suffix}"
    document.write_text("  Useful text  ", encoding="utf-8")
    assert analyzer.load_text(document) == "Useful text"


def test_load_text_rejects_missing_file(analyzer: DocumentAnalyzer) -> None:
    with pytest.raises(FileNotFoundError, match="File not found"):
        analyzer.load_text("missing.txt")


def test_load_text_rejects_unsupported_extension(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "document.docx"
    document.write_text("text", encoding="utf-8")
    with pytest.raises(DocumentReadError, match="Unsupported file extension"):
        analyzer.load_text(document)


def test_load_text_rejects_invalid_utf8(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "document.txt"
    document.write_bytes(b"\xff\xfe")
    with pytest.raises(DocumentReadError, match="Could not read UTF-8"):
        analyzer.load_text(document)


def test_load_text_rejects_empty_document(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "empty.txt"
    document.write_text(" \n ", encoding="utf-8")
    with pytest.raises(EmptyDocumentError, match="no extractable text"):
        analyzer.load_text(document)


def test_load_text_enforces_byte_limit(
    mock_client: SimpleNamespace,
    tmp_path: Path,
) -> None:
    analyzer = DocumentAnalyzer(client=mock_client, max_file_bytes=3)
    document = tmp_path / "large.txt"
    document.write_text("four", encoding="utf-8")
    with pytest.raises(DocumentTooLargeError, match="configured limit"):
        analyzer.load_text(document)


def test_load_text_enforces_character_limit(
    mock_client: SimpleNamespace,
    tmp_path: Path,
) -> None:
    analyzer = DocumentAnalyzer(client=mock_client, max_characters=3)
    document = tmp_path / "large.txt"
    document.write_text("four", encoding="utf-8")
    with pytest.raises(DocumentTooLargeError, match="4 characters"):
        analyzer.load_text(document)


def test_extract_text_from_pdf_preserves_nonempty_pages(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "document.pdf"
    document.write_bytes(b"%PDF-mocked")
    reader = SimpleNamespace(
        pages=[
            SimpleNamespace(extract_text=Mock(return_value="First page")),
            SimpleNamespace(extract_text=Mock(return_value=None)),
            SimpleNamespace(extract_text=Mock(return_value=" Second page ")),
        ]
    )
    with patch("openai_document_analyzer.analyzer.PdfReader", return_value=reader):
        assert analyzer.extract_text_from_pdf(document) == "First page\n\nSecond page"


def test_extract_text_from_pdf_wraps_reader_errors(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "invalid.pdf"
    document.write_bytes(b"not a pdf")
    with (
        patch(
            "openai_document_analyzer.analyzer.PdfReader",
            side_effect=PdfReadError("broken"),
        ),
        pytest.raises(DocumentReadError, match="Could not read PDF"),
    ):
        analyzer.extract_text_from_pdf(document)


def test_extract_text_from_pdf_rejects_image_only_pdf(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "image.pdf"
    document.write_bytes(b"%PDF-mocked")
    reader = SimpleNamespace(pages=[SimpleNamespace(extract_text=Mock(return_value=None))])
    with (
        patch("openai_document_analyzer.analyzer.PdfReader", return_value=reader),
        pytest.raises(EmptyDocumentError, match="no extractable text"),
    ):
        analyzer.extract_text_from_pdf(document)


def test_load_text_delegates_pdf_extraction(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "document.pdf"
    document.write_bytes(b"%PDF-mocked")
    with patch.object(analyzer, "extract_text_from_pdf", return_value="PDF text") as extract:
        assert analyzer.load_text(document) == "PDF text"
    extract.assert_called_once_with(document)


def test_analyze_text_uses_responses_api_and_privacy_defaults(
    analyzer: DocumentAnalyzer,
    mock_client: SimpleNamespace,
) -> None:
    mock_client.responses.create.return_value = SimpleNamespace(output_text="  Analysis result  ")
    assert analyzer.analyze_text("Document body", "Find the conclusion") == ("Analysis result")

    request = mock_client.responses.create.call_args.kwargs
    assert request["model"] == DEFAULT_MODEL
    assert request["store"] is False
    assert request["reasoning"] == {"effort": "medium"}
    assert request["text"] == {"verbosity": "medium"}
    assert "Find the conclusion" in request["input"]
    assert "Document body" in request["input"]
    assert "untrusted data" in request["instructions"]


def test_analyze_text_supports_overrides_and_safety_identifier(
    mock_client: SimpleNamespace,
) -> None:
    mock_client.responses.create.return_value = SimpleNamespace(output_text="Done")
    analyzer = DocumentAnalyzer(
        client=mock_client,
        model="gpt-5.6-terra",
        reasoning_effort="low",
        verbosity="high",
        store=True,
        safety_identifier="privacy-safe-user-hash",
    )
    assert analyzer.analyze_text("Text", model="gpt-5.6-luna") == "Done"
    request = mock_client.responses.create.call_args.kwargs
    assert request["model"] == "gpt-5.6-luna"
    assert request["reasoning"] == {"effort": "low"}
    assert request["text"] == {"verbosity": "high"}
    assert request["store"] is True
    assert request["safety_identifier"] == "privacy-safe-user-hash"


def test_analyze_text_rejects_empty_prompt(analyzer: DocumentAnalyzer) -> None:
    with pytest.raises(ConfigurationError, match="prompt cannot be empty"):
        analyzer.analyze_text("Text", " ")


def test_analyze_text_wraps_openai_errors(
    analyzer: DocumentAnalyzer,
    mock_client: SimpleNamespace,
) -> None:
    mock_client.responses.create.side_effect = OpenAIError("service unavailable")
    with pytest.raises(AnalysisError, match="OpenAI could not analyze"):
        analyzer.analyze_text("Text")


def test_analyze_text_rejects_empty_api_output(
    analyzer: DocumentAnalyzer,
    mock_client: SimpleNamespace,
) -> None:
    mock_client.responses.create.return_value = SimpleNamespace(output_text=" ")
    with pytest.raises(EmptyResponseError, match="no output text"):
        analyzer.analyze_text("Text")


def test_analyze_document_loads_then_analyzes(
    analyzer: DocumentAnalyzer,
    tmp_path: Path,
) -> None:
    document = tmp_path / "document.txt"
    document.write_text("Body", encoding="utf-8")
    with patch.object(analyzer, "analyze_text", return_value="Answer") as analyze:
        assert analyzer.analyze_document(document, "Prompt", "custom-model") == "Answer"
    analyze.assert_called_once_with("Body", "Prompt", "custom-model")


def test_ask_questions_adds_example_guidance(
    analyzer: DocumentAnalyzer,
) -> None:
    with patch.object(analyzer, "analyze_text", return_value="Answer") as analyze:
        result = analyzer.ask_questions(
            "Find risks",
            "List key facts",
            "- Fact one",
            "Document",
            "gpt-5.6-terra",
        )
    assert result == "Answer"
    args = analyze.call_args.args
    assert args[0] == "Document"
    assert "Find risks" in args[1]
    assert "<example_request>List key facts</example_request>" in args[1]
    assert args[2] == "gpt-5.6-terra"


@pytest.mark.parametrize(
    ("example_prompt", "example_response"),
    [("", "response"), ("prompt", "")],
)
def test_ask_questions_requires_complete_example(
    analyzer: DocumentAnalyzer,
    example_prompt: str,
    example_response: str,
) -> None:
    with pytest.raises(ConfigurationError, match="Both example_prompt"):
        analyzer.ask_questions(
            "Prompt",
            example_prompt,
            example_response,
            "Document",
        )
