"""Command-line interface for OpenAI Document Analyzer."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from openai_document_analyzer import (
    DEFAULT_MODEL,
    MODEL_PROFILES,
    DocumentAnalyzer,
    DocumentAnalyzerError,
    __version__,
)

DEFAULT_PROMPT = "Summarize the document and identify its key points."


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="openai-document-analyzer",
        description="Analyze TXT, Markdown, and PDF documents with OpenAI.",
    )
    parser.add_argument("document", nargs="?", type=Path, help="Document to analyze")
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument("-p", "--prompt", help="Analysis request")
    prompt_group.add_argument(
        "--prompt-file",
        type=Path,
        help="Read the analysis request from a UTF-8 file",
    )
    parser.add_argument("--model", help=f"OpenAI model (default: {DEFAULT_MODEL})")
    parser.add_argument("--example-prompt", type=Path, help="Few-shot example request")
    parser.add_argument("--example-response", type=Path, help="Few-shot example response")
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="medium",
    )
    parser.add_argument(
        "--verbosity",
        choices=("low", "medium", "high"),
        default="medium",
    )
    parser.add_argument("--max-characters", type=int, default=200_000)
    parser.add_argument("--max-output-tokens", type=int, default=4_000)
    parser.add_argument(
        "--store",
        action="store_true",
        help="Allow OpenAI to store the response (disabled by default)",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List documented model profiles and exit",
    )
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the modern command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_models:
        for model, description in MODEL_PROFILES:
            marker = " (default)" if model == DEFAULT_MODEL else ""
            print(f"{model}{marker}: {description}")
        return 0

    if args.document is None:
        parser.error("the following arguments are required: document")
    if bool(args.example_prompt) != bool(args.example_response):
        parser.error("--example-prompt and --example-response must be used together")

    try:
        prompt = (
            args.prompt_file.read_text(encoding="utf-8").strip()
            if args.prompt_file
            else args.prompt or DEFAULT_PROMPT
        )
        analyzer = DocumentAnalyzer(
            model=args.model,
            max_characters=args.max_characters,
            max_output_tokens=args.max_output_tokens,
            reasoning_effort=args.reasoning_effort,
            verbosity=args.verbosity,
            store=args.store,
        )
        if args.example_prompt:
            result = analyzer.ask_questions(
                prompt=prompt,
                example_prompt=args.example_prompt.read_text(encoding="utf-8"),
                example_response=args.example_response.read_text(encoding="utf-8"),
                text_to_analyze=analyzer.load_text(args.document),
                model=args.model,
            )
        else:
            result = analyzer.analyze_document(args.document, prompt, args.model)
    except (DocumentAnalyzerError, FileNotFoundError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(result)
    return 0


def legacy_main(argv: Sequence[str] | None = None) -> int:
    """Run the v1 three-file interactive interface."""
    arguments = list(argv if argv is not None else sys.argv[1:])
    if len(arguments) != 3:
        print(
            "Usage: python scripts/text_analysis.py <example_prompt> <example_response> <document>",
            file=sys.stderr,
        )
        return 2

    example_prompt_path, example_response_path, document_path = map(Path, arguments)
    try:
        analyzer = DocumentAnalyzer()
        example_prompt = example_prompt_path.read_text(encoding="utf-8")
        example_response = example_response_path.read_text(encoding="utf-8")
        document = analyzer.load_text(document_path)
    except (DocumentAnalyzerError, FileNotFoundError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print("Legacy interactive mode. Type a question, 'model' to select a model, or 'exit' to quit.")
    current_model = analyzer.default_model
    while True:
        try:
            prompt = input("\nQuestion: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if prompt.lower() == "exit":
            return 0
        if prompt.lower() == "model":
            for index, (model, description) in enumerate(MODEL_PROFILES, 1):
                print(f"{index}. {model} — {description}")
            selection = input("Model number or ID: ").strip()
            if selection.isdigit() and 1 <= int(selection) <= len(MODEL_PROFILES):
                current_model = MODEL_PROFILES[int(selection) - 1][0]
            elif selection:
                current_model = selection
            print(f"Using {current_model}")
            continue
        if not prompt:
            continue
        try:
            answer = analyzer.ask_questions(
                prompt,
                example_prompt,
                example_response,
                document,
                current_model,
            )
        except DocumentAnalyzerError as exc:
            print(f"error: {exc}", file=sys.stderr)
            continue
        print(f"\n{answer}")


def entrypoint() -> None:
    """Console-script entry point."""
    raise SystemExit(main())
