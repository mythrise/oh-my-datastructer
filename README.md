# Oh-My-DataStructer (OMD)

> Data structures course assignment harness for Claude Code. From assignment description to submission package.

## What is this?

OMD is a Claude Code plugin that provides a complete workflow for data structures course assignments. Give it your assignment description, and it will guide you through analysis, planning, implementation, testing, visualization, report generation, and submission packaging.

## Features

- **Auto-scaffolding**: Detects DS topic, recommends language, creates project structure
- **Architecture Blueprint**: Decomposes problems into modules with basic/advanced/innovative methods (Natureflow-style)
- **Multi-round Planning**: gstack-style review rounds with interactive decision points
- **3D Visualization**: Three.js interactive visualization with Glassmorphism HUD
- **Chinese Academic Report**: Word document with correct formatting (SimHei/SimSun/TNR, 1.5x spacing)
- **Auto-Research**: Karpathy-style iterative optimization with AHP/entropy-weight metric design
- **Submission Packaging**: Correct naming convention, zip with all deliverables

## Installation

```bash
# Claude Code marketplace
claude plugin install mythrise/oh-my-datastructer

# Manual
git clone https://github.com/mythrise/oh-my-datastructer.git ~/.claude/plugins/oh-my-datastructer
```

## Quick Start

```
/ds:init "哈夫曼编码与文件压缩"
/ds:get-information
/ds:plan
/ds:implement
/ds:test
/ds:visualize
/ds:report
/ds:package
```

## Supported Assignment Types

| Type | Examples | Default Language |
|------|---------|-----------------|
| Compression/Encoding | Huffman, LZ77, arithmetic coding | Python |
| Sorting | Quicksort, mergesort, heapsort comparison | Python / C++ |
| Trees | BST, AVL, Red-Black, B-tree | Python / C++ |
| Graphs | Dijkstra, Prim, Kruskal, topological sort | Python |
| Hash Tables | Open addressing, chaining, perfect hashing | Python / C |
| Linear Structures | Stack, queue, linked list applications | C / Python |

## Commands

| Command | Description |
|---------|-------------|
| `/ds:init "题目"` | Initialize project from assignment description |
| `/ds:get-information` | Decompose into modules, survey academic methods |
| `/ds:plan` | Multi-round interactive planning |
| `/ds:implement` | Implement core algorithm code |
| `/ds:test` | Run tests + baseline/ablation/comparison experiments |
| `/ds:visualize` | Generate Three.js 3D visualization |
| `/ds:report` | Generate Word experiment report |
| `/ds:auto-research` | Iterative optimization loop |
| `/ds:package` | Package for submission |

## Codex 适配

OMD 原生支持 Claude Code 的 Codex 模式。在实现阶段，独立模块可并行委托 Codex 完成，大幅提升开发速度。

### 使用方式

**方式一：在 `/ds:implement` 中自动委托**

`/ds:implement` 会自动识别可并行的独立模块，将其委托给 Codex 执行。无需额外配置。

**方式二：手动委托特定模块给 Codex**

```
# 在 Claude Code 中使用 Codex 实现单个模块
/ds:implement --codex "core/encoder.py"

# 或直接在对话中指定
请使用 Codex 实现 src/core/encoder.py 中的编码器模块
```

**方式三：Codex CLI 独立使用**

```bash
# 将 OMD 作为 Codex 的上下文
codex --context .claude/plugins/oh-my-datastructer "实现 AVL 树的左旋和右旋操作"
```

### Codex 最佳实践

- **适合委托**: 核心算法实现、测试用例生成、基准测试脚本、数据导出器
- **不适合委托**: 多轮规划讨论（/ds:plan）、创新点设计、报告撰写
- **并行策略**: 当任务树中存在 ≥2 个无依赖模块时，自动触发 Codex 并行实现
- **质量门禁**: Codex 产出自动经过单元测试验证，测试不通过则回退重试

### 与 Claude Code Agent 协作

```
┌─────────────────────────────────────────────┐
│  Claude Code (主控)                          │
│  ├─ /ds:plan        → 交互式规划             │
│  ├─ /ds:implement   → 分析依赖图             │
│  │   ├─ Codex #1    → 模块 A (并行)          │
│  │   ├─ Codex #2    → 模块 B (并行)          │
│  │   └─ Claude      → 模块 C (有依赖，串行)   │
│  ├─ /ds:test        → 集成验证               │
│  └─ /ds:report      → 报告生成               │
└─────────────────────────────────────────────┘
```

## License

MIT
