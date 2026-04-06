# 可视化模式库

供 `/ds:visualize` 和 `agents/visualizer.md` 使用的 Three.js 可视化模式参考。

---

## 设计系统

### 配色方案
```
主色（cyber-cyan）: #00f3ff
辅色（neon-purple）: #a855f7
强调色（neon-pink）: #ff006e
背景色: #0a0a0f
面板背景: rgba(255, 255, 255, 0.05)
文字色: #e0e0e0
成功色: #00ff88
警告色: #ffaa00
错误色: #ff4444
```

### 字体
- HUD 文字：`"JetBrains Mono", "Fira Code", monospace`
- 标题：`"Inter", sans-serif`

### Glassmorphism 面板
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
```

---

## 数据结构 → 可视化模式映射

### 1. 树形结构（Tree Mode）
**适用**: 哈夫曼树、BST、AVL、红黑树、B 树、Trie

**布局算法**: 层次布局（Reingold-Tilford 变体）
- X: 同层节点等距分布
- Y: 层深度 × 层间距
- Z: 可用于表达额外维度（如平衡因子）

**节点表现**:
- 球体几何体，半径按权重缩放
- 颜色映射：深度梯度 / 平衡因子 / 红黑色
- 悬浮标签：键值、频率、高度等

**边表现**:
- 圆柱体或线段连接父子节点
- 颜色可表示 0/1（哈夫曼）或左/右

**交互**:
- 点击节点：展开详情面板
- 悬浮高亮：该节点的子树
- 滚轮：缩放

### 2. 图网络（Graph Mode）
**适用**: 最短路径、MST、拓扑排序、网络流

**布局算法**: 力导向布局（Force-Directed）
- 斥力：节点间库仑力
- 引力：边弹簧力
- 阻尼：逐步收敛

**节点表现**:
- 球体，大小按度数缩放
- 颜色：未访问=灰、已访问=cyan、当前=pink、最短路=green

**边表现**:
- 线段，宽度按权重缩放
- 有向图：箭头指示方向
- 高亮路径：发光效果

**交互**:
- 点击起点/终点：触发算法演示
- 拖拽节点：手动调整布局
- 播放/暂停：算法步进

### 3. 排序动画（Sort Mode）
**适用**: 各类排序算法对比

**布局**: 一维柱状排列
- X: 数组索引位置
- Y: 元素值（柱高度）
- Z: 可用于多算法并排对比

**柱状表现**:
- Box 几何体，高度=值
- 颜色状态：未处理=灰、比较中=yellow、交换中=pink、已排序=green

**动画**:
- 比较：两柱高亮
- 交换：柱体位移动画（lerp）
- 完成：从左到右逐个变绿

**HUD 数据**:
- 比较次数实时计数
- 交换次数实时计数
- 当前算法名称
- 进度条

### 4. 哈希分布（Hash Mode）
**适用**: 哈希表、布隆过滤器

**布局**: 圆形桶排列
- 桶沿圆周分布
- 链表/探测序列向外延伸

**桶表现**:
- 圆柱体，高度=链长
- 颜色：空桶=暗灰、正常=cyan、过长=red

**交互**:
- 输入键：演示哈希计算 + 插入过程
- 滑块调节负载因子
- 切换哈希函数

### 5. 字符串匹配（String Mode）
**适用**: KMP、BM、AC 自动机

**布局**: 双行文字排列
- 上行：文本（Text）
- 下行：模式（Pattern），可滑动对齐

**表现**:
- 每个字符一个方块
- 匹配=green、失配=red、比较中=yellow、跳过=grey
- 失配函数/坏字符表：侧边面板

**动画**:
- 模式滑动
- 指针移动
- 失配跳转高亮

---

## Three.js 公共配置

```javascript
// 场景设置
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.FogExp2(0x0a0a0f, 0.002);

// 相机
const camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 1000);

// 渲染器
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = THREE.ACESFilmicToneMapping;

// 控制器
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// 光照
const ambient = new THREE.AmbientLight(0xffffff, 0.4);
const point = new THREE.PointLight(0x00f3ff, 1, 100);
```

## HUD 面板标准布局

```
┌─────────────────────────────────────────┐
│ [左上] 项目信息面板                       │
│   - 作业名称                              │
│   - 数据结构类型                          │
│   - 当前算法                              │
│                                           │
│              [中央] 3D 场景                │
│                                           │
│ [左下] 控制面板          [右上] 统计面板   │
│   - 播放/暂停             - 关键指标      │
│   - 速度滑块              - 实时计数      │
│   - 重置                  - 复杂度显示    │
│                                           │
│                          [右下] 详情面板   │
│                            - 选中节点信息  │
│                            - 算法步骤说明  │
└─────────────────────────────────────────┘
```
