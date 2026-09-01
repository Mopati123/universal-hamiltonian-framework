#!/usr/bin/env python3
"""Generate Book of Mopati navigation from the canonical manifest."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "book_manifest.json"
START = "<!-- BOOK_NAV_START -->"
END = "<!-- BOOK_NAV_END -->"


def load_chapters() -> list[dict]:
    with MANIFEST.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return data["chapters"]


def rel_docs_path(path: str) -> str:
    prefix = "docs/"
    return path[len(prefix):] if path.startswith(prefix) else path


def render_nav(chapters: list[dict], index: int) -> str:
    current = chapters[index]
    total = len(chapters)
    parts = ["[Table of Contents](BOOK_INDEX.md)", f"Chapter {current['number']} of {total - 1}"]
    if index > 0:
        prev = chapters[index - 1]
        parts.append(f"[Previous: {prev['title']}]({rel_docs_path(prev['file'])})")
    if index + 1 < total:
        nxt = chapters[index + 1]
        parts.append(f"[Next: {nxt['title']}]({rel_docs_path(nxt['file'])})")
    return START + "\n\n" + " | ".join(parts) + "\n\n" + END


def replace_or_insert(text: str, nav: str) -> str:
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        return before.rstrip() + "\n\n" + nav + after
    lines = text.splitlines()
    insert_at = 1 if lines else 0
    lines[insert_at:insert_at] = ["", nav, ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    chapters = load_chapters()
    for index, chapter in enumerate(chapters):
        path = ROOT / chapter["file"]
        text = path.read_text(encoding="utf-8")
        path.write_text(replace_or_insert(text, render_nav(chapters, index)), encoding="utf-8")
        print(f"updated {chapter['file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
