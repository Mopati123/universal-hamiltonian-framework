#!/usr/bin/env python3
"""Fail-closed validation for the Book of Mopati truth-aligned edition."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "book_manifest.json"
INDEX_PATH = ROOT / "docs" / "BOOK_INDEX.md"

ALLOWED = {
    "standard_physics",
    "engineering_analogy",
    "research_hypothesis",
    "empirically_validated",
}

REQUIRED_CHAPTER_FIELDS = {
    "number",
    "file",
    "title",
    "audit_status",
    "classifications",
    "evidence_status",
}

# Exact legacy formulations that must never return as affirmative Book claims.
LEGACY_OVERCLAIMS = (
    "everything is hamiltonian. not metaphorically",
    "everything that exists can be expressed as a hamiltonian",
    "all change occurs through the canonical equations",
    "systems spontaneously evolve toward minimum energy",
    "same algorithm. different domains. universal truth",
    "what follows is not metaphor. it's measurement",
    "the framework exhibits proto-consciousness",
    "faster-than-light information is mathematically consistent, thermodynamically valid, and practically applicable",
    "this is the equation governing everything",
    "unified field theory of everything",
    "information = energy = consciousness (proven)",
    "not metaphor. mathematical equivalence",
    "future information backflow",
    "advantage confirmed",
    "proven profitable",
    "guaranteed profit",
    "production-ready for ict/fvg trading",
)

REQUIRED_BANNER_LABELS = (
    "**Classification:**",
    "**Evidence:**",
    "**Certification scope:**",
)


def load_manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        return cast(dict[str, Any], json.load(fh))


def chapter_paths(manifest: dict) -> list[Path]:
    return [ROOT / c["file"] for c in manifest["chapters"]]


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    book = manifest.get("book", {})
    chapters = manifest.get("chapters", [])

    if book.get("chapter_count") != 16:
        errors.append("book.chapter_count must be 16")
    if len(chapters) != 16:
        errors.append(f"manifest must contain 16 chapters; got {len(chapters)}")

    numbers = [c.get("number") for c in chapters]
    if numbers != list(range(16)):
        errors.append(f"chapter numbering must be exactly 0..15; got {numbers!r}")

    if set(manifest.get("allowed_classifications", [])) != ALLOWED:
        errors.append("allowed_classifications must equal the canonical four-class taxonomy")

    seen_files: set[str] = set()
    for chapter in chapters:
        missing = REQUIRED_CHAPTER_FIELDS - chapter.keys()
        if missing:
            errors.append(f"chapter {chapter.get('number')} missing fields: {sorted(missing)}")
            continue

        if chapter["file"] in seen_files:
            errors.append(f"duplicate chapter file in manifest: {chapter['file']}")
        seen_files.add(chapter["file"])

        unknown = set(chapter["classifications"]) - ALLOWED
        if unknown:
            errors.append(
                f"chapter {chapter['number']} has unknown classifications: {sorted(unknown)}"
            )

        path = ROOT / chapter["file"]
        if not path.is_file():
            errors.append(f"chapter {chapter['number']} file missing: {chapter['file']}")

    canonical = book.get("canonical_exercises")
    if canonical != "docs/chapter0-exercises.md":
        errors.append("canonical exercise path must be docs/chapter0-exercises.md")
    elif not (ROOT / canonical).is_file():
        errors.append("canonical exercise file is missing")

    duplicate = ROOT / "docs" / "chapter0-exercises-COMPLETE.md"
    if duplicate.exists():
        errors.append("duplicate Chapter 0 exercise authority still exists")

    return errors


def validate_chapter_banner(chapter: dict) -> list[str]:
    errors: list[str] = []
    path = ROOT / chapter["file"]
    text = path.read_text(encoding="utf-8")
    header = "\n".join(text.splitlines()[:12])

    for label in REQUIRED_BANNER_LABELS:
        if label not in header:
            errors.append(f"{chapter['file']} missing required banner label {label}")

    for classification in chapter["classifications"]:
        if classification not in header:
            errors.append(
                f"{chapter['file']} manifest classification {classification} is absent from chapter banner"
            )

    return errors


def extract_fenced_blocks(text: str, language: str) -> list[str]:
    patterns = (
        rf"`{{3}}{language}\s*\n(.*?)`{{3}}",
        rf"~{{3}}{language}\s*\n(.*?)~{{3}}",
    )
    blocks: list[str] = []
    for pattern in patterns:
        blocks.extend(re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL))
    return blocks


def validate_python_blocks(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for index, block in enumerate(extract_fenced_blocks(text, "python"), start=1):
        lowered = block.lower()
        if "# pseudocode" in lowered or "# pseudo-code" in lowered:
            continue
        try:
            ast.parse(block)
        except SyntaxError as exc:
            errors.append(
                f"{path.relative_to(ROOT)} python block {index} has invalid syntax: "
                f"{exc.msg} line {exc.lineno}"
            )
    return errors


def validate_json_blocks(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for index, block in enumerate(extract_fenced_blocks(text, "json"), start=1):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(
                f"{path.relative_to(ROOT)} JSON block {index} is invalid JSON: "
                f"{exc.msg} line {exc.lineno}"
            )
    return errors


def scan_legacy_overclaims(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").lower()
    errors: list[str] = []
    for phrase in LEGACY_OVERCLAIMS:
        if phrase in text:
            errors.append(f"{path.relative_to(ROOT)} contains prohibited legacy claim: {phrase}")
    return errors


def validate_navigation_source() -> list[str]:
    errors: list[str] = []
    generator = ROOT / "tools" / "generate_book_navigation.py"
    wrapper = ROOT / "add_book_navigation.py"

    if not generator.is_file():
        errors.append("canonical navigation generator is missing")
    else:
        text = generator.read_text(encoding="utf-8")
        if "book_manifest.json" not in text:
            errors.append("navigation generator must derive chapter data from book_manifest.json")

    if not wrapper.is_file():
        errors.append("navigation compatibility entry point is missing")
    else:
        text = wrapper.read_text(encoding="utf-8")
        for stale in ("of 13", "of 14", "chapter_num < 13", "chapter_num < 14"):
            if stale in text:
                errors.append(f"navigation wrapper contains stale hard-coded count: {stale}")

    return errors


def validate_index() -> list[str]:
    errors: list[str] = []
    if not INDEX_PATH.is_file():
        return ["docs/BOOK_INDEX.md is missing"]

    text = INDEX_PATH.read_text(encoding="utf-8")
    lowered = text.lower()

    if "16 chapters" not in lowered:
        errors.append("BOOK_INDEX.md must declare the canonical 16-chapter corpus")

    for classification in ALLOWED:
        if classification not in text:
            errors.append(f"BOOK_INDEX.md does not document classification {classification}")

    # The index may discuss rejected claims, but must not contain the strongest old slogans.
    for phrase in (
        "not metaphorically. **literally.**",
        "**everything is hamiltonian.**",
        "**every claim is verifiable.**",
    ):
        if phrase in lowered:
            errors.append(f"BOOK_INDEX.md contains obsolete certification slogan: {phrase}")

    return errors


def structural_errors(manifest: dict) -> list[str]:
    errors = validate_manifest(manifest)
    errors.extend(validate_navigation_source())
    errors.extend(validate_index())

    for chapter in manifest.get("chapters", []):
        path = ROOT / chapter["file"]
        if not path.is_file():
            continue
        errors.extend(validate_chapter_banner(chapter))
        errors.extend(validate_python_blocks(path))
        errors.extend(validate_json_blocks(path))
        errors.extend(scan_legacy_overclaims(path))

    canonical_exercises = ROOT / manifest.get("book", {}).get(
        "canonical_exercises", "docs/chapter0-exercises.md"
    )
    if canonical_exercises.is_file():
        errors.extend(validate_python_blocks(canonical_exercises))
        errors.extend(validate_json_blocks(canonical_exercises))
        errors.extend(scan_legacy_overclaims(canonical_exercises))

    return errors


def certification_errors(manifest: dict) -> list[str]:
    errors = structural_errors(manifest)

    for chapter in manifest.get("chapters", []):
        if chapter["audit_status"] != "aligned":
            errors.append(
                f"chapter {chapter['number']} is not aligned: audit_status={chapter['audit_status']}"
            )

    if manifest.get("book", {}).get("certification_status") != "certified":
        errors.append("book.certification_status must be 'certified' for certification")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certify",
        action="store_true",
        help="Require the complete Book corpus to satisfy truth certification.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    errors = certification_errors(manifest) if args.certify else structural_errors(manifest)

    if errors:
        print("CERTIFICATION BLOCKED" if args.certify else "BOOK VALIDATION FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("BOOK TRUTH CERTIFICATION PASS" if args.certify else "BOOK STRUCTURAL VALIDATION PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
