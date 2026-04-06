---
name: ds-report
description: "Generate Chinese academic format Word experiment report using docx-js. Fonts: SimHei(黑体) headings, SimSun(宋体) body, Times New Roman numbers/letters. 1.5x line spacing, 2-char first-line indent. Sections: cover page, TOC, algorithm description, complexity analysis, experiments (baseline+ablation+comparison with embedded charts), innovation points, conclusion. Triggers: report, 报告, word, docx, 实验报告"
---

# /ds:report — 实验报告生成

生成符合中文学术格式的 Word 实验报告，内嵌图表。

## 前置条件

- 已运行 `/ds:test`（`reports/benchmarks.json` 已生成）
- 核心代码已完成

## 格式规范常量

```javascript
// 字体
const SONG = "SimSun";          // 宋体 — 正文
const HEI  = "SimHei";          // 黑体 — 标题
const TNR  = "Times New Roman"; // 数字和字母

// 字号（单位：half-point）
const SZ_H1   = 32; // 一号标题：三号 = 16pt
const SZ_H2   = 30; // 二号标题：小三号 = 15pt
const SZ_H3   = 24; // 三号标题：小四号 = 12pt
const SZ_BODY = 21; // 正文：五号 = 10.5pt

// 行距
const SPACING_15 = { line: 360, lineRule: "auto" }; // 1.5 倍行距

// 首行缩进（10.5pt × 2 字符 × 20 = 420 DXA）
const INDENT_2CHAR = { firstLine: 420 };

// A4 页面边距（DXA）
const PAGE_MARGIN = { top: 1440, right: 1800, bottom: 1440, left: 1800 };

// 表格边框
const BORDER_THIN = { style: "single", size: 4, color: "2C5F8A" };
```

## 执行流程

### Step 1: 生成图表

运行 `gen_chart.py` 生成 matplotlib 图表到 `reports/assets/`：

必须生成的图表（根据 DS 类型适配）：
1. **fig1_frequency.png** — 频率/分布柱状图
2. **fig2_codelength.png** / **fig2_performance.png** — 核心指标散点图
3. **fig3_distribution.png** — 分布图（码长分布/数据分布）
4. **fig4_benchmark.png** — 基准性能对比（熵 vs 码长 / 时间对比）
5. **fig5_comparison.png** — 算法对比柱状图
6. **fig6_complexity.png** — 复杂度增长趋势图

matplotlib 配置：
```python
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC", "Heiti SC", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
```

### Step 2: 生成 Word 文档

使用 Node.js `docx` 库生成报告。报告结构：

#### 封面页
```
数据结构课程设计
实  验  报  告

题目：{作业名称}
姓名：{学生姓名}
学号：{学号}
日期：{日期}
```
字体：黑体，居中，大号。

#### 目录
使用 `TableOfContents` 组件，自动从标题生成。

#### 一、问题描述与分析
- 作业原始要求
- 核心知识点
- 问题分析

数据来源：`project_truth.md` → 原始需求

#### 二、算法设计
- 整体架构（文字描述 + 架构图）
- 核心算法思想
- 关键数据结构定义
- 伪代码或流程图

数据来源：`project_truth.md` → 架构蓝图

#### 三、核心代码实现
- 关键函数的代码片段（等宽字体，9pt）
- 代码解释

数据来源：`implementation_registry.md` → 核心代码文件

#### 四、时空复杂度分析
- 理论分析（表格形式）
- 各操作的复杂度推导

格式：
```
| 操作 | 时间复杂度 | 空间复杂度 | 说明 |
|------|-----------|-----------|------|
```

#### 五、实验结果与分析

**5.1 Baseline 实验**
- 表格：不同规模下的性能数据
- 图表：fig4_benchmark.png
- 分析文字

**5.2 消融实验**
- 表格：每个优化模块的贡献
- 分析：哪个创新点贡献最大

**5.3 对比实验**
- 表格：与替代算法的对比
- 图表：fig5_comparison.png
- 分析：为什么当前方案更优/更适合

数据来源：`reports/benchmarks.json`

#### 六、创新点说明
- 列出每个创新点
- 说明原理和效果
- 引用消融实验数据证明贡献

数据来源：`innovation_points.md` + `benchmarks.json`

#### 七、可视化展示
- 可视化截图（如果有）
- 功能说明

#### 八、总结与体会
- 项目完成情况
- 学到了什么
- 可以改进的方向

### Step 3: 内嵌图表

```javascript
// 读取 PNG 图片并嵌入
function embedChart(name, widthPx, heightPx) {
  return new ImageRun({
    type: "png",
    data: fs.readFileSync(path.join(ASSETS_DIR, name)),
    transformation: { width: widthPx, height: heightPx }
  });
}

// 图注（居中，不缩进）
function figCaption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({
      text, font: { eastAsia: SONG, ascii: TNR }, size: 18, bold: true
    })],
    spacing: { before: 60, after: 120 },
    indent: { firstLine: 0 }
  });
}
```

### Step 4: 输出

写入 `reports/作业X_学号_姓名.docx`。

如果学号和姓名未提供，询问用户或使用占位符。

```
[OMD] 实验报告已生成
[OMD] 文件：reports/作业二_学号_姓名.docx
[OMD] 包含：封面 + 目录 + 8 个章节 + 6 张图表
[OMD] 下一步：/ds:package 打包提交
```

### 注意事项

- 所有数字数据必须来自 `benchmarks.json`，不得手写
- 表格数据自动从 JSON 生成，确保一致性
- 如果某些图表不适用于当前 DS 类型，跳过或替换
- macOS 上可能没有 SimSun/SimHei，使用 PingFang SC / Heiti SC 作为备选
