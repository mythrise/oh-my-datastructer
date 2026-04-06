---
name: ds-visualize
description: "Generate Three.js 3D interactive visualization with Glassmorphism HUD. Selects visualization mode by DS type: trees->3D node topology, graphs->force-directed 3D, sorting->3D bar animation, hash->bucket distribution. Creates data exporter, adapts Three.js rendering, adds cyber-punk styled HUD with live metrics. Triggers: visualize, visualization, 3d, 可视化, three.js, frontend"
---

# /ds:visualize — 3D 交互式可视化

为数据结构生成 Three.js 3D 交互式可视化，带 Glassmorphism 风格 HUD。

## 前置条件

- 核心代码已可运行
- `exporter.py` 已创建（`/ds:implement` 阶段）

## 可视化模式选择

根据 DS 类型自动选择可视化模式：

| DS 类型 | 可视化模式 | 节点表示 | 边/连接表示 | 交互方式 |
|---------|-----------|---------|------------|---------|
| 树 | 3D 树形拓扑 | 球体（叶=青色二十面体，内部=灰色球） | 线段（脉冲线） | 点击查看节点详情 |
| 图 | 力导向 3D | 球体（按度数大小） | 管道（按权重粗细） | 高亮路径 |
| 排序 | 3D 柱状阵列 | 长方体（高度=值） | 无 | 逐步动画播放 |
| 哈希表 | 桶分布 | 圆柱体（桶） + 球体（元素） | 链接线（冲突链） | 插入/查找动画 |
| 线性结构 | 序列可视化 | 立方体/球体 | 箭头线（指针） | 操作动画 |

## 执行流程

### Step 1: 运行数据导出

```bash
python3 src/backend/main.py export data/test.txt src/frontend/data.json
```

验证 `data.json` 已生成且非空。

### Step 2: 创建可视化框架

在 `src/frontend/` 中创建：

**index.html** — Glassmorphism HUD：
- 顶部：系统标题栏 + 状态指示灯 + 数据源信息
- 中部 Analysis Strip：6 个指标卡片（输入大小、输出大小、压缩率、信息熵、符号空间、推荐）
- 左侧面板：详细数据监控（总符号数、唯一符号、效率等）
- 右侧面板：位流/数据流分析
- 底部：控制栏（重置视角、自动旋转、交互提示）
- 背景：3D Canvas 容器

**CSS 设计系统：**
```css
:root {
  --cyber-cyan: #00f3ff;
  --cyber-pink: #ff00ff;
  --cyber-blue: #0044ff;
}
.glass {
  background: rgba(0, 10, 20, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 243, 255, 0.15);
}
```

**main.js** — Three.js 3D 引擎：
```javascript
// 核心组件
scene = new THREE.Scene();
camera = new THREE.PerspectiveCamera(60, w/h, 1, 10000);
renderer = new THREE.WebGLRenderer({ antialias: true });
controls = new OrbitControls(camera, renderer.domElement);

// 环境
scene.fog = new THREE.FogExp2(0x000205, 0.0008);
ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
pointLight = new THREE.PointLight(0x00f3ff, 2, 2000);
gridHelper = new THREE.GridHelper(4000, 60);
starField = createStarField(10000);

// 交互
raycaster = new THREE.Raycaster();
// 点击检测 → 显示节点详情
```

### Step 3: 适配 DS 类型

**树可视化（参考现有哈夫曼项目）：**
- 递归布局：根节点在顶部，每层向下偏移 60px，左右子树按 offset 分开
- 叶节点：IcosahedronGeometry，发光青色
- 内部节点：SphereGeometry，深色
- 边：LineBasicMaterial 脉冲线
- 叶标签：Canvas 纹理 → Sprite
- 浮动动画：`sin(time + x * 0.1) * 8`

**图可视化：**
- 力导向布局：Spring-Electrical 模型
- 节点大小按度数缩放
- 边按权重着色（低=青色，高=粉色）
- 路径高亮：选中节点后显示最短路径

**排序可视化：**
- 柱状阵列：BoxGeometry，高度 = 值
- 步进动画：每帧展示一步排序操作
- 比较高亮：正在比较的两个元素变色
- 交换动画：Tween 交换位置

**哈希表可视化：**
- 桶：CylinderGeometry 阵列
- 元素：SphereGeometry 堆叠在桶中
- 冲突链：线段连接溢出元素
- 探测动画：显示探测序列

### Step 4: HUD 数据绑定

从 `data.json` 读取数据后，更新所有 HUD 面板：

```javascript
function renderAnalysis(data) {
  setText('total-symbols', data.metadata.total_symbols);
  setText('unique-symbols', data.metadata.unique_symbols);
  setText('entropy-value', data.metrics.entropy_bits_per_symbol.toFixed(2) + ' bits');
  setText('compression-ratio', formatPercent(data.metrics.compression_ratio));
  // ... 更多指标
}
```

### Step 5: 交互功能

- **点击节点**：显示详情面板（标签、频率、编码、路径）
- **路径高亮**：从被点击节点到根节点的边变亮
- **重置视角**：camera 飞回默认位置
- **自动旋转**：OrbitControls.autoRotate toggle
- **响应式**：window resize 自适应

### Step 6: 生成截图（可选）

如果 Puppeteer 可用，自动截取可视化页面用于报告：
```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('file://' + __dirname + '/src/frontend/index.html');
  await page.waitForTimeout(3000);
  await page.screenshot({path: 'reports/assets/screen_overview.png'});
  await browser.close();
})();
"
```

### Step 7: 更新状态

```
[OMD] 可视化已生成
[OMD] 打开方式：在浏览器中打开 src/frontend/index.html
[OMD] 下一步：/ds:report 生成实验报告
```
