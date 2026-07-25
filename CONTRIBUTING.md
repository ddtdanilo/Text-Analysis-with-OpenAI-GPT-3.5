# Contributing

Thank you for improving OpenAI Document Analyzer.

## Before opening a change

- Search existing issues and pull requests.
- Open an issue before a substantial feature or public API change.
- Do not include real private documents, API keys, or captured production
  responses.
- Review the [privacy policy](PRIVACY.md) and
  [architecture](docs/ARCHITECTURE.md).

## Local setup

```bash
git clone https://github.com/ddtdanilo/OpenAI-Document-Analyzer.git
cd OpenAI-Document-Analyzer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

An API key is not required to run the test suite.

## Development workflow

1. Create a focused branch from `main`.
2. Implement the smallest coherent change.
3. Add tests that fail without the change.
4. Update the relevant documentation and changelog.
5. Run:

   ```bash
   ruff check .
   ruff format --check .
   pytest
   python -m build
   git diff --check
   ```

6. Open a pull request and complete its checklist.

## Code standards

- Support every Python version declared in `pyproject.toml`.
- Add type annotations to public and internal functions.
- Raise a domain-specific exception for an expected operational failure.
- Avoid broad exception handling.
- Keep file and network operations bounded.
- Inject the OpenAI client when testability or custom configuration matters.
- Keep prompts lean, explicit, and resistant to instructions inside documents.
- Keep tests deterministic and network-free.

Ruff is the source of truth for linting and formatting. Do not add competing
formatter configuration.

## Testing OpenAI behavior

Mock `client.responses.create` and assert the complete request surface relevant
to the change. Do not use a real API key, recorded customer response, or live
model call in a test.

Model migrations must link official OpenAI documentation and explain effects on
quality, latency, cost, parameters, and compatibility.

## Commits and releases

Use clear, imperative Conventional Commit subjects:

```text
feat: add Markdown document support
fix: preserve PDF page boundaries
docs: explain response storage
test: cover empty API responses
```

Version and release changes follow the policy in `AGENTS.md` and
[`docs/RELEASING.md`](docs/RELEASING.md).

## License and conduct

By contributing, you agree that your contribution may be distributed under the
MIT License. Participation is governed by
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
