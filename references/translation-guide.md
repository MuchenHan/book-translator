# Translation Guide (English → Japanese Academic Text)

## Style
- である調（学術書標準）
- First occurrence of technical terms: 「統語論（syntax）」format
- Italics → 「」, quotes → 「」, book titles → 『』
- Person names → katakana（初出時に原語併記: チョムスキー（Chomsky））
- Preserve footnote numbers, Figure references
- Page markers: `=== p.XX ===` must be preserved

## Parallel Translation Strategy
For chapters > 5,000 words, split into ~3,000-word batches and spawn parallel sub-agents:
- Split at page boundaries (never mid-sentence)
- Each agent gets: source text + terminology table + translation rules
- After all complete: merge, verify page continuity, fill any gaps
- Build final docx with `scripts/build_docx.py`

## Terminology Management
Create a terminology file (one term per line, TSV or `eng → jpn` format):
```
phoneme → 音素
morpheme → 形態素
syntax → 統語論
```
Pass to `build_docx.py --terms-file terminology.txt` for automatic appendix.

## Sub-Agent Prompt Template
```
You are translating [BOOK] from English to Japanese.

RULES:
1. Academic である調
2. Standard terminology: [LIST KEY TERMS]
3. First occurrence: 「日本語（english）」format
4. Italics → 「」, quotes → 「」, book titles → 『』
5. Person names → katakana (romanization on first occurrence)
6. Keep === p.XX === markers, footnote numbers, Figure references
7. Translate EVERYTHING - no summaries or skips

INPUT: Read [FILE_PATH]
OUTPUT: Write to [OUTPUT_PATH]
```
