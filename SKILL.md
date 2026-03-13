---
name: book-translator
description: OCR scanned book PDFs and translate into formatted Japanese docx. Use when asked to digitize, OCR, or translate book chapters/papers from PDF scans. Produces page-accurate docx with clickable TOC, section headings, and terminology appendix. Supports parallel translation via sub-agents for long chapters.
---

# Book Translator

Digitize scanned book chapters (PDF) → OCR → translate (EN→JA) → formatted docx.

## Dependencies

```bash
pip install pymupdf python-docx pyobjc-framework-Vision pyobjc-framework-Quartz
```

## Workflow

### 1. OCR: PDF → Page-Marked Text

```bash
python3 scripts/ocr_vision.py <input.pdf> <output_dir> --start-page 81 --dpi 150 --lang en
```

- Extracts images at specified DPI, runs macOS Vision OCR
- Output: `output_dir/all_pages.txt` with `=== p.XX ===` markers per page
- Individual pages also saved as `output_dir/pXXX.txt`
- For higher quality on key pages, use Gemini vision API as supplement (if quota available)

### 2. Translate: Parallel Sub-Agents

For chapters > 5,000 words, split source at page boundaries into ~3,000-word batches.

```bash
# Split example (adjust line numbers per page markers)
sed -n '1,298p' source.txt > part1.txt
sed -n '299,600p' source.txt > part2.txt
sed -n '601,$p' source.txt > part3.txt
```

Spawn parallel sub-agents (Scholar, Writer, APF-Writer or any available):

```
sessions_spawn(agentId="scholar", label="translate-1", mode="run", task="...")
sessions_spawn(agentId="writer", label="translate-2", mode="run", task="...")
sessions_spawn(agentId="apf-writer", label="translate-3", mode="run", task="...")
```

See `references/translation-guide.md` for prompt template and terminology management.

After all complete, merge and verify page continuity:

```bash
cat ja_part_1.txt ja_part_2.txt ja_part_3.txt > ja_complete.txt
grep "=== p\." ja_complete.txt | sort -t. -k2 -n  # verify no gaps
```

Fill any missing pages manually if sub-agents skipped.

### 3. Build Docx

```bash
python3 scripts/build_docx.py ja_complete.txt output.docx \
  --title "言語行動" \
  --subtitle "Verbal Behavior" \
  --author "B.F. スキナー（B.F. Skinner）" \
  --year "1957" \
  --font "Yu Mincho" \
  --font-size 11 \
  --terms-file terminology.txt \
  --sections "タクト:1,拡張タクト:1,般化的拡張:2,隠喩的拡張:2,抽象化:1"
```

Options:
- `--sections`: Comma-separated heading titles. Append `:N` for heading level (default 2)
- `--terms-file`: Auto-generates terminology appendix table. Format: `english → japanese` or TSV
- TOC: clickable Word field (right-click → Update Field in Word)

### 4. Deliver

Send the docx to the user via `message(action=send, filePath=...)`.

## Key Notes

- macOS Vision OCR works well for printed English text; accuracy ~95%+
- For poor scans, increase DPI to 200-300
- Always verify page count: `grep -c "=== p\." file.txt`
- Gemini Flash vision gives higher OCR quality but has daily quota limits (free tier: ~20 req/day)
- Translation quality check: spot-check 2-3 pages after merge, especially at batch boundaries
