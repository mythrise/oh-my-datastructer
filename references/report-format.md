# 实验报告格式规范

供 `/ds:report` 和 `agents/writer.md` 使用的中文学术报告格式定义。

---

## 字体规范

| 元素 | 中文字体 | 英文/数字字体 | 字号 |
|------|---------|-------------|------|
| 一级标题 | 黑体 (SimHei) | Times New Roman | 三号 (16pt) |
| 二级标题 | 黑体 (SimHei) | Times New Roman | 小三 (15pt) |
| 三级标题 | 黑体 (SimHei) | Times New Roman | 四号 (12pt) |
| 正文 | 宋体 (SimSun) | Times New Roman | 小四 (10.5pt) |
| 表格内容 | 宋体 (SimSun) | Times New Roman | 五号 (10pt) |
| 代码 | 等宽 (Courier New) | Courier New | 五号 (10pt) |
| 页眉/页脚 | 宋体 (SimSun) | Times New Roman | 小五 (9pt) |

### macOS 字体回退
- SimHei → STHeiti / PingFang SC (Semibold)
- SimSun → STSong / Songti SC

## 排版规范

| 元素 | 设置 |
|------|------|
| 行距 | 1.5 倍 |
| 段前/段后 | 标题: 12pt / 6pt; 正文: 0 / 0 |
| 首行缩进 | 正文段落缩进 2 字符 (约 420 twips) |
| 页边距 | 上 2.54cm, 下 2.54cm, 左 3.18cm, 右 3.18cm |
| 纸张 | A4 (210mm × 297mm) |
| 页码 | 底部居中，阿拉伯数字 |

## docx-js 常量

```javascript
const FONT = {
  SONG: "SimSun",
  HEI: "SimHei",
  TNR: "Times New Roman",
  MONO: "Courier New",
};

const SIZE = {  // 单位: half-point
  H1: 32,    // 三号 = 16pt × 2
  H2: 30,    // 小三 = 15pt × 2
  H3: 24,    // 四号 = 12pt × 2
  BODY: 21,  // 小四 = 10.5pt × 2
  TABLE: 20, // 五号 = 10pt × 2
  SMALL: 18, // 小五 = 9pt × 2
};

const SPACING = {
  LINE_15: { line: 360 },       // 1.5 倍行距
  BEFORE_TITLE: { before: 240 }, // 标题前 12pt
  AFTER_TITLE: { after: 120 },   // 标题后 6pt
};

const INDENT = {
  FIRST_2CHAR: { firstLine: 420 }, // 首行缩进 2 字符
};
```

## 报告结构

```
1. 封面
   - 课程名称
   - 作业名称
   - 学号、姓名
   - 日期

2. 目录

3. 算法描述与主要思想
   3.1 问题背景
   3.2 核心算法原理
   3.3 算法流程（伪代码或流程图）

4. 数据结构设计
   4.1 主要数据结构定义
   4.2 关键数据结构选择理由

5. 时空复杂度分析
   5.1 时间复杂度（最好/平均/最坏）
   5.2 空间复杂度
   5.3 与理论下界的比较

6. 实验设计与结果
   6.1 实验环境
   6.2 测试数据说明
   6.3 Baseline 实验结果
   6.4 消融实验结果
   6.5 对比实验结果

7. 图表与可视化
   （内嵌到各章节中）

8. 创新点说明

9. 总结与展望

10. 参考文献（如有）
```

## 图表规范

- 图编号格式：图 X.Y（章节号.序号）
- 表编号格式：表 X.Y
- 图标题在图下方，居中
- 表标题在表上方，居中
- 图表引用使用"如图 X.Y 所示"格式
- 图片分辨率 ≥ 150 DPI
- 图表宽度不超过版心宽度

## matplotlib 中文配置

```python
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["SimHei", "STHeiti", "PingFang SC"]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["figure.dpi"] = 150
matplotlib.rcParams["savefig.dpi"] = 150
```
