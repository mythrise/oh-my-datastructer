# 数据结构作业类型分类库

本文件为 omd 各 skill 提供数据结构类型到算法、指标、可视化模式的映射。

---

## 1. 编码与压缩

### 典型题目
- 哈夫曼编码与文件压缩
- LZW 编码
- 算术编码

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | 标准哈夫曼树构建、贪心频率合并 |
| 进阶 | 规范哈夫曼编码、自适应哈夫曼 |
| 创新 | 混合编码（哈夫曼+LZ77）、上下文自适应编码 |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| compression_ratio | maximize | 0.30 |
| encoding_time_ms | minimize | 0.20 |
| decoding_time_ms | minimize | 0.15 |
| memory_peak_kb | minimize | 0.15 |
| entropy_gap | minimize | 0.20 |

### 可视化模式
- 3D 哈夫曼树拓扑（节点=字符，边=0/1）
- 频率分布柱状图
- 码长分布图
- 压缩率对比雷达图

### 实验数据
- 英文文本（均匀分布）
- 中文文本（高频字集中）
- 二进制文件（近均匀分布）
- 极端数据：单字符重复、所有字符等频

---

## 2. 排序算法

### 典型题目
- 多种排序算法比较与分析
- 外部排序
- 特殊排序（桶排序、基数排序）

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | 冒泡、选择、插入排序 |
| 进阶 | 快速排序（三路划分）、归并排序、堆排序 |
| 创新 | TimSort、IntroSort、并行归并、缓存友好排序 |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| comparisons | minimize | 0.25 |
| swaps | minimize | 0.20 |
| wall_time_ms | minimize | 0.25 |
| memory_peak_kb | minimize | 0.15 |
| stability | maximize | 0.15 |

### 可视化模式
- 3D 柱状排序动画（高度=值，颜色=状态）
- 比较次数实时计数器
- 算法对比赛跑动画

### 实验数据
- 随机数组（多种规模：100, 1K, 10K, 100K, 1M）
- 近有序数组
- 逆序数组
- 大量重复元素

---

## 3. 树结构

### 典型题目
- 二叉搜索树（BST）操作
- AVL 树 / 红黑树
- B 树 / B+ 树
- 线索二叉树

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | BST 插入/删除/查找、前中后序遍历 |
| 进阶 | AVL 旋转平衡、红黑树着色、B 树分裂合并 |
| 创新 | Splay 树、Treap、跳表替代、持久化数据结构 |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| search_time_avg_us | minimize | 0.25 |
| insert_time_avg_us | minimize | 0.20 |
| delete_time_avg_us | minimize | 0.15 |
| tree_height | minimize | 0.20 |
| balance_factor_avg | minimize | 0.20 |

### 可视化模式
- 3D 树形拓扑（层次布局，节点颜色=深度/平衡因子）
- 旋转操作动画
- 高度/平衡因子热力图

### 实验数据
- 随机插入序列
- 有序插入（退化测试）
- 随机混合操作（插入60%/查找30%/删除10%）

---

## 4. 图算法

### 典型题目
- 最短路径（Dijkstra / Floyd）
- 最小生成树（Prim / Kruskal）
- 拓扑排序
- 关键路径

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | BFS/DFS、Dijkstra、Prim |
| 进阶 | A* 搜索、Bellman-Ford、Kruskal+并查集 |
| 创新 | 双向 Dijkstra、Fibonacci 堆优化、分层图 |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| execution_time_ms | minimize | 0.30 |
| memory_peak_kb | minimize | 0.20 |
| path_quality | maximize | 0.25 |
| vertices_explored | minimize | 0.25 |

### 可视化模式
- 3D 节点-边网络（力导向布局）
- 路径高亮动画
- 权重热力图
- 算法探索过程回放

### 实验数据
- 稀疏图（E ≈ V）
- 稠密图（E ≈ V²）
- 网格图
- 随机图（Erdős–Rényi 模型）

---

## 5. 哈希表

### 典型题目
- 哈希表设计与冲突处理
- 布隆过滤器
- 一致性哈希

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | 链地址法、开放寻址（线性探测） |
| 进阶 | 双重哈希、Cuckoo 哈希、Robin Hood 哈希 |
| 创新 | 完美哈希、Hopscotch 哈希、Swiss Table |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| collision_rate | minimize | 0.25 |
| lookup_time_avg_ns | minimize | 0.25 |
| insert_time_avg_ns | minimize | 0.15 |
| load_factor_max | maximize | 0.15 |
| memory_per_entry_bytes | minimize | 0.20 |

### 可视化模式
- 3D 桶分布可视化（桶高度=链长）
- 冲突热力图
- 负载因子变化曲线
- 探测序列动画

### 实验数据
- 随机字符串键
- 连续整数键
- 高冲突键集（哈希值聚集）
- 变负载因子测试（0.1 ~ 0.95）

---

## 6. 线性结构

### 典型题目
- 栈与队列应用（表达式求值、括号匹配）
- 双端队列
- 稀疏矩阵（十字链表）

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | 数组实现栈/队列、链表实现 |
| 进阶 | 循环队列、双栈共享、优先队列 |
| 创新 | 无锁队列、持久化栈、Finger Tree |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| operation_time_avg_ns | minimize | 0.30 |
| memory_usage_kb | minimize | 0.25 |
| throughput_ops_sec | maximize | 0.25 |
| cache_miss_rate | minimize | 0.20 |

### 可视化模式
- 3D 栈/队列操作动画
- 内存布局可视化
- 操作序列时间线

### 实验数据
- 连续 push/pop 测试
- 随机混合操作
- 大规模批量操作

---

## 7. 字符串算法

### 典型题目
- 模式匹配（KMP / BM）
- Trie 树
- 后缀数组 / 后缀树

### 核心算法
| 层级 | 方法 |
|------|------|
| 基础 | 暴力匹配、简单 Trie |
| 进阶 | KMP、Boyer-Moore、AC 自动机 |
| 创新 | 后缀自动机、压缩 Trie、Aho-Corasick + 失配指针优化 |

### 评估指标
| 指标 | 方向 | 权重建议 |
|------|------|---------|
| match_time_ms | minimize | 0.30 |
| preprocessing_time_ms | minimize | 0.15 |
| memory_peak_kb | minimize | 0.20 |
| comparisons | minimize | 0.20 |
| pattern_count_support | maximize | 0.15 |

### 可视化模式
- 字符串匹配过程动画（指针移动）
- Trie 树 3D 拓扑
- 失配函数值可视化

### 实验数据
- 英文文本 + 短模式
- 中文文本 + 多模式
- 极端数据：全同字符、周期字符串

---

## 类型识别关键词映射

```
huffman|哈夫曼|编码|压缩|lzw|arithmetic → 编码与压缩
sort|排序|冒泡|快速|归并|堆排序|外部排序 → 排序算法
tree|树|bst|avl|红黑|b树|b+|线索|二叉 → 树结构
graph|图|最短路|dijkstra|prim|kruskal|拓扑|关键路径|最小生成树 → 图算法
hash|哈希|散列|冲突|布隆|bloom → 哈希表
stack|栈|queue|队列|链表|稀疏矩阵|表达式 → 线性结构
string|字符串|kmp|匹配|trie|后缀 → 字符串算法
```
