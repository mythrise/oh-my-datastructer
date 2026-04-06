---
name: ds-auto-research
description: "Karpathy autoresearch-style iterative optimization with AHP/entropy-weight composite metric design. Phase A: WebSearch for evaluation dimensions + AHP hierarchy + entropy weight -> composite scoring formula. Phase B: Baseline measurement. Phase C: N iterations of analyze->stash->modify->evaluate->keep/revert. Phase D: Summary report with success/failure analysis and radar chart. Each iteration modifies ONE optimization point. Triggers: auto-research, optimize, iterate, 自动研究, 优化, 迭代, autoresearch"
---

# /ds:auto-research — 自动迭代优化

参考 Karpathy autoresearch 的设计，结合 AHP/熵权法进行指标设计，自动化迭代优化算法性能。

## 使用方式

```
/ds:auto-research                           # 默认 10 轮
/ds:auto-research --iterations 20           # 指定轮次
/ds:auto-research --target src/backend/encoder.py  # 指定目标文件
/ds:auto-research --metric compression_ratio       # 指定单一指标
```

## 前置条件

- 核心代码已实现且可运行
- baseline 实验数据存在（或在 Phase B 中自动生成）

## 执行流程

### Phase A: 指标设计

#### A1. 收集评估维度

使用 WebSearch 检索：
- "数据结构 {topic} 性能评估指标"
- "{algorithm} benchmark metrics"
- "{ds_type} evaluation criteria"

#### A2. AHP 层次分析法建立指标体系

```
目标层：算法综合性能评分
    │
    ├── 准则层 C1：时间效率（权重 w1）
    │   ├── 指标 I1：编码/运行时间 (ms)
    │   └── 指标 I2：解码/查询时间 (ms)
    │
    ├── 准则层 C2：空间效率（权重 w2）
    │   ├── 指标 I3：内存峰值 (KB)
    │   └── 指标 I4：输出大小/压缩率
    │
    ├── 准则层 C3：算法质量（权重 w3）
    │   ├── 指标 I5：编码效率（信息熵接近度）
    │   └── 指标 I6：操作计数（比较/交换/旋转次数）
    │
    └── 准则层 C4：鲁棒性（权重 w4）
        ├── 指标 I7：最坏情况 vs 平均情况比值
        └── 指标 I8：不同数据分布的方差
```

AHP 判断矩阵（示例，哈夫曼编码）：
```
        C1    C2    C3    C4
C1 [   1     1/2    2     3  ]   时间效率
C2 [   2      1     3     4  ]   空间效率（压缩最重要）
C3 [  1/2    1/3    1     2  ]   算法质量
C4 [  1/3    1/4   1/2    1  ]   鲁棒性
```

计算特征向量 → AHP 主观权重 `w_ahp = [w1, w2, w3, w4]`
一致性检验：CR < 0.1

#### A3. 熵权法确定客观权重

从 baseline 运行中收集多组数据（不同规模、不同分布）：

```python
# 数据矩阵 X (m 个样本 × n 个指标)
# 1. 标准化
X_norm = (X - X.min()) / (X.max() - X.min())

# 2. 计算概率矩阵
P = X_norm / X_norm.sum(axis=0)

# 3. 计算信息熵
E = -1/ln(m) * sum(P * ln(P))

# 4. 计算权重
d = 1 - E  # 差异系数
w_entropy = d / d.sum()  # 熵权法客观权重
```

#### A4. 综合权重与评分公式

```python
# 组合权重（AHP 主观 + 熵权法客观）
alpha = 0.5  # 主观-客观权衡系数
w_final = alpha * w_ahp + (1 - alpha) * w_entropy
w_final = w_final / w_final.sum()  # 归一化

# 综合评分（越高越好）
# 对于"越小越好"的指标取倒数或负值
score = sum(w_final[i] * normalize(metric[i]) for i in range(n))
```

