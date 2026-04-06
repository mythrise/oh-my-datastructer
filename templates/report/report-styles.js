/**
 * OMD 报告格式常量 — 供 generate_report.js 使用
 *
 * 中文学术报告标准格式：黑体标题 / 宋体正文 / TNR 数字 / 1.5 倍行距
 */

// 字体
const FONT = {
  SONG: "SimSun",       // 宋体 — 正文
  HEI: "SimHei",        // 黑体 — 标题
  TNR: "Times New Roman", // 英文/数字
  MONO: "Courier New",  // 代码
};

// macOS 回退字体
const FONT_FALLBACK = {
  SONG: ["SimSun", "STSong", "Songti SC"],
  HEI: ["SimHei", "STHeiti", "PingFang SC"],
};

// 字号 (half-point)
const SIZE = {
  H1: 32,    // 三号 = 16pt
  H2: 30,    // 小三 = 15pt
  H3: 24,    // 四号 = 12pt
  BODY: 21,  // 小四 = 10.5pt
  TABLE: 20, // 五号 = 10pt
  SMALL: 18, // 小五 = 9pt
  CODE: 20,  // 五号 = 10pt
};

// 间距 (twips)
const SPACING = {
  LINE_15: { line: 360 },         // 1.5 倍行距
  LINE_SINGLE: { line: 240 },     // 单倍行距
  BEFORE_H1: { before: 360 },     // 标题前 18pt
  AFTER_H1: { after: 240 },       // 标题后 12pt
  BEFORE_H2: { before: 240 },     // 二级标题前 12pt
  AFTER_H2: { after: 120 },       // 二级标题后 6pt
  BEFORE_H3: { before: 200 },
  AFTER_H3: { after: 100 },
};

// 缩进
const INDENT = {
  FIRST_2CHAR: { firstLine: 420 }, // 首行缩进 2 字符
};

// 页面设置 (twips, 1cm ≈ 567 twips)
const PAGE = {
  WIDTH: 11906,   // A4 宽 = 210mm
  HEIGHT: 16838,  // A4 高 = 297mm
  MARGIN_TOP: 1440,    // 2.54cm
  MARGIN_BOTTOM: 1440,
  MARGIN_LEFT: 1800,   // 3.18cm
  MARGIN_RIGHT: 1800,
};

// 表格样式
const TABLE_STYLE = {
  BORDER_COLOR: "000000",
  BORDER_SIZE: 1,
  HEADER_SHADING: "D9E2F3",    // 表头浅蓝背景
  ALT_ROW_SHADING: "F2F2F2",  // 交替行灰背景
};

module.exports = {
  FONT, FONT_FALLBACK, SIZE, SPACING, INDENT, PAGE, TABLE_STYLE,
};
