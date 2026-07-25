# Configuration Reference

## Environment variables

The package loads `.env` with `python-dotenv` and also honors process
environment variables.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes, unless a client is injected | — | OpenAI project API key |
| `OPENAI_MODEL` | No | `gpt-5.6-sol` | Default model ID |
| `OPENAI_SAFETY_IDENTIFIER` | No | — | Stable privacy-preserving end-user identifier |

Constructor arguments and CLI flags take precedence over environment defaults.

Never set `OPENAI_SAFETY_IDENTIFIER` to a name, email address, API key, or
another directly identifying value.

## CLI options

```text
openai-document-analyzer [-h] [-p PROMPT | --prompt-file PATH]
                         [--model MODEL]
                         [--example-prompt PATH --example-response PATH]
                         [--reasoning-effort {none,low,medium,high,xhigh,max}]
                         [--verbosity {low,medium,high}]
                         [--max-characters N]
                         [--max-output-tokens N]
                         [--store] [--list-models] [--version]
                         [document]
```

| Option | Default | Notes |
| --- | --- | --- |
| `document` | Required | TXT, Markdown, or text-based PDF |
| `--prompt` | Summary prompt | Direct analysis request |
| `--prompt-file` | — | Reads the request from a UTF-8 file |
| `--model` | Environment or `gpt-5.6-sol` | Accepts compatible model IDs |
| `--reasoning-effort` | `medium` | Higher values can increase latency and usage |
| `--verbosity` | `medium` | Controls answer detail |
| `--max-characters` | `200000` | Rejects extracted text above the limit |
| `--max-output-tokens` | `4000` | Bounds generated output |
| `--store` | Disabled | Explicitly permits response storage |

`--prompt` and `--prompt-file` are mutually exclusive.
`--example-prompt` and `--example-response` must be used together.

## Python constructor

```python
DocumentAnalyzer(
    api_key=None,
    model=None,
    *,
    client=None,
    max_characters=200_000,
    max_file_bytes=20 * 1024 * 1024,
    max_output_tokens=4_000,
    reasoning_effort="medium",
    verbosity="medium",
    store=False,
    safety_identifier=None,
)
```

Passing `client` bypasses local API-key resolution and allows the caller to
configure retries, timeouts, transport, and observability with the OpenAI SDK.

## Model selection

- Start with `gpt-5.6-sol` when quality is the primary requirement.
- Evaluate `gpt-5.6-terra` for a quality/cost balance.
- Evaluate `gpt-5.6-luna` for cost-sensitive, higher-volume use.

Use representative documents and prompts to measure accuracy, completeness,
latency, and cost. Do not assume a lower-cost profile is acceptable without an
evaluation.

Model availability and pricing are controlled by OpenAI and may change. Consult
the [official model catalog](https://developers.openai.com/api/docs/models).

## File and character limits

File-size checks happen before reading or parsing. Character checks happen
after text extraction and whitespace normalization. The package rejects limits
instead of silently truncating, because silent truncation can invalidate an
analysis.

For documents above the configured limit, split the source into meaningful
sections and analyze them separately. A production summarization pipeline should
add explicit chunking, per-section provenance, and a tested aggregation step.
