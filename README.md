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

如果你想让 Claude Code 或 OpenCode 直接帮你完成整套初始化，最简单的方式就是先把下面这段提示词发给它：

```text
请帮我初始化这套 AI 原生笔记库。

1. 如果当前目录里还没有 AiNote，就执行：
   git clone https://github.com/Xueheng-Li/AiNote.git

2. 进入 AiNote 目录，先阅读 README.md 和 CLAUDE.md，理解这套笔记库的工作方式。

3. 检查目录结构是否完整，至少包括：
   - .claude
   - .claude/skills
   - .claude/skills/takenote
   - 1_关于我
   - 2_想法
   - 3_工作
   - 4_学习
   - 5_会议
   - 6_研究
   - 7_行政
   - 8_附件
   - 9_代码
   - 临时工作区
   - system_config

4. 帮我完成第一轮个性化配置，重点检查和引导我补全这些文件：
   - 1_关于我/个人背景.md
   - 1_关于我/当前状态.md
   - CLAUDE.md
   - system_config/memory.md
   - system_config/templates.md

5. 务必保留 .claude/skills/takenote/，这是这套仓库默认的记笔记入口。

6. 完成后告诉我：
   - 你修改了哪些文件
   - 还需要我补充哪些信息
   - 请明确提醒我更新 1_关于我/个人背景.md 和 1_关于我/当前状态.md
   - 教我接下来怎样用 /takenote 或“记一下”来记第一条笔记
```

这套仓库默认依赖 `.claude/skills/takenote/` 作为记笔记入口，使用时务必保留这个目录，不要删掉。

初始化完成后，你可以这样开始记录想法：

```text
/takenote 我刚想到一个点子：如果把 AI 原生笔记系统和课程学习结合，可能可以做成个性化学习中心。
```

或者直接用自然语言：

```text
记一下：我发现很多笔记系统的问题不是记不下来，而是后续不会再被调用。
```

Claude Code 会根据 `takenote` 的规则自动判断内容类型、选择目录、生成标题，并同步更新对应的 `_index.md`。

你可以直接参考这条现成示例笔记：[AI 原生笔记系统作为个性化学习中心](./2_%E6%83%B3%E6%B3%95/AI%E5%8E%9F%E7%94%9F%E7%AC%94%E8%AE%B0%E7%B3%BB%E7%BB%9F%E4%BD%9C%E4%B8%BA%E4%B8%AA%E6%80%A7%E5%8C%96%E5%AD%A6%E4%B9%A0%E4%B8%AD%E5%BF%83.md)。

如果你想手动操作，也可以按这个顺序开始：

1. 先把仓库拉到本地
2. 用 Obsidian 打开这个文件夹
3. 在这个目录下启动 Claude Code 或 OpenCode
4. 让它先读一遍 `CLAUDE.md`
5. 更新 `1_关于我/个人背景.md` 和 `1_关于我/当前状态.md`

```bash
git clone https://github.com/Xueheng-Li/AiNote.git
```
## 📁 目录结构

```text
AiNote/
├── .claude/
│   └── skills/
│       └── takenote/
│           └── SKILL.md
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

- `.claude/skills/takenote/` 是这套仓库的默认必需组件，不要删掉
- `README.md`、`system_config/` 和 `.claude/skills/` 都属于这套模板的组成部分
- 你实际搭自己的库时，`CLAUDE.md` 和 `.claude/skills/takenote/` 都应保留
- `.claude/skills/takenote/` 是默认必需组件，用来接收 `/takenote`、`记一下`、`帮我整理成笔记` 这类输入
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
