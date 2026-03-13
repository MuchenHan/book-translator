[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

# Book Translator

スキャンされた学術書籍 PDF を macOS Vision OCR で文字起こしし、AI 翻訳（EN→JA）を経て、クリック可能な目次・セクション見出し・術語対照表を備えたプロフェッショナルな .docx ファイルとして出力するツールである。

## なぜこのツールが必要か？

**対象ユーザー：** 文学、社会科学、人文科学分野の研究者で、英語原著を日常的に読み、分析する必要がある方。

**課題：**

1. 非英語圏の研究者は英語の学術原著を頻繁に参照する必要があるが、スキャンされた PDF は検索不可・コピー不可・引用困難である
2. 絶版・希少な学術書はスキャン品質の低いものしか入手できないことが多い
3. 手作業での文字起こしと翻訳は極めて時間がかかり、研究効率を著しく低下させる
4. 既存の OCR ツールは学術研究に適した出力形式を提供していない

**本ツールの解決策：** macOS ネイティブの Vision OCR（API 費用ゼロ）+ AI 翻訳 + 自動 docx フォーマットにより、スキャン原稿から利用可能な研究文書への変換をワンストップで実現する。

## 機能

- macOS Vision フレームワーク OCR（印刷英文の精度約 95% 以上）
- ページ単位のテキスト抽出、`=== p.XX ===` ページマーカー保持
- Claude Code sub-agents による長章の並列翻訳
- プロフェッショナルな docx 出力：表紙、クリック可能な目次、セクション見出し、ページマーカー
- 術語対照表の自動生成
- フォント、文字サイズ、見出し階層のカスタマイズ
- EN→JA 翻訳対応（他言語ペアへ拡張可能）
- Claude Code skill 統合によるワンコマンド・ワークフロー

## 動作要件

- macOS（Apple Silicon または Intel）— Vision フレームワークに必要
- Python 3.9+
- 依存パッケージ：`pymupdf`, `python-docx`, `pyobjc-framework-Vision`, `pyobjc-framework-Quartz`

## インストール

```bash
git clone https://github.com/MuchenHan/book-translator.git
cd book-translator
pip install -r requirements.txt
```

## 使用方法

### ステップ 1：OCR — PDF からページマーカー付きテキストへ

```bash
python3 scripts/ocr_vision.py input.pdf output_dir --start-page 81 --dpi 150 --lang en
```

- 指定 DPI で画像を抽出し、macOS Vision OCR を実行する
- 出力：`output_dir/all_pages.txt`（ページマーカー付き）
- スキャン品質が低い場合、DPI を 200–300 に上げることを推奨する

### ステップ 2：翻訳

> **注意：** 本プロジェクトには独立した翻訳スクリプトは含まれていない。翻訳は LLM（Claude、GPT 等）を用いて手動で行うか、Claude Code skill による自動化で実行する。

5,000 語を超える章はページ境界で約 3,000 語のバッチに分割する：

```bash
# 例：ページマーカーに対応する行番号で分割
sed -n '1,298p' all_pages.txt > part1.txt
sed -n '299,600p' all_pages.txt > part2.txt
sed -n '601,$p' all_pages.txt > part3.txt
```

各バッチを LLM で翻訳した後、結合する：

```bash
cat ja_part1.txt ja_part2.txt ja_part3.txt > ja_complete.txt
# ページ欠落がないことを確認：
grep -c "=== p\." ja_complete.txt
```

自動並列翻訳を行う場合は、**Claude Code skill**（下記の [Claude Code 統合](#claude-code-統合) を参照）を使用されたい。分割・翻訳・結合を自動的に処理する。

翻訳規範および sub-agent プロンプトテンプレートは [references/translation-guide.md](references/translation-guide.md) を参照されたい。

### ステップ 3：Docx 生成

```bash
python3 scripts/build_docx.py ja_complete.txt output.docx \
  --title "書籍タイトル" \
  --subtitle "原題" \
  --author "著者名" \
  --year "2000" \
  --font "Yu Mincho" \
  --font-size 11 \
  --terms-file terminology.txt \
  --sections "セクション1:1,セクション2:2"
```

生成される `.docx` ファイルには以下が含まれる：

- 表紙ページ（書名、副題、著者、刊行年）
- クリック可能な目次（Word で右クリック → フィールドの更新で生成）
- セクション見出し（原書のページ範囲に対応）
- 術語対照表（`--terms-file` を指定した場合）

## Claude Code 統合

本プロジェクトには Claude Code の skill 定義ファイル（`SKILL.md`）が含まれている。[Claude Code](https://claude.com/claude-code) を使用している場合、skill としてインポートすることでワンコマンドでの全工程実行が可能である。

## 翻訳ガイド

詳細は [references/translation-guide.md](references/translation-guide.md) を参照されたい。以下の内容を含む：

- 学術である調文体（日本語学術標準）
- 術語フォーマット規則
- 長文テキストの並列翻訳戦略

## 活用事例

- 心理学・哲学・社会学の古典的著作の電子化
- 絶版・希少な学術書の個人研究用デジタル化
- 大学院生・研究者のための多言語読解支援

## コントリビューション

Issue や Pull Request の提出を歓迎する。

特に以下の領域への貢献を歓迎する：

- 追加言語ペア（例：EN→ZH、EN→KO）
- 代替 OCR バックエンド（例：Tesseract による Linux 対応）
- 出力形式の拡張（例：EPUB、LaTeX）

## ライセンス

MIT License — [LICENSE](LICENSE) を参照されたい。
