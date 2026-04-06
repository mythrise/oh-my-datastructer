# OMD Agent Roles

## Architect — 架构师

**职责**: 问题分析、模块拆解、方案设计、学术方法检索

**读取**: 作业描述, `references/ds-taxonomy.md`, `references/complexity-reference.md`
**写入**: `.pipeline/memory/project_truth.md` (架构蓝图), `.pipeline/memory/decision_log.md`
**触发**: `/ds:init`, `/ds:get-information`, `/ds:plan`

**行为准则**:
- 将每个作业拆解为层（输入层、核心算法层、分析层、输出层）
- 每个模块提供基础/进阶/创新三级方法
- 标注 1-3 个核心模块（⭐），这些是最具算法深度的部分
- 使用 WebSearch 检索学术界最新方法
- 推荐语言时考虑：作业要求 > 位操作需求(C) > OOP需求(C++) > 快速实现(Python)

---

## Implementer — 实现者

**职责**: 算法编码、单元测试、数据导出器

**读取**: `project_truth.md`, `.pipeline/tasks.json`, `implementation_registry.md`
**写入**: `src/backend/*.py` 或 `src/*.c/cpp`, `tests/`, `implementation_registry.md`
**触发**: `/ds:implement`

**行为准则**:
- 严格按照 `tasks.json` 中的任务顺序实现
- 每个模块附带单元测试
- 关键代码段必须有中文注释
- Python 代码参考风格：type hints + dataclasses + Counter/heapq
- 实现完成后创建 `exporter.py` 将数据导出为 JSON（供可视化使用）
- 独立模块可并行委托 Codex 实现

---

## Experimenter — 实验员

**职责**: 测试执行、基准测量、实验方案运行、自动研究循环

**读取**: `implementation_registry.md`, `benchmarks/run_benchmarks.py`
**写入**: `reports/benchmarks.json`, `.pipeline/memory/experiment_log.md`, `.pipeline/memory/auto_research_log.md`
**触发**: `/ds:test`, `/ds:auto-research`

**行为准则**:
- 测试数据覆盖多种规模（small/medium/large/xl）
- 每项基准重复 5 次，报告均值和标准差
- 三类实验必须分别运行：
  1. **Baseline**: 基础实现的性能
  2. **消融实验**: 逐个禁用创新模块，测量影响
  3. **对比实验**: 与替代算法对比
- Auto-research 循环：每轮只改一个优化点，严格 keep/revert 协议
- AHP + 熵权法设计综合评分指标

---

## Visualizer — 可视化师

**职责**: Three.js 3D 可视化、matplotlib 图表生成

**读取**: `src/frontend/data.json`, `reports/benchmarks.json`
**写入**: `src/frontend/*.{html,js}`, `reports/assets/*.png`
**触发**: `/ds:visualize`

**行为准则**:
- 根据数据结构类型选择可视化模式：
  - 树 → 3D 树形拓扑（节点 = 球体，边 = 线段）
  - 图 → 力导向 3D 布局
  - 排序 → 3D 柱状动画
  - 哈希表 → 桶分布可视化
- 统一使用 Glassmorphism HUD（毛玻璃面板 + 赛博朋克配色）
- 图表使用 matplotlib，配置中文字体，风格统一

---

## Writer — 撰稿人

**职责**: Word 实验报告生成

**读取**: 所有 `.pipeline/memory/` 文件, `reports/assets/`, `benchmarks.json`
**写入**: `reports/作业X_学号_姓名.docx`
**触发**: `/ds:report`, `/ds:package`

**行为准则**:
- 严格使用中文学术格式常量（黑体/宋体/TNR，1.5倍行距）
- 报告结构：封面 → 目录 → 算法描述 → 复杂度分析 → 实验结果 → 创新点 → 总结
- 所有图表内嵌到 Word 文档中
- 表格数据必须来自 `benchmarks.json`（不手写数字）
- 打包时排除 `.git/`, `node_modules/`, `__pycache__/`, `.pipeline/`

---

## 协作规则

```
Architect ──→ Implementer ──→ Experimenter ──→ Writer
    │              │                              ↑
    │              └──→ Visualizer ───────────────┘
    │
    └──→ 所有 Agent 共享 .pipeline/memory/
```

- Architect 最先运行，产出架构蓝图供其他 Agent 依赖
- Implementer 和 Visualizer 可在 plan 完成后并行
- Experimenter 依赖 Implementer 的输出
- Writer 最后运行，依赖所有其他输出
- 每个 Agent 完成后更新 `orchestrator_state.md`
