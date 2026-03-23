# 🤖 AI-Native Notes Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Xueheng-Li/AiNote)

[中文说明](./README.md) | English

This repository is the minimal template used in the article "Build an AI-Native Notes Vault Step by Step." It is meant to be opened as an Obsidian vault and operated through [Claude Code](https://claude.ai/claude-code) or [OpenCode](https://github.com/sst/opencode).

## What It Does

The AI becomes the main entry point. Based on `CLAUDE.md`, it can:

- analyze raw input
- search related folders and `_index.md` files
- decide where the note belongs
- create or update the Markdown file
- keep folder indexes in sync

## Core File

`CLAUDE.md` defines:

- the purpose of the vault
- the note-processing workflow
- folder structure and search rules
- note format, writing style, and safety boundaries

## Quick Start

1. Clone or download this repository.
2. Open it in Obsidian.
3. Edit `1_关于我/个人背景.md` for your own context.
4. Start Claude Code or OpenCode in the vault directory.
5. Ask it to read `CLAUDE.md` first.

For note capture, use the bundled `.claude/skills/takenote` skill instead of maintaining a separate command template.

## Folder Structure

```text
AiNote/
├── CLAUDE.md
├── 1_关于我/
├── 2_想法/
├── 3_工作/
├── 4_学习/
├── 5_会议/
├── 6_研究/
├── 7_行政/
├── 8_附件/
├── 9_代码/
├── 临时工作区/
└── system_config/
```

The Chinese folder names match the article version of the template.

For the minimal runtime setup, `CLAUDE.md` is the only required root-level control file. If you want the built-in note-capture entry point, keep `.claude/skills/takenote/` as well.
