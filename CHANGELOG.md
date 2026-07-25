# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.0.0] - 2026-07-25

### Added

- Installable `openai_document_analyzer` package and console command.
- GPT‑5.6 Sol, Terra, and Luna model profiles.
- Typed configuration, document, and API exceptions.
- Configurable file-size, character, output-token, reasoning, and verbosity
  controls.
- Markdown document support.
- Response-storage opt-in and optional privacy-preserving safety identifier.
- Architecture, API, configuration, migration, privacy, security, support,
  contribution, and agent documentation.
- Cross-version CI, CodeQL analysis, build verification, and tag-based releases.

### Changed

- Migrated model calls from Chat Completions to the Responses API.
- Raised the minimum Python version from 3.8 to 3.11.
- Replaced the interactive setup script with standard Python packaging.
- Rebuilt tests to avoid network access and enforce at least 95% coverage.
- Hardened prompts so document content is treated as untrusted data.
- Improved PDF extraction by preserving page boundaries and handling empty
  pages explicitly.

### Removed

- Retired GPT‑3.5 and GPT‑4 Turbo presets.
- Self-modifying coverage-badge workflow and generated SVG.
- Node-based semantic-release configuration.

### Breaking changes

- `DocumentAnalyzer.analyze_text()` and `analyze_document()` are synchronous.
- Expected operational failures now raise typed exceptions instead of returning
  error strings.
- The canonical imports moved from `scripts.document_analyzer` to
  `openai_document_analyzer`.

See [`docs/MIGRATION_V2.md`](docs/MIGRATION_V2.md) for upgrade examples.

## [1.0.3] - 2025-05-23

### Fixed

- Cleaned up duplicate README badges.

## [1.0.2] - 2025-05-23

### Fixed

- Corrected the initial semantic-release version configuration.

## [1.0.1] - 2025-05-23

### Fixed

- Improved PDF text extraction and version tracking.

## [1.0.0] - 2025-05-23

### Added

- Initial application, automated releases, and test suite.

[Unreleased]: https://github.com/ddtdanilo/OpenAI-Document-Analyzer/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/ddtdanilo/OpenAI-Document-Analyzer/compare/v1.0.3...v2.0.0
[1.0.3]: https://github.com/ddtdanilo/OpenAI-Document-Analyzer/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/ddtdanilo/OpenAI-Document-Analyzer/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/ddtdanilo/OpenAI-Document-Analyzer/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/ddtdanilo/OpenAI-Document-Analyzer/releases/tag/v1.0.0
