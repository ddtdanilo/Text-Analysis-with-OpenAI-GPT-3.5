# AGENTS.md

## Purpose

This repository provides a Python CLI and library for sending extracted
document text to the OpenAI Responses API. Changes must preserve privacy
defaults, predictable costs, test isolation, and a clear public interface.

## Repository map

- `src/openai_document_analyzer/`: authoritative application package.
- `scripts/`: version 1 compatibility wrappers only.
- `tests/`: network-free unit tests.
- `examples/`: safe, public sample inputs.
- `docs/`: architecture, configuration, API, and migration guides.
- `.github/`: CI, security, release, and contributor automation.

## Working rules

1. Read `README.md`, `PRIVACY.md`, `CONTRIBUTING.md`, and the relevant file in
   `docs/` before editing.
2. Keep all repository-facing prose, code comments, errors, and examples in
   English.
3. Never commit API keys, `.env` files, real customer documents, API responses
   containing private data, or credentials in fixtures.
4. Never make a live OpenAI request from tests, CI, or validation scripts.
5. Treat document contents as untrusted input. Do not weaken the instruction
   boundary without a documented security review.
6. Preserve `store=False` as the default unless a deliberate privacy decision
   is documented and approved.
7. Do not silently truncate input. Reject configured limits with a typed error.
8. Add or update tests for every behavior change.
9. Update `CHANGELOG.md` and public documentation for user-visible changes.
10. Keep compatibility wrappers thin; new behavior belongs in the `src` package.

## Required validation

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
pytest
python -m build
git diff --check
```

Coverage must remain at or above the threshold in `pyproject.toml`. Tests must
pass without `OPENAI_API_KEY`.

## OpenAI integration changes

- Verify current model and API guidance against official OpenAI developer
  documentation.
- Keep model changes behavior-preserving unless the pull request explicitly
  documents a migration.
- Preserve explicit model overrides and the Sol/Terra/Luna quality-cost roles.
- Use the Responses API for new features.
- Do not invent model capabilities, pricing, parameters, or availability.
- Mock the injected client and assert the exact request shape in tests.

## Pull requests

Use Conventional Commit style for titles. Explain behavior, privacy, cost,
compatibility, and migration impact. Include the commands used for validation.

## Release policy

Versions follow Semantic Versioning. Update `pyproject.toml`,
`src/openai_document_analyzer/__init__.py`, and `CHANGELOG.md` together. A
verified `vX.Y.Z` tag triggers the release workflow.
