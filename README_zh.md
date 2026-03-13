[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md)

# Book Translator

扫描学术书籍 PDF → OCR 识别 → AI 翻译 → 排版输出 docx

## 为什么需要这个工具？

**目标用户**：文学系、社会科学、人文学科的研究者，日常需要阅读英文原著并进行分析。

**痛点**：

1. 非英语国家的研究者经常需要阅读英文学术原著，但扫描版 PDF 无法搜索、无法复制文本、难以引用
2. 经典/绝版学术著作往往只有质量较差的扫描件可用
3. 手动转录和翻译极其耗时，严重影响研究效率
4. 现有 OCR 工具无法产出适合学术研究的输出格式

**解决方案**：macOS 原生 Vision OCR（零 API 费用）+ AI 翻译 + 自动化 docx 排版，一站式完成从扫描件到可用研究文档的转换。

## 功能特性

- macOS Vision 框架 OCR（印刷英文准确率约 95%+）
- 逐页文本提取，保留 `=== p.XX ===` 页码标记
- 支持通过 Claude Code sub-agents 并行翻译长章节
- 专业 docx 输出：封面、可点击目次、章节标题、页码标记
- 术语对照表自动生成
- 可配置字体、字号、标题层级
- 支持 EN→JA 翻译（可扩展至其他语言对）
- Claude Code skill 集成，一键完成全流程

## 环境要求

- macOS（Apple Silicon 或 Intel）— Vision 框架必需
- Python 3.9+
- 依赖包：`pymupdf`、`python-docx`、`pyobjc-framework-Vision`、`pyobjc-framework-Quartz`

## 安装

```bash
git clone https://github.com/MuchenHan/book-translator.git
cd book-translator
pip install -r requirements.txt
```

## 使用方法

### 第 1 步：OCR — PDF 转页标记文本

```bash
python3 scripts/ocr_vision.py input.pdf output_dir --start-page 81 --dpi 150 --lang en
```

- 按指定 DPI 提取图像，调用 macOS Vision OCR
- 输出：`output_dir/all_pages.txt`，含页码标记
- 扫描质量差时，将 DPI 提高到 200–300

### 第 2 步：翻译

超过 5,000 词的章节，按页码边界拆分为约 3,000 词的批次，并行翻译。

### 第 3 步：生成 Docx

```bash
python3 scripts/build_docx.py ja_complete.txt output.docx \
  --title "书名" \
  --subtitle "原书名" \
  --author "作者" \
  --year "1957" \
  --font "Yu Mincho" \
  --font-size 11 \
  --terms-file terminology.txt \
  --sections "章节1:1,章节2:2"
```

## Claude Code 集成

本项目包含 Claude Code skill 定义文件（`SKILL.md`）。如果你使用 [Claude Code](https://claude.com/claude-code)，可以将其导入为 skill，实现一键完成全流程。

## 翻译规范

详见 [references/translation-guide.md](references/translation-guide.md)，包括：

- 学术である調文体（日语学术标准）
- 术语格式规范
- 长文本并行翻译策略

## 使用场景

- 心理学/哲学/社会学经典著作电子化（如 Skinner 的《Verbal Behavior》）
- 绝版/稀缺学术书籍的个人研究数字化
- 研究生和研究者的跨语言阅读辅助

## 贡献

欢迎提交 issue 和 pull request！

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
