---
name: ds-test
description: "Run tests and experiments. Unit tests, then three experiment types: Baseline (basic implementation performance), Ablation (disable one optimization at a time to measure contribution), Comparison (vs alternative algorithms). Multi-scale test data (small/medium/large/xl), 5 repetitions per benchmark. Generates reports/benchmarks.json. Triggers: test, benchmark, experiment, 测试, 实验, 基准"
---

# /ds:test — 测试与实验

运行完整的测试套件和三类实验（baseline、消融、对比）。

## 前置条件

- 已运行 `/ds:implement`（核心代码已实现）
- `.pipeline/tasks.json` 中有实验任务

## 执行流程

### Step 1: 单元测试

```bash
# Python
pytest tests/ -v --tb=short

# C
make test

# C++
cmake --build build && ctest --output-on-failure
```

所有测试必须通过后才进入实验阶段。如有失败，先修复。

### Step 2: 生成测试数据

根据 DS 类型生成多规模测试数据：

| 规模 | 排序 | 树 | 图 | 哈希 | 压缩 |
|------|------|-----|-----|------|------|
| small | N=1000 | N=100 | V=50,E=200 | N=100 | 1KB |
| medium | N=10000 | N=1000 | V=500,E=5000 | N=1000 | 100KB |
| large | N=100000 | N=10000 | V=5000,E=50000 | N=10000 | 1MB |
| xl | N=1000000 | N=100000 | V=50000,E=500000 | N=100000 | 10MB |

数据分布类型：
- **随机**：均匀随机生成
- **有序**：已排序数据（排序的最好/最坏情况）
- **逆序**：反向排序
- **重复**：大量重复元素
- **偏斜**：极不均匀分布（压缩的最好情况）

### Step 3: Baseline 实验

目标：建立基准性能数据。

```python
# 伪代码
for scale in [small, medium, large, xl]:
    for distribution in [random, sorted, reverse, repeated]:
        data = generate_test_data(scale, distribution)
        results = []
        for trial in range(5):  # 5 次重复
            metrics = run_and_measure(data)
            results.append(metrics)
        record_baseline(scale, distribution, mean(results), std(results))
```

收集的指标（根据 DS 类型选择）：

| DS 类型 | 主要指标 | 辅助指标 |
|---------|---------|---------|
| 压缩编码 | compression_ratio | encoding_efficiency, entropy_gap, encode_time_ms, decode_time_ms |
| 排序 | wall_time_ms | comparisons, swaps, memory_bytes |
| 树 | avg_search_time_ns | tree_height, rotation_count, balance_factor |
| 图 | execution_time_ms | path_cost, memory_bytes, edge_relaxations |
| 哈希表 | avg_probe_count | collision_rate, load_factor, lookup_time_ns |

### Step 4: 消融实验

目标：验证每个创新/优化模块的贡献。

从 `innovation_points.md` 读取创新点列表。对每个创新点：

1. 创建"禁用该创新点"的版本（替换为基础实现）
2. 在相同测试数据上运行
3. 对比 baseline 和禁用版的性能差异

```
消融实验结果：
┌──────────────┬──────────┬──────────┬──────────┐
│ 配置          │ 压缩率    │ 编码效率  │ 编码时间  │
├──────────────┼──────────┼──────────┼──────────┤
│ 完整实现      │ 52.3%    │ 98.6%    │ 3.2ms    │
│ 去除范式编码   │ 55.1%    │ 98.6%    │ 3.1ms    │
│ 去除二进制头部  │ 58.7%    │ 98.6%    │ 3.3ms    │
└──────────────┴──────────┴──────────┴──────────┘
结论：范式编码贡献 2.8% 压缩率提升，二进制头部贡献 6.4%
```

### Step 5: 对比实验

目标：与替代算法/实现进行对比。

从 `decision_log.md` 读取对比对象。实现或引入对比算法（简化版即可），在相同数据集上运行。

```
对比实验结果：
┌──────────────┬──────────┬──────────┬──────────┐
│ 算法          │ 压缩率    │ 编码效率  │ 编码时间  │
├──────────────┼──────────┼──────────┼──────────┤
│ 范式哈夫曼    │ 52.3%    │ 98.6%    │ 3.2ms    │
│ 标准哈夫曼    │ 55.1%    │ 98.6%    │ 3.1ms    │
│ 等长编码      │ 100%     │ 58.2%    │ 0.8ms    │
└──────────────┴──────────┴──────────┴──────────┘
```

### Step 6: 输出实验数据

写入 `reports/benchmarks.json`：

```json
{
  "baseline": {
    "cases": [
      {
        "name": "small_random",
        "scale": "small",
        "distribution": "random",
        "metrics": {
          "compression_ratio": {"mean": 0.523, "std": 0.001},
          "encoding_efficiency": {"mean": 0.986, "std": 0.000},
          "encode_time_ms": {"mean": 3.2, "std": 0.3}
        }
      }
    ]
  },
  "ablation": {
    "full": {"compression_ratio": 0.523},
    "without_canonical": {"compression_ratio": 0.551},
    "without_binary_header": {"compression_ratio": 0.587}
  },
  "comparison": {
    "canonical_huffman": {"compression_ratio": 0.523},
    "standard_huffman": {"compression_ratio": 0.551},
    "fixed_length": {"compression_ratio": 1.0}
  }
}
```

更新 `.pipeline/memory/experiment_log.md`，更新 `orchestrator_state.md` 阶段为 `tested`。

```
[OMD] 实验完成
[OMD] Baseline: {主要指标} = {值}
[OMD] 消融: {N} 个创新点已验证贡献
[OMD] 对比: 优于 {M}/{K} 个替代算法
[OMD] 下一步：/ds:visualize 或 /ds:report
```
