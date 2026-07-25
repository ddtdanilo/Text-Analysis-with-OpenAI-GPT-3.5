"""Tests for the modern and compatibility command-line interfaces."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from openai_document_analyzer import ConfigurationError, cli


def test_list_models(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--list-models"]) == 0
    output = capsys.readouterr().out
    assert "gpt-5.6-sol (default)" in output
    assert "gpt-5.6-terra" in output


def test_main_analyzes_document(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    document = tmp_path / "document.txt"
    document.write_text("Body", encoding="utf-8")
    analyzer = Mock()
    analyzer.analyze_document.return_value = "Result"

    with patch("openai_document_analyzer.cli.DocumentAnalyzer", return_value=analyzer):
        result = cli.main(
            [
                str(document),
                "--prompt",
                "Find decisions",
                "--model",
                "gpt-5.6-terra",
                "--reasoning-effort",
                "low",
                "--verbosity",
                "high",
                "--store",
            ]
        )

    assert result == 0
    assert capsys.readouterr().out == "Result\n"
    analyzer.analyze_document.assert_called_once_with(
        document,
        "Find decisions",
        "gpt-5.6-terra",
    )


def test_main_reads_prompt_and_example_files(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    document = tmp_path / "document.txt"
    prompt = tmp_path / "prompt.txt"
    example_prompt = tmp_path / "example-prompt.txt"
    example_response = tmp_path / "example-response.txt"
    for path, value in [
        (document, "Body"),
        (prompt, "Extract actions"),
        (example_prompt, "Example request"),
        (example_response, "Example response"),
    ]:
        path.write_text(value, encoding="utf-8")

    analyzer = Mock()
    analyzer.load_text.return_value = "Loaded body"
    analyzer.ask_questions.return_value = "Guided result"
    with patch("openai_document_analyzer.cli.DocumentAnalyzer", return_value=analyzer):
        result = cli.main(
            [
                str(document),
                "--prompt-file",
                str(prompt),
                "--example-prompt",
                str(example_prompt),
                "--example-response",
                str(example_response),
            ]
        )

    assert result == 0
    assert capsys.readouterr().out == "Guided result\n"
    analyzer.ask_questions.assert_called_once_with(
        prompt="Extract actions",
        example_prompt="Example request",
        example_response="Example response",
        text_to_analyze="Loaded body",
        model=None,
    )


def test_main_reports_expected_errors(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    document = tmp_path / "document.txt"
    document.write_text("Body", encoding="utf-8")
    with patch(
        "openai_document_analyzer.cli.DocumentAnalyzer",
        side_effect=ConfigurationError("missing configuration"),
    ):
        assert cli.main([str(document)]) == 2
    assert "error: missing configuration" in capsys.readouterr().err


def test_main_requires_document() -> None:
    with pytest.raises(SystemExit, match="2"):
        cli.main([])


def test_main_requires_both_example_files(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="2"):
        cli.main(
            [
                str(tmp_path / "document.txt"),
                "--example-prompt",
                str(tmp_path / "prompt.txt"),
            ]
        )


def test_legacy_main_rejects_wrong_argument_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert cli.legacy_main([]) == 2
    assert "Usage:" in capsys.readouterr().err


def test_legacy_main_reports_initialization_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    files = [str(tmp_path / f"{index}.txt") for index in range(3)]
    with patch(
        "openai_document_analyzer.cli.DocumentAnalyzer",
        side_effect=ConfigurationError("missing key"),
    ):
        assert cli.legacy_main(files) == 2
    assert "error: missing key" in capsys.readouterr().err


def test_legacy_main_exits_cleanly(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    files = []
    for index, value in enumerate(("Example prompt", "Example response", "Document")):
        path = tmp_path / f"{index}.txt"
        path.write_text(value, encoding="utf-8")
        files.append(str(path))

    analyzer = Mock(default_model="gpt-5.6-sol")
    analyzer.load_text.return_value = "Document"
    with (
        patch("openai_document_analyzer.cli.DocumentAnalyzer", return_value=analyzer),
        patch("builtins.input", return_value="exit"),
    ):
        assert cli.legacy_main(files) == 0
    assert "Legacy interactive mode" in capsys.readouterr().out


def test_legacy_main_selects_model_and_answers(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    files = []
    for index, value in enumerate(("Example prompt", "Example response", "Document")):
        path = tmp_path / f"{index}.txt"
        path.write_text(value, encoding="utf-8")
        files.append(str(path))

    analyzer = Mock(default_model="gpt-5.6-sol")
    analyzer.load_text.return_value = "Document"
    analyzer.ask_questions.return_value = "Answer"
    with (
        patch("openai_document_analyzer.cli.DocumentAnalyzer", return_value=analyzer),
        patch(
            "builtins.input",
            side_effect=["model", "2", "", "What changed?", "exit"],
        ),
    ):
        assert cli.legacy_main(files) == 0

    output = capsys.readouterr().out
    assert "Using gpt-5.6-terra" in output
    assert "Answer" in output
    analyzer.ask_questions.assert_called_once_with(
        "What changed?",
        "Example prompt",
        "Example response",
        "Document",
        "gpt-5.6-terra",
    )


def test_legacy_main_accepts_custom_model_and_eof(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    files = []
    for index, value in enumerate(("Prompt", "Response", "Document")):
        path = tmp_path / f"{index}.txt"
        path.write_text(value, encoding="utf-8")
        files.append(str(path))

    analyzer = Mock(default_model="gpt-5.6-sol")
    analyzer.load_text.return_value = "Document"
    with (
        patch("openai_document_analyzer.cli.DocumentAnalyzer", return_value=analyzer),
        patch("builtins.input", side_effect=["model", "custom-snapshot", EOFError]),
    ):
        assert cli.legacy_main(files) == 0
    assert "Using custom-snapshot" in capsys.readouterr().out


def test_legacy_main_reports_analysis_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    files = []
    for index, value in enumerate(("Prompt", "Response", "Document")):
        path = tmp_path / f"{index}.txt"
        path.write_text(value, encoding="utf-8")
        files.append(str(path))

    analyzer = Mock(default_model="gpt-5.6-sol")
    analyzer.load_text.return_value = "Document"
    analyzer.ask_questions.side_effect = ConfigurationError("bad request")
    with (
        patch("openai_document_analyzer.cli.DocumentAnalyzer", return_value=analyzer),
        patch("builtins.input", side_effect=["Question", "exit"]),
    ):
        assert cli.legacy_main(files) == 0
    assert "error: bad request" in capsys.readouterr().err


def test_entrypoint_uses_main_result() -> None:
    with (
        patch("openai_document_analyzer.cli.main", return_value=7),
        pytest.raises(SystemExit, match="7"),
    ):
        cli.entrypoint()
