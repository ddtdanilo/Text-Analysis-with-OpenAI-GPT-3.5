# CLAUDE.md

Follow [`AGENTS.md`](AGENTS.md) as the authoritative repository instructions.

The canonical implementation is under `src/openai_document_analyzer/`.
The `scripts/` directory contains compatibility wrappers and must not become a
second implementation.

Before changing OpenAI models, request parameters, or prompts, consult current
official OpenAI developer documentation. Keep response storage opt-in,
documents classified as untrusted data, and all tests network-free.

Run before proposing a change:

```bash
ruff check .
ruff format --check .
pytest
python -m build
git diff --check
```
