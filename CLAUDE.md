# Oh-My-DataStructer (OMD)

数据结构课程大作业通用 harness 系统。从作业题目到提交压缩包的全流程自动化。

## 工作流

```
/ds:init "题目"        → 初始化项目，检测数据结构类型，推荐语言，创建脚手架
/ds:get-information    → 拆解作业为模块，检索基础/进阶/创新方法（Natureflow 风格）
/ds:plan               → 多轮 review 规划（gstack 风格），收集用户创新点
/ds:implement          → 按任务树实现核心算法，可委托 Codex 并行编码
/ds:test               → 单元测试 + baseline/消融/对比实验
/ds:visualize          → Three.js 3D 交互式可视化（Glassmorphism HUD）
/ds:report             → 中文学术格式 Word 实验报告（内嵌图表）
/ds:auto-research      → Karpathy 风格自动迭代优化 + AHP/熵权法指标设计
/ds:package            → 打包提交文件（作业X_学号_姓名.zip）
```

## 项目约定

- 默认语言：Python 3.10+（可指定 C/C++）
- 核心算法：`src/backend/` 或 `src/`
- 前端可视化：`src/frontend/`
- 报告与图表：`reports/`
- 测试数据：`data/`
- 管线状态：`.pipeline/`

## 代码风格

- Python：type hints，中文 docstrings，PEP 8
- JavaScript：docx-js 生成 Word，Three.js 可视化
- 图表：matplotlib + 中文字体（SimHei / PingFang SC）

## 报告格式

- 一号标题：黑体三号（SimHei 16pt）
- 二号标题：黑体小三号（SimHei 15pt）
- 三号标题：宋体小四号（SimSun 12pt）
- 正文：宋体五号（SimSun 10.5pt）
- 数字/字母：Times New Roman
- 行距：1.5 倍（360 twips）
- 首行缩进：2 字符（420 DXA）
- 命名：作业X_学号_姓名.docx

## 关键状态文件

| 文件 | 用途 |
|------|------|
| `.pipeline/memory/project_truth.md` | 单一事实源：作业需求 + 架构蓝图 + 决策 |
| `.pipeline/memory/orchestrator_state.md` | 当前阶段 + 下一步行动 |
| `.pipeline/tasks.json` | 任务队列 |
| `.pipeline/memory/experiment_log.md` | 实验历史 |
| `.pipeline/memory/auto_research_log.md` | 自动研究迭代日志 |
| `reports/benchmarks.json` | 实验数据（自动生成） |
| `src/frontend/data.json` | 可视化数据（自动生成） |

## 依赖

- Python：标准库 + matplotlib + Pillow
- Node.js：docx（Word 生成）
- 核心算法不依赖外部框架

## Agent 协作

- **Architect**：分析 → 拆解 → 方案设计（/ds:init, /ds:get-information, /ds:plan）
- **Implementer**：编码实现（/ds:implement）
- **Experimenter**：测试 + 基准 + 自动研究（/ds:test, /ds:auto-research）
- **Visualizer**：3D 可视化 + 图表（/ds:visualize）
- **Writer**：Word 报告生成（/ds:report, /ds:package）