输出：`evaluation_metrics.json`
```json
{
  "indicators": [
    {"name": "encode_time_ms", "direction": "minimize", "weight": 0.15},
    {"name": "compression_ratio", "direction": "minimize", "weight": 0.35},
    {"name": "encoding_efficiency", "direction": "maximize", "weight": 0.25},
    {"name": "decode_time_ms", "direction": "minimize", "weight": 0.10},
    {"name": "memory_peak_kb", "direction": "minimize", "weight": 0.15}
  ],
  "ahp_weights": [0.15, 0.35, 0.25, 0.10, 0.15],
  "entropy_weights": [0.18, 0.30, 0.22, 0.12, 0.18],
  "final_weights": [0.165, 0.325, 0.235, 0.110, 0.165],
  "ahp_cr": 0.042,
  "formula": "score = 0.165*norm(1/t_enc) + 0.325*norm(1/ratio) + 0.235*norm(eff) + 0.110*norm(1/t_dec) + 0.165*norm(1/mem)"
}
```

### Phase B: Baseline 建立

1. 运行当前实现，收集所有指标数据
2. 在多种测试数据上运行（至少 3 种规模 × 2 种分布）
3. 计算 baseline 综合评分

```
[OMD] Baseline 综合评分: 0.7234
[OMD] 各指标:
  - 编码时间: 3.2ms (权重 16.5%)
  - 压缩率: 52.3% (权重 32.5%)
  - 编码效率: 98.6% (权重 23.5%)
  - 解码时间: 4.1ms (权重 11.0%)
  - 内存峰值: 256KB (权重 16.5%)
```

### Phase C: 迭代循环

```
FOR round = 1 to N:

  1. 分析当前代码 + 过往失败记录
     → 识别性能瓶颈
     → 提出一个具体优化方向

  2. git stash push -m "auto-research-round-{round}"

  3. 修改核心算法文件（仅一个优化点）
     优化策略优先级：
     a. 算法级：更换数据结构或算法（如 list→heap）
     b. 微优化：减小常数因子（如避免 dict 查找热循环）
     c. 内存布局：改善缓存行为
     d. 语言特性：用内置 C 实现替代纯 Python
     e. 剪枝：跳过不必要的工作（短路、早停）

  4. 运行评估 → 计算新综合评分

  5. 判断：
     IF new_score > best_score:
       → KEEP（保留修改）
       → best_score = new_score
       → 记录：修改内容 + 算法原理 + 提升幅度 + 各指标变化
       → git stash drop
     ELSE:
       → REVERT（回滚）
       → git stash pop
       → 记录：尝试方向 + 失败原因

  6. 写入 auto_research_log.md
```

### Phase D: 总结报告

生成迭代总结到 `.pipeline/memory/auto_research_log.md`：

```markdown
# 自动研究日志

## 配置
- 目标文件：src/backend/encoder.py
- 综合评分公式：{formula}
- Baseline 评分：0.7234
- 迭代轮次：20

## 迭代记录

| # | 操作 | 描述 | 评分变化 | 各指标变化 | 结果 |
|---|------|------|---------|-----------|------|
| 1 | 算法级 | 用数组索引替代字典查找 | 0.7234→0.7234 | 时间-12%, 其他不变 | REVERT(综合分不变) |
| 2 | 微优化 | 批量位写入(8bit一次) | 0.7234→0.7401 | 时间-28%, 其他不变 | KEEP |
| 3 | 剪枝 | 跳过单符号输入的树构建 | 0.7401→0.7401 | 无变化 | REVERT |

## 最终结果
- 最终评分：0.7401（提升 2.31%）
- 成功优化 1 项：批量位写入（原理：减少系统调用次数）
- 失败尝试 2 项

## 成功优化详解
### 优化 #2：批量位写入
- **修改**：将逐位写入改为 8 位一次写入
- **原理**：减少 file.write() 系统调用次数，批量 I/O 效率更高
- **效果**：编码时间从 3.2ms 降至 2.3ms（-28%），综合分 +2.31%
```

终端输出：
```
[OMD] 自动研究完成（20 轮）
[OMD] Baseline → Final: 0.7234 → 0.7401 (+2.31%)
[OMD] 成功优化: 1 项 | 失败尝试: 2 项
[OMD] 详细日志: .pipeline/memory/auto_research_log.md
```
