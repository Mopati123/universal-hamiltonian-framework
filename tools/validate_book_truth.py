#!/usr/bin/env python3
"""Book of Mopati truth and mathematical consistency validator."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "book_manifest.json"

ALLOWED = {
    "standard_physics",
    "engineering_analogy",
    "research_hypothesis",
    "empirically_validated",
}
CERTIFIABLE_AUDIT = {"aligned"}

PROHIBITED_UNQUALIFIED_PATTERNS = {
    "universal_hamiltonian_literalism": re.compile(
        r"\\b(everything|all systems|any system)\\b.{0,80}\\b(is|are|possesses?|has)\\b.{0,80}\\bhamiltonian\\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "hamiltonian_minimizes_energy": re.compile(
        r"hamilton(?:'s|ian).{0,120}(minimi[sz](?:e|es|ed|ation)|spontaneously evolve.{0,40}minimum energy)",
        re.IGNORECASE | re.DOTALL,
    ),
    "classical_is_quantum_entanglement": re.compile(
        r"\\b(classical|oscillator)\\b.{0,100}\\b(entanglement|entangled)\\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "retrocausal_market_fact": re.compile(
        r"\\b(retrocausal(?:ity)?|future information backflow|tachyonic prediction)\\b.{0,100}\\b(price|market|trade|trading)\\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "consciousness_measurement": re.compile(
        r"\\b(measure(?:s|d|ment)?|quantif(?:y|ies|ied|ication))\\b.{0,100}\\b(consciousness|internal experience)\\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "unbreakable_crypto": re.compile(
        r"\\b(unbreakable|perfectly secure|guaranteed secure)\\b.{0,80}\\b(encryption|cryptograph|security)\\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "fabricated_performance_language": re.compile(
        r"\\b(advantage confirmed|proven profitable|production-ready|guaranteed profit)\\b",
        re.IGNORECASE,
    ),
}

REQUIRED_CHAPTER_FIELDS = {
    "number",
    "file",
    "title",
    "audit_status",
    "classifications",
    "evidence_status",
}


def load_manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    chapters = manifest.get("chapters", [])
    if manifest.get("book", {}).get("chapter_count") != len(chapters):
        errors.append("book.chapter_count does not match number of chapter records")

    numbers = [c.get("number") for c in chapters]
    if numbers != list(range(16)):
        errors.append(f"chapter numbering must be exactly 0..15; got {numbers!r}")

    for chapter in chapters:
        missing = REQUIRED_CHAPTER_FIELDS - chapter.keys()
        if missing:
            errors.append(f"chapter {chapter.get('number')} missing fields: {sorted(missing)}")
            continue
        classes = set(chapter["classifications"])
        unknown = classes - ALLOWED
        if unknown:
            errors.append(f"chapter {chapter['number']} has unknown classifications: {sorted(unknown)}")
        path = ROOT / chapter["file"]
        if not path.is_file():
            errors.append(f"chapter {chapter['number']} file missing: {chapter['file']}")

    canonical = manifest.get("book", {}).get("canonical_exercises")
    if not canonical or not (ROOT / canonical).is_file():
        errors.append("canonical exercise file is missing")

    return errors


def extract_python_blocks(markdown: str) -> list[str]:
    fence = chr(96) * 3
    pattern = re.escape(fence) + r"python\\s*\\n(.*?)" + re.escape(fence)
    return re.findall(pattern, markdown, flags=re.IGNORECASE | re.DOTALL)


def validate_python_syntax(chapter_path: Path) -> list[str]:
    errors: list[str] = []
    text = chapter_path.read_text(encoding="utf-8")
    for index, block in enumerate(extract_python_blocks(text), start=1):
        lowered = block.lower()
        if "# pseudocode" in lowered or "# pseudo-code" in lowered:
            continue
        try:
            ast.parse(block)
        except SyntaxError as exc:
            errors.append(
                f"{chapter_path.relative_to(ROOT)} python block {index} is not valid standalone syntax: "
                f"{exc.msg} (line {exc.lineno})"
            )
    return errors


def scan_claim_language(chapter_path: Path) -> list[str]:
    text = chapter_path.read_text(encoding="utf-8")
    errors: list[str] = []
    for name, pattern in PROHIBITED_UNQUALIFIED_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{chapter_path.relative_to(ROOT)} triggers claim rule: {name}")
    return errors


def validate_navigation_source() -> list[str]:
    errors: list[str] = []
    nav_script = ROOT / "add_book_navigation.py"
    if nav_script.is_file():
        text = nav_script.read_text(encoding="utf-8")
        if "of 13" in text or "chapter_num < 13" in text:
            errors.append(
                "add_book_navigation.py hard-codes obsolete chapter totals; navigation must derive from book_manifest.json"
            )
    return errors


def certification_errors(manifest: dict) -> list[str]:
    errors = validate_manifest(manifest)
    errors.extend(validate_navigation_source())

    for chapter in manifest.get("chapters", []):
        if chapter["audit_status"] not in CERTIFIABLE_AUDIT:
            errors.append(
                f"chapter {chapter['number']} is not certifiable: audit_status={chapter['audit_status']}"
            )
        path = ROOT / chapter["file"]
        if path.is_file():
            errors.extend(scan_claim_language(path))
            errors.extend(validate_python_syntax(path))

    if manifest.get("book", {}).get("certification_status") != "certified":
        errors.append(
            "book.certification_status is not 'certified'; certification remains blocked by design"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certify",
        action="store_true",
        help="Fail unless the complete Book of Mopati corpus is eligible for truth certification.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    errors = certification_errors(manifest) if args.certify else validate_manifest(manifest)

    if errors:
        label = "CERTIFICATION BLOCKED" if args.certify else "BOOK AUDIT SCHEMA INVALID"
        print(label)
        for item in errors:
            print(f"- {item}")
        return 1

    print("BOOK TRUTH VALIDATION PASS" if args.certify else "BOOK AUDIT SCHEMA PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
