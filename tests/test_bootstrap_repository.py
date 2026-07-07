from pathlib import Path

from scripts.bootstrap_repository import bootstrap


def test_bootstrap_dry_run_does_not_create_output_directories(tmp_path: Path) -> None:
    config_path = tmp_path / "client-config.yaml"
    config_path.write_text(
        """client:
  name: Example B2B SaaS Client
automation:
  output_dir: generated-output
""",
        encoding="utf-8",
    )

    messages = bootstrap(config_path, dry_run=True)

    assert any("Would create directory" in message for message in messages)
    assert not (tmp_path / "generated-output").exists()
