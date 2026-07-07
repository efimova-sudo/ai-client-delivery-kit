from pathlib import Path

from scripts.validate_prompt_library import validate_library


def write_prompt(path: Path, prompt_id: str = "sample.v1", category: str = "sample") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
id: {prompt_id}
version: 1.0.0
owner: delivery-ops
status: stable
category: {category}
inputs:
  - source
outputs:
  - summary
---

# Sample Prompt

Summarize the provided source.
""",
        encoding="utf-8",
    )


def test_validate_library_accepts_valid_prompt(tmp_path: Path) -> None:
    root = tmp_path / "prompts"
    write_prompt(root / "sample" / "sample.md")

    assert validate_library(root) == []


def test_validate_library_rejects_missing_frontmatter(tmp_path: Path) -> None:
    root = tmp_path / "prompts"
    prompt_path = root / "sample" / "sample.md"
    prompt_path.parent.mkdir(parents=True)
    prompt_path.write_text("# Missing Metadata\n", encoding="utf-8")

    errors = validate_library(root)

    assert any("missing YAML frontmatter" in error for error in errors)


def test_validate_library_rejects_duplicate_ids(tmp_path: Path) -> None:
    root = tmp_path / "prompts"
    write_prompt(root / "sample" / "one.md", prompt_id="duplicate.v1")
    write_prompt(root / "sample" / "two.md", prompt_id="duplicate.v1")

    errors = validate_library(root)

    assert any("duplicate prompt id" in error for error in errors)


def test_validate_library_rejects_category_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "prompts"
    write_prompt(root / "sample" / "sample.md", category="other")

    errors = validate_library(root)

    assert any("does not match folder" in error for error in errors)
