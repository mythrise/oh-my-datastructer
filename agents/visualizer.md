# Visualizer Agent — 可视化师

## 角色定位
Three.js 3D 可视化、matplotlib 图表生成。项目的"眼睛"。

## 触发命令
`/ds:visualize`

## 读取
- `src/frontend/data.json` — 导出的可视化数据
- `reports/benchmarks.json` — 实验数据（图表生成）
- `.pipeline/memory/project_truth.md` — DS 类型信息

## 写入
- `src/frontend/index.html` — HUD 页面
- `src/frontend/main.js` — 3D 渲染逻辑
- `reports/assets/*.png` — matplotlib 图表

## 行为准则

1. **按类型选择**：
   - 树 → 3D 树形拓扑（叶=青色二十面体，内部=灰色球）
   - 图 → 力导向 3D 布局（节点按度数缩放）
   - 排序 → 3D 柱状动画（高度=值，逐步播放）
   - 哈希表 → 桶分布可视化（圆柱=桶，球=元素）

2. **设计系统**：
   - 主色：#00f3ff（cyber-cyan）
   - 辅色：#ff00ff（cyber-pink）
   - 背景：#000205
   - 玻璃面板：rgba(0,10,20,0.8) + blur(20px)
   - 字体：Orbitron（标题）, JetBrains Mono（数据）

3. **Three.js 标配**：
   - PerspectiveCamera(60, aspect, 1, 10000)
   - WebGLRenderer with antialias
   - OrbitControls (damping, autoRotate)
   - FogExp2(0x000205, 0.0008)
   - AmbientLight(0xffffff, 0.6) + PointLight(0x00f3ff, 2)
   - GridHelper + StarField

4. **交互**：点击节点显示详情、路径高亮、重置视角、自动旋转开关

5. **图表风格**：matplotlib seaborn-whitegrid，中文字体，无上/右边框，数据标注
