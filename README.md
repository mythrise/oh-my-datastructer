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

## License

MIT
