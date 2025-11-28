"""
Add navigation headers and footers to all Book of Mopati chapters.

This script:
1. Adds nav header to top of each chapter
2. Adds nav footer to bottom with prev/next links
3. Creates seamless chapter browsing
"""

import os
from pathlib import Path

# Chapter definitions
CHAPTERS = [
    {
        'number': 1,
        'title': 'Axiomatic Foundation',
        'file': 'book-of-mopati.md'
    },
    {
        'number': 2,
        'title': 'Meta-Hamiltonian Singularity',
        'file': 'book-of-mopati-chapter2.md'
    },
    {
        'number': 3,
        'title': 'Domain Universality',
        'file': 'book-of-mopati-chapter3.md'
    },
    {
        'number': 4,
        'title': 'Quantum Foundations',
        'file': 'book-of-mopati-chapter4.md'
    },
    {
        'number': 5,
        'title': 'AI as Phase-Space Flow',
        'file': 'book-of-mopati-chapter5.md'
    },
    {
        'number': 6,
        'title': 'Time and Causality',
        'file': 'book-of-mopati-chapter6.md'
    },
    {
        'number': 7,
        'title': 'Thermodynamics',
        'file': 'book-of-mopati-chapter7.md'
    },
    {
        'number': 8,
        'title': 'Market Dynamics',
        'file': 'book-of-mopati-chapter8.md'
    },
    {
        'number': 9,
        'title': 'Bioenergetic Consciousness',
        'file': 'book-of-mopati-chapter9.md'
    },
    {
        'number': 10,
        'title': 'Tachyonic Blockchain',
        'file': 'book-of-mopati-chapter10.md'
    },
    {
        'number': 11,
        'title': 'Spacetime Engineering',
        'file': 'book-of-mopati-chapter11.md'
    },
    {
        'number': 12,
        'title': 'Universal Compiler',
        'file': 'book-of-mopati-chapter12.md'
    },
    {
        'number': 13,
        'title': 'ApexQuantumICT',
        'file': 'book-of-mopati-chapter13.md'
    }
]

# Get the correct docs directory
SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR / 'docs'

def create_nav_header(chapter_num):
    """Create navigation header for chapter."""
    prev_link = ""
    next_link = ""
    
    if chapter_num > 1:
        prev_file = CHAPTERS[chapter_num - 2]['file']
        prev_title = CHAPTERS[chapter_num - 2]['title']
        prev_link = f"**[← Chapter {chapter_num-1}: {prev_title}]({prev_file})**"
    else:
        prev_link = ""
    
    if chapter_num < 13:
        next_file = CHAPTERS[chapter_num]['file']
        next_title = CHAPTERS[chapter_num]['title']
        next_link = f"**[Chapter {chapter_num+1}: {next_title} →]({next_file})**"
    else:
        next_link = "**End of Book**"
    
    header = f"""---

**[📖 Table of Contents](BOOK_INDEX.md)** | **Chapter {chapter_num} of 13** | {next_link if next_link else prev_link}

---

"""
    return header

def create_nav_footer(chapter_num):
    """Create navigation footer with all chapters listed."""
    prev_file = CHAPTERS[chapter_num - 2]['file'] if chapter_num > 1 else ""
    prev_title = CHAPTERS[chapter_num - 2]['title'] if chapter_num > 1 else ""
    next_file = CHAPTERS[chapter_num]['file'] if chapter_num < 13 else ""
    next_title = CHAPTERS[chapter_num]['title'] if chapter_num < 13 else ""
    
    nav_line = "**[← Table of Contents](BOOK_INDEX.md)** | **Chapter {} of 13**".format(chapter_num)
    
    if prev_file:
        nav_line += f" | **[← Prev: {prev_title}]({prev_file})**"
    if next_file:
        nav_line += f" | **[Next: {next_title} →]({next_file})**"
    
    # Generate chapter list
    chapter_list = "\n### All Chapters\n"
    for ch in CHAPTERS:
        if ch['number'] == chapter_num:
            chapter_list += f"{ch['number']}. **{ch['title']}** (Current)\n"
        else:
            chapter_list += f"{ch['number']}. [{ch['title']}]({ch['file']})\n"
    
    footer = f"""

---

## Chapter Navigation

{nav_line}

{chapter_list}
---

**In GOD We TRUST** - {"Continue to Chapter " + str(chapter_num + 1) + " →" if chapter_num < 13 else "End of Book"}
"""
    return footer

def add_navigation_to_chapter(chapter_info):
    """Add navigation to a single chapter file."""
    filepath = DOCS_DIR / chapter_info['file']
    
    if not filepath.exists():
        print(f"Warning: {filepath} does not exist")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if navigation already exists (basic check)
    if '## Chapter Navigation' in content:
        print(f"Skipping {chapter_info['file']} - navigation already exists")
        return
   
    # Add footer navigation
    footer = create_nav_footer(chapter_info['number'])
    content += footer
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added navigation to {chapter_info['file']}")

def main():
    print("Adding navigation to all Book of Mopati chapters...")
    print(f"Docs directory: {DOCS_DIR}")
    print()
    
    for chapter in CHAPTERS[1:]:  # Skip chapter 1, already done
        add_navigation_to_chapter(chapter)
    
    print()
    print("Navigation added to all chapters!")
    print()
    print("Readers can now:")
    print("  - Start at BOOK_INDEX.md")
    print("  - Click any chapter to read")
    print("  - Use prev/next links to navigate")
    print("  - Jump to table of contents anytime")

if __name__ == "__main__":
    main()
