# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| 2.x | Yes |
| 1.x | No |

Security fixes are applied to the latest release and the default branch.

## Reporting a vulnerability

Use GitHub
[private vulnerability reporting](https://github.com/ddtdanilo/OpenAI-Document-Analyzer/security/advisories/new)
for prompt-injection bypasses, unsafe data disclosure, credential exposure,
dependency compromise, workflow vulnerabilities, or other security-sensitive
issues.

Do not open a public issue or attach a real sensitive document. Include:

- affected version and environment;
- a minimal synthetic reproduction;
- expected and observed behavior;
- impact and realistic attack conditions;
- any proposed mitigation.

## Credential handling

- Store API keys in `.env`, a secret manager, or environment variables.
- Never embed a key in code, examples, command output, issues, or test fixtures.
- Use a restricted OpenAI project key and review usage limits.
- Rotate a key immediately if exposure is suspected.

## Scope boundaries

Model output is probabilistic and may be incorrect. Prompt-injection defenses
reduce risk but cannot guarantee that arbitrary hostile documents are safe.
Applications making consequential decisions must add domain-specific validation,
authorization, human review, and output handling.
