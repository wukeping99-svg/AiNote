# 🤖 AI 原生笔记系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Xueheng-Li/AiNote)

中文 | [English](./README_EN.md)

这是文章《手把手搭建 AI 原生笔记库》对应的最小示例仓库。你可以直接把它当成 Obsidian vault 打开，再用 [Claude Code](https://claude.ai/claude-code) 或 [OpenCode](https://github.com/sst/opencode) 作为主入口来记笔记、整理资料和维护索引。

## ✨ 它能做什么

把一段原始输入交给 AI，它会按 `CLAUDE.md` 里的规则：

- 分析这段内容是什么
- 先搜索相关笔记和 `_index.md`
- 决定该放进哪个文件夹
- 创建或更新 Markdown 笔记
- 同步维护文件夹索引

这不是“笔记软件里多了个聊天框”，而是从记录到归档都先经过 AI。

## ⚙️ 核心文件

`CLAUDE.md` 是这套系统的核心。它规定了：

- 这个库是干什么的
- AI 该按什么顺序处理输入
- 目录结构和搜索规则
- 笔记格式、写作要求和安全边界

如果你要把这套模板改成自己的版本，优先改它。

## 🚀 快速开始

1. clone 或下载这个仓库
2. 用 Obsidian 打开这个文件夹
3. 按你的情况改 `1_关于我/个人背景.md`
4. 在这个目录下启动 Claude Code 或 OpenCode
5. 让它先读一遍 `CLAUDE.md`

如果你想在 Claude Code 里用记笔记入口，直接启用仓库自带的 `.claude/skills/takenote` 即可，不需要再维护一份单独的命令模板。

## 📁 目录结构

```text
AiNote/
├── CLAUDE.md
├── README.md
├── README_EN.md
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

说明：

- 这份仓库为了方便说明，额外保留了 `README.md`、`system_config/` 和 `.claude/skills/`
- 你实际搭自己的库时，最简运行版本保留 `CLAUDE.md` 就够了
- 如果你也想直接复用记笔记入口，就连同 `.claude/skills/takenote/` 一起保留
- 每个子文件夹都带一个 `_index.md`，供 AI 先定位再深入读取

## 🧪 如何验证配置

启动 Claude Code 后，直接问：

```text
请读一下 CLAUDE.md，告诉我你理解的规则。
```

再测试一个真实问题，比如：

```text
我之前记过什么关于 AI 原生笔记系统的内容？
```

如果它能先通过 `_index.md` 找到相关笔记，再给出准确摘要，说明配置已经跑通。

## 📖 示例内容

仓库里放了几类最小示例：

- `1_关于我/`：人物背景和当前状态
- `2_想法/`：一条系统理念笔记和一条示例想法
- `3_工作/` 到 `9_代码/`：各类别的示例笔记
- `临时工作区/`：给 AI 放草稿和中间文件

## 📦 需要什么

- [Obsidian](https://obsidian.md/)
- [Claude Code](https://claude.ai/claude-code) 或 [OpenCode](https://github.com/sst/opencode)
- 能读写本地文件的模型接口

## 👨‍💻 作者

[Xueheng Li](https://github.com/Xueheng-Li)
