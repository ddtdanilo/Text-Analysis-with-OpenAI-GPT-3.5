# Migrating from Version 1 to Version 2

Version 2 is a deliberate breaking release. It replaces retired model presets
and Chat Completions with the current package, CLI, and Responses API design.

## Installation

Version 1:

```bash
pip install -r requirements.txt
python scripts/text_analysis.py prompt.txt response.txt document.txt
```

Version 2:

```bash
pip install -e .
openai-document-analyzer document.txt --prompt-file prompt.txt
```

The original three-file interactive command remains as a temporary
compatibility wrapper.

## Imports

Version 1:

```python
from scripts.document_analyzer import DocumentAnalyzer
```

Version 2:

```python
from openai_document_analyzer import DocumentAnalyzer
```

The old import currently re-exports the new class but may be removed in a future
major release.

## Synchronous methods

Version 1:

```python
result = await analyzer.analyze_document("report.pdf")
```

Version 2:

```python
result = analyzer.analyze_document("report.pdf")
```

The former method was declared async while using a synchronous OpenAI client.
Version 2 makes that behavior explicit.

## Errors

Version 1 sometimes returned a string beginning with `Error`. That value could
be mistaken for a valid model answer.

Version 2 raises typed exceptions:

```python
from openai_document_analyzer import AnalysisError, DocumentReadError

try:
    result = analyzer.analyze_document("report.pdf")
except DocumentReadError:
    ...
except AnalysisError:
    ...
```

## Models

| Version 1 preset | Version 2 starting point |
| --- | --- |
| `gpt-4o` | `gpt-5.6-sol` |
| `gpt-4o-mini` | Evaluate `gpt-5.6-luna` |
| `gpt-4-turbo` | Evaluate `gpt-5.6-terra` or Sol |
| GPT‑3.5 presets | Evaluate `gpt-5.6-luna` |

These mappings describe a starting point, not guaranteed equivalence. Run
representative evaluations for output quality, latency, and cost.

## API parameters

Version 2:

- uses `client.responses.create`;
- uses `max_output_tokens` rather than `max_tokens`;
- sets reasoning effort and text verbosity explicitly;
- does not set `temperature`;
- disables response storage by default;
- reads output from `response.output_text`.

## Document behavior

- TXT content is normalized by trimming outer whitespace.
- Markdown files are supported.
- PDF page boundaries are preserved with blank lines.
- Empty and image-only PDFs raise `EmptyDocumentError`.
- Oversized input raises `DocumentTooLargeError`; it is never silently
  truncated.

## Examples

The example prompt/response flow remains available:

```python
result = analyzer.ask_questions(
    prompt="List the key risks.",
    example_prompt="List the key decisions.",
    example_response="- Decision one",
    text_to_analyze=document_text,
)
```

Use examples only when they define a necessary output shape. Lean, direct
prompts are preferable for ordinary analysis.
