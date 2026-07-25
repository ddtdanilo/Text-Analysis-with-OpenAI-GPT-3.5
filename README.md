# OpenAI Document Analyzer

[![CI](https://github.com/ddtdanilo/OpenAI-Document-Analyzer/actions/workflows/quality.yml/badge.svg)](https://github.com/ddtdanilo/OpenAI-Document-Analyzer/actions/workflows/quality.yml)
[![CodeQL](https://github.com/ddtdanilo/OpenAI-Document-Analyzer/actions/workflows/codeql.yml/badge.svg)](https://github.com/ddtdanilo/OpenAI-Document-Analyzer/actions/workflows/codeql.yml)
[![Latest release](https://img.shields.io/github/v/release/ddtdanilo/OpenAI-Document-Analyzer?color=2F80ED)](https://github.com/ddtdanilo/OpenAI-Document-Analyzer/releases/latest)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-27AE60.svg)](LICENSE)

A privacy-conscious Python CLI and library for asking focused questions about
TXT, Markdown, and PDF documents with the
[OpenAI Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses).

Version 2 uses the GPT‑5.6 model family, typed application errors, configurable
document limits, local PDF text extraction, and network-free unit tests with
more than 99% branch coverage.

## Why this project

- Analyze local `.txt`, `.md`, `.markdown`, and text-based `.pdf` files.
- Use `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, or another compatible
  model ID.
- Keep response storage disabled by default.
- Protect prompts from instructions embedded inside document content.
- Control reasoning effort, answer verbosity, output tokens, and input size.
- Use either a friendly CLI or the reusable `DocumentAnalyzer` Python class.
- Retain a compatibility command for the original three-file interactive flow.

> [!IMPORTANT]
> Document text is extracted locally, then the extracted text is sent to the
> OpenAI API for analysis. Do not submit material you are not authorized to
> process. Review [`PRIVACY.md`](PRIVACY.md) before using confidential,
> regulated, personal, or proprietary documents.

## Requirements

- Python 3.11 or newer
- An OpenAI API project key
- API access to the selected model
- Text-based PDFs; scanned/image-only PDFs require OCR before analysis

API usage may incur charges. Review the current
[model catalog](https://developers.openai.com/api/docs/models) and your project
usage limits before processing large documents.

## Installation

```bash
git clone https://github.com/ddtdanilo/OpenAI-Document-Analyzer.git
cd OpenAI-Document-Analyzer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Copy the environment template and add a project API key:

```bash
cp env.example .env
```

```dotenv
OPENAI_API_KEY=your_project_api_key
OPENAI_MODEL=gpt-5.6-sol
```

Never commit `.env` or an API key.

## Quick start

Analyze a document with the default prompt:

```bash
openai-document-analyzer report.pdf
```

Ask a focused question:

```bash
openai-document-analyzer report.pdf \
  --prompt "List the decisions, owners, deadlines, and unresolved risks."
```

Use a balanced model and lower reasoning effort:

```bash
openai-document-analyzer notes.md \
  --model gpt-5.6-terra \
  --reasoning-effort low \
  --verbosity low
```

Read a longer prompt from a file:

```bash
openai-document-analyzer contract.pdf --prompt-file review-prompt.txt
```

The module form is equivalent:

```bash
python -m openai_document_analyzer report.pdf
```

List the documented model profiles:

```bash
openai-document-analyzer --list-models
```

## Python API

```python
from openai_document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer(
    model="gpt-5.6-terra",
    reasoning_effort="medium",
    verbosity="medium",
    store=False,
)

result = analyzer.analyze_document(
    "report.pdf",
    "Summarize the conclusions and cite the supporting sections.",
)
print(result)
```

The client can be injected for custom networking, testing, or observability:

```python
from openai import OpenAI
from openai_document_analyzer import DocumentAnalyzer

client = OpenAI(timeout=60.0, max_retries=3)
analyzer = DocumentAnalyzer(client=client)
```

See the [API guide](docs/API.md) for the public interface and exceptions.

## Model profiles

| Model | Intended use |
| --- | --- |
| `gpt-5.6-sol` | Default; frontier capability for demanding analysis |
| `gpt-5.6-terra` | Balanced intelligence, latency, and cost |
| `gpt-5.6-luna` | Cost-efficient, higher-volume analysis |

The model list is guidance, not an allowlist. `--model` also accepts compatible
snapshots and future model IDs available to your OpenAI project. Evaluate output
quality, latency, and cost on representative documents before changing a
production default.

## Safety limits and privacy defaults

- Response storage is disabled unless `--store` is explicitly supplied.
- Files larger than 20 MiB are rejected before parsing.
- Extracted text longer than 200,000 characters is rejected before API use.
- Output is limited to 4,000 tokens by default.
- Document contents are labeled as untrusted data in the model instructions.
- API failures are raised as typed application errors; they are not returned as
  plausible analysis text.

Limits can be changed through CLI flags or constructor arguments. Raising a
limit can increase latency and cost.

## Legacy interactive command

The original version 1 command remains available during the v2 transition:

```bash
python scripts/text_analysis.py \
  examples/example_prompt.txt \
  examples/example_response.txt \
  examples/example_text_to_analyze.txt
```

New integrations should use the package CLI or Python API. See the
[v2 migration guide](docs/MIGRATION_V2.md).

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
pytest
python -m build
```

The test suite never calls the OpenAI API. All network behavior is mocked.

## Documentation

- [Configuration reference](docs/CONFIGURATION.md)
- [Python API](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Version 2 migration](docs/MIGRATION_V2.md)
- [Privacy and data handling](PRIVACY.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Support](SUPPORT.md)
- [Changelog](CHANGELOG.md)

## License and attribution

Released under the [MIT License](LICENSE).

OpenAI is a trademark of OpenAI, L.L.C. This independent project is not
affiliated with or endorsed by OpenAI.

Copyright © 2023–2026 Danilo Díaz Tarascó and contributors.
