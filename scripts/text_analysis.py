#!/usr/bin/env python3
"""Compatibility entry point for the version 1.x interactive interface."""

from openai_document_analyzer.cli import legacy_main

if __name__ == "__main__":
    raise SystemExit(legacy_main())
