#!/usr/bin/env python3
"""Sync template registry table into docs/flutter-template-guide.md."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

DOC_PATH = REPO_ROOT / "docs" / "flutter-template-guide.md"
START_MARKER = "<!-- TEMPLATE_REGISTRY_TABLE:START -->"
END_MARKER = "<!-- TEMPLATE_REGISTRY_TABLE:END -->"


def _render_registry_table() -> str:
    """Build markdown table from template registry metadata."""
    from fwen.template_registry import get_template_registry

    lines = [
        "| Template ID | Layer | CLI Dependencies | Source Path | Output Path | Scenario |"
        " Mutually Exclusive With | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for template in get_template_registry():
        cli_dependencies = (
            ", ".join(template.cli_dependencies) if template.cli_dependencies else "always"
        )
        mutually_exclusive_with = (
            ", ".join(template.mutually_exclusive_with) if template.mutually_exclusive_with else "-"
        )
        lines.append(
            "| "
            f"`{template.template_id}`"
            f" | `{template.layer}`"
            f" | {cli_dependencies}"
            f" | `{template.source_path}`"
            f" | `{template.output_path}`"
            f" | {template.scenario}"
            f" | {mutually_exclusive_with}"
            f" | `{template.status}`"
            " |"
        )

    return "\n".join(lines)


def _sync_content(content: str) -> str:
    """Return content with generated registry table injected."""
    if START_MARKER not in content or END_MARKER not in content:
        raise ValueError(f"Missing sync markers in {DOC_PATH}: {START_MARKER} / {END_MARKER}")

    start = content.index(START_MARKER) + len(START_MARKER)
    end = content.index(END_MARKER)
    generated = "\n\n" + _render_registry_table() + "\n\n"
    return content[:start] + generated + content[end:]


def sync_template_guide(check_only: bool) -> int:
    """Sync registry table into docs, or verify that docs are in sync."""
    current = DOC_PATH.read_text()
    synced = _sync_content(current)

    if check_only:
        if current == synced:
            print("Template guide is in sync with template_registry.")
            return 0
        print("Template guide is out of sync. Run:\n  uv run python scripts/sync_template_guide.py")
        return 1

    DOC_PATH.write_text(synced)
    print(f"Updated {DOC_PATH}")
    return 0


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Sync template registry docs.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if docs are in sync and exit non-zero when drift exists.",
    )
    args = parser.parse_args()
    return sync_template_guide(check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
