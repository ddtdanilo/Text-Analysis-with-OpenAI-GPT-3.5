# Python API

## Import

```python
from openai_document_analyzer import DocumentAnalyzer
```

## `DocumentAnalyzer`

### `load_text(filepath) -> str`

Loads UTF-8 TXT or Markdown content, or extracts text from a PDF. Leading and
trailing whitespace is removed.

Raises:

- `FileNotFoundError`
- `DocumentReadError`
- `DocumentTooLargeError`
- `EmptyDocumentError`

### `extract_text_from_pdf(filepath) -> str`

Extracts nonempty PDF pages locally and separates them with a blank line.
Image-only PDFs return `EmptyDocumentError`; run OCR before calling the package.

### `analyze_text(text, prompt=..., model=None) -> str`

Sends text and an analysis request through the Responses API. The `model`
argument overrides the configured default for one call.

Raises:

- `ConfigurationError` for an empty prompt;
- `DocumentTooLargeError` or `EmptyDocumentError` for invalid text;
- `AnalysisError` when the OpenAI SDK raises an API error;
- `EmptyResponseError` when the API provides no output text.

### `analyze_document(filepath, prompt=..., model=None) -> str`

Combines `load_text()` and `analyze_text()`.

### `ask_questions(prompt, example_prompt, example_response, text_to_analyze, model=None) -> str`

Uses one example request and response as answer-shape guidance. Examples are not
treated as evidence about the document. Both example values are required.

This method exists for version 1 migration. Prefer a direct, explicit prompt
when an example is unnecessary.

## Constants

### `DEFAULT_MODEL`

The package default: `gpt-5.6-sol`.

### `MODEL_PROFILES`

Documented Sol, Terra, and Luna model IDs with their intended tradeoff. It is
not an allowlist.

## Exception hierarchy

```text
DocumentAnalyzerError
├── ConfigurationError
├── DocumentReadError
├── DocumentTooLargeError
├── EmptyDocumentError
└── AnalysisError
    └── EmptyResponseError
```

Catch the narrowest exception that the application can handle:

```python
from openai_document_analyzer import (
    AnalysisError,
    DocumentAnalyzer,
    DocumentReadError,
)

analyzer = DocumentAnalyzer()

try:
    result = analyzer.analyze_document("report.pdf")
except DocumentReadError as exc:
    print(f"Document problem: {exc}")
except AnalysisError as exc:
    print(f"API problem: {exc}")
```

Programming errors and unexpected failures are intentionally not converted to
plausible analysis text.

## Client injection

```python
from openai import OpenAI
from openai_document_analyzer import DocumentAnalyzer

client = OpenAI(timeout=45.0, max_retries=4)
analyzer = DocumentAnalyzer(client=client)
```

The injected object must provide `client.responses.create(...)` and return an
object with `output_text`.

## Sync behavior

Version 2 is synchronous. Applications requiring async execution should place
the synchronous call in an appropriate worker or implement a dedicated
`AsyncOpenAI` integration with equivalent request, privacy, and error behavior.
