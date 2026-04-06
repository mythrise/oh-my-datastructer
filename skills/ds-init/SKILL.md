---
name: ds-init
description: "Initialize a data structures assignment project. Parses the assignment description (Chinese), detects DS topic (huffman/sorting/trees/graphs/hash/linear), recommends implementation language (Python/C/C++), creates project scaffold, initializes .pipeline/ state. Use when: user provides an assignment title like /ds:init '哈夫曼编码与文件压缩'. Triggers: init, initialize, start, new assignment, 初始化, 新作业, 开始"
---

# /ds:init — 项目初始化

从作业题目描述创建完整的数据结构项目。

## 使用方式

```
/ds:init "哈夫曼编码与文件压缩（树与贪心算法）"
/ds:init "排序算法性能比较"
/ds:init --lang cpp "二叉搜索树与AVL树"
```

`$ARGUMENTS` = 作业题目描述文本。可选 `--lang python|c|cpp` 指定语言。

## 执行流程

### Step 1: 解析作业题目

从 `$ARGUMENTS` 中提取：
- **作业名称**（如"哈夫曼编码与文件压缩"）
- **核心知识点**（如"二叉树、哈夫曼树、贪心算法"）
- **任务要求**（如"统计频率、构建树、编码解码、比较压缩率"）

如果用户提供了截图或 docx 文件路径，先读取内容再解析。

### Step 2: 检测数据结构类型

使用关键词映射：

| 关键词 | 类型 | topic_id |
|--------|------|----------|
| 哈夫曼, Huffman, 编码, 压缩, 熵 | 压缩编码 | `huffman` |
| 排序, sort, 冒泡, 快速, 归并, 堆排序, 希尔 | 排序算法 | `sorting` |
| 二叉搜索树, BST, AVL, 红黑树, B树, 平衡树 | 树结构 | `trees` |
| 最短路径, Dijkstra, 最小生成树, Prim, Kruskal, 拓扑, BFS, DFS, 图 | 图算法 | `graphs` |
| 哈希, 散列, hash, 开放地址, 链地址 | 哈希表 | `hash` |
| 栈, 队列, 链表, 双端队列, 跳表 | 线性结构 | `linear` |

如果无法确定，询问用户。

### Step 3: 推荐实现语言

决策树：

```
1. 用户通过 --lang 指定了？ → 使用指定语言
2. 作业文本明确要求某语言？ → 使用该语言
3. 涉及位操作/系统级/内存管理？ → 推荐 C
4. 涉及面向对象/泛型/STL？ → 推荐 C++
5. 侧重算法逻辑/快速原型？ → 推荐 Python（默认）
```

输出推荐时说明理由：
```
[OMD] 推荐语言：Python
[OMD] 理由：作业侧重算法逻辑和数据分析，Python 标准库（heapq, collections）足以支撑，
             且便于快速生成可视化和实验报告。
```

### Step 4: 创建项目脚手架

根据检测到的语言，从插件的 `templates/project-scaffold/{lang}/` 复制文件到当前工作目录。

**Python 项目结构：**
```
{project_name}/
├── src/
│   ├── backend/           # 核心算法
│   │   ├── __init__.py
│   │   └── main.py        # 入口
│   ├── frontend/          # Three.js 可视化（后续 /ds:visualize 填充）
│   └── utils/
│       └── __init__.py
├── tests/
│   └── test_core.py
├── benchmarks/
│   └── run_benchmarks.py
├── reports/
│   └── assets/            # 图表存放
├── data/                  # 测试数据
├── docs/                  # 文档和作业要求
├── .pipeline/             # 管线状态
│   ├── tasks.json
│   └── memory/
│       ├── project_truth.md
│       ├── orchestrator_state.md
│       ├── experiment_log.md
│       ├── auto_research_log.md
│       ├── decision_log.md
│       ├── innovation_points.md
│       └── implementation_registry.md
└── requirements.txt
```

**C/C++ 项目结构：**
```
{project_name}/
├── src/
│   ├── main.c / main.cpp
│   ├── core.h / core.hpp
│   └── ...
├── tests/
├── benchmarks/
├── reports/
├── data/
├── docs/
├── .pipeline/             # 同上
└── Makefile / CMakeLists.txt
```

### Step 5: 初始化管线状态

创建 `.pipeline/memory/project_truth.md`：
```markdown
# 项目真相

## 作业信息
- 名称：{作业名称}
- 类型：{topic_id}
- 语言：{language}
- 创建时间：{timestamp}

## 原始需求
{用户提供的完整作业描述}

## 检测到的知识点
{提取的核心知识点列表}

## 任务要求
{提取的具体任务列表}
```

创建 `.pipeline/memory/orchestrator_state.md`：
```markdown
# 管线状态

## 当前阶段
init → **已完成**

## 下一步
运行 /ds:get-information 进行作业拆解

## 时间线
- {timestamp}: 项目初始化完成
```

创建 `.pipeline/tasks.json`：
```json
{
  "project_id": "{topic_id}-{timestamp}",
  "assignment_name": "{作业名称}",
  "topic": "{topic_id}",
  "language": "{language}",
  "created": "{timestamp}",
  "tasks": [],
  "experiments": []
}
```

### Step 6: 输出总结

```
[OMD] ✅ 项目初始化完成
[OMD] 作业：{作业名称}
[OMD] 类型：{topic_display_name}
[OMD] 语言：{language}
[OMD] 目录：{project_path}
[OMD]
[OMD] 下一步：运行 /ds:get-information 拆解作业模块
```

## 注意事项

- 如果当前目录已存在 `.pipeline/`，警告用户"检测到已有项目，是否覆盖？"
- 如果作业描述是图片，使用 Read 工具读取图片内容
- 作业名称用于后续报告命名，确保提取准确
- 记住用户的学号和姓名（如果提供了），写入 project_truth.md
