[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

# Book Translator

Digitize scanned academic books → OCR → Translate → Formatted docx.

## Why This Tool?

Researchers in literature, social sciences, and humanities frequently need to engage with English-language monographs for close reading and analysis. In practice, this is harder than it should be:

1. **Unsearchable scans.** Researchers in non-English-speaking countries regularly work with scanned PDFs that cannot be searched, copied, or cited directly.
2. **Degraded sources.** Classic and out-of-print academic books are often available only as poor-quality scans with no digital text layer.
3. **Time cost.** Manual transcription and translation of book-length texts is prohibitively time-consuming.
4. **Format gap.** Existing OCR tools produce raw text dumps, not research-friendly documents with structure, page references, and terminology support.

Book Translator addresses these problems by combining **macOS native Vision OCR** (zero API cost), **AI-powered translation**, and **automated docx formatting** into a single pipeline.

## Features

- **macOS Vision framework OCR** — ~95%+ accuracy on printed English text, no cloud API required
- **Page-accurate extraction** — text output includes `=== p.XX ===` markers tied to original page numbers
- **Parallel translation** — long chapters are split into batches and translated concurrently via Claude Code sub-agents
- **Professional docx output** — title page, clickable table of contents, section headings, and page markers
- **Terminology appendix** — auto-generated from user-provided term lists
- **Configurable formatting** — fonts, sizes, and heading structure are all adjustable
- **EN→JA translation** — designed for English-to-Japanese academic translation, extensible to other language pairs
- **Claude Code skill integration** — import as a skill for a one-command workflow

## Requirements

- **macOS** (Apple Silicon or Intel) — required for the Vision framework
- **Python 3.9+**
- Python packages: `pymupdf`, `python-docx`, `pyobjc-framework-Vision`, `pyobjc-framework-Quartz`

## Installation

```bash
git clone https://github.com/MuchenHan/book-translator.git
cd book-translator
pip install -r requirements.txt
```

## Usage

### Step 1: OCR — PDF to Page-Marked Text

```bash
python3 scripts/ocr_vision.py input.pdf output_dir --start-page 81 --dpi 150 --lang en
```

- Extracts page images at the specified DPI and runs macOS Vision OCR on each page.
- Output: `output_dir/all_pages.txt` with `=== p.XX ===` page markers.
- For poor-quality scans, increase DPI to 200–300 for better recognition accuracy.

### Step 2: Translate

For chapters exceeding ~5,000 words, split the text at page boundaries into ~3,000-word batches and translate them in parallel. This keeps each batch within model context limits and significantly reduces total translation time.

### Step 3: Build Docx

```bash
python3 scripts/build_docx.py ja_complete.txt output.docx \
  --title "Book Title" \
  --subtitle "Original Title" \
  --author "Author Name" \
  --year "1957" \
  --font "Yu Mincho" \
  --font-size 11 \
  --terms-file terminology.txt \
  --sections "Section1:1,Section2:2"
```

This generates a professionally formatted `.docx` file with:

- A title page with book metadata
- A clickable table of contents
- Section headings mapped to page ranges
- A terminology appendix (if `--terms-file` is provided)

## Claude Code Integration

This project includes a Claude Code skill definition (`SKILL.md`). If you use [Claude Code](https://claude.com/claude-code), you can import it as a skill for a streamlined one-command workflow that handles OCR, translation, and docx generation in sequence.

## Translation Guide

See [references/translation-guide.md](references/translation-guide.md) for detailed translation conventions, including:

- Academic である調 style (the standard register for Japanese academic writing)
- Technical term formatting rules (original English in parentheses on first occurrence)
- Parallel translation strategy for book-length texts

## Use Cases

- **Digitizing academic classics** — psychology, philosophy, sociology monographs (e.g., Skinner's *Verbal Behavior*)
- **Preserving rare texts** — personal research digitization of out-of-print books available only as scans
- **Cross-language reading support** — helping graduate students and researchers engage with English-language scholarship

## Contributing

Contributions are welcome. Please feel free to submit issues and pull requests. If you extend the tool to support additional language pairs or output formats, a PR would be appreciated.

## License

MIT License — see [LICENSE](LICENSE).
