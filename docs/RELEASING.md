# Releasing

Releases follow Semantic Versioning and are created from verified tags.

## Prepare

1. Confirm the default branch is green.
2. Choose the next version from user-visible compatibility impact.
3. Update the version in:
   - `pyproject.toml`
   - `src/openai_document_analyzer/__init__.py`
4. Move the relevant changelog entries from `Unreleased` to a dated version.
5. Update citation metadata when appropriate.
6. Open and merge a pull request containing only the release preparation.

## Validate

```bash
ruff check .
ruff format --check .
pytest
python -m build
python -m pip install --force-reinstall dist/*.whl
openai-document-analyzer --version
```

No live API call is required.

## Tag

Create a signed annotated tag from the exact verified default-branch commit:

```bash
git tag -s vX.Y.Z -m "OpenAI Document Analyzer vX.Y.Z"
git push origin vX.Y.Z
```

The release workflow verifies the package, confirms that the tag matches the
package version, builds source and wheel distributions, and creates the GitHub
Release with generated notes.

## Verify

- The tag points to the intended commit.
- The release workflow succeeded.
- The GitHub Release contains both distribution files.
- The installed wheel reports the expected version.
- README and changelog release links resolve.

If a release is incorrect, do not silently replace it. Publish a corrective
patch release unless a just-created, unused release contains no downstream user
impact and the correction is explicitly documented.
