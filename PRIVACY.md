# Privacy and Data Handling

## Data flow

1. The application reads a local TXT, Markdown, or PDF file.
2. PDF text extraction happens locally with `pypdf`.
3. The extracted text, analysis prompt, model configuration, and optional
   example are sent to the OpenAI API.
4. The returned text is printed to the terminal or returned to the caller.

The application does not upload the original PDF file. It does send the text
extracted from that file.

## Defaults

- OpenAI response storage is disabled by default with `store=False`.
- No application telemetry is collected.
- No document text or API response is written to disk by the package.
- `.env` and common local environment files are ignored by Git.
- Tests use injected mock clients and do not make API requests.

Passing `--store` or `store=True` changes the response-storage behavior for that
request. Review your OpenAI organization and project data controls separately.
OpenAI documents those controls in its
[data controls guide](https://developers.openai.com/api/docs/guides/your-data).

## Your responsibilities

Before analyzing a document:

- confirm that you are authorized to process it with a third-party API;
- remove data that is unnecessary for the analysis;
- understand applicable contractual, regulatory, residency, and retention
  requirements;
- avoid API keys, passwords, private keys, access tokens, and authentication
  material;
- evaluate whether the selected model and OpenAI project are approved for the
  data classification.

This project does not provide legal, privacy, or compliance advice.

## Safety identifier

Applications serving multiple end users may set `OPENAI_SAFETY_IDENTIFIER` to a
stable, privacy-preserving value. Hash or otherwise pseudonymize an internal
identifier before supplying it. Never use a person's name, email address, API
key, or other directly identifying value.

## Local logs and shell history

Prompts passed directly on the command line may be retained by shell history or
visible to local process inspection. Use `--prompt-file` when that distinction
matters and protect the prompt file according to its sensitivity.

Terminal output may also contain sensitive information derived from the
document. Redirect or save output only to an approved location.

## Reporting a privacy or security concern

Follow [`SECURITY.md`](SECURITY.md) for private reporting. Do not attach a real
sensitive document to a public issue.
