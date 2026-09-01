#!/usr/bin/env python3
"""Backward-compatible entry point for Book of Mopati navigation generation.

The canonical implementation is tools/generate_book_navigation.py and derives
all chapter numbers and links from docs/book_manifest.json.
"""

from tools.generate_book_navigation import main

if __name__ == "__main__":
    raise SystemExit(main())
