---
name: ds-implement
description: "Implement core algorithm code according to the plan. Reads tasks.json, implements each module in sequence with unit tests. Creates exporter.py for visualization data bridge. Can delegate independent modules to Codex for parallel coding. Supports Python (type hints, Chinese docstrings), C (stdlib, Makefile), C++ (STL, CMake). Triggers: implement, code, build, 实现, 编码, 写代码"
---

# /ds:implement — 核心算法实现

按照规划的任务树，逐模块实现核心算法代码。

## 前置条件

- 已运行 `/ds:plan`（任务树已生成）
- `.pipeline/tasks.json` 中有待实现的任务

## 执行流程

### Step 1: 加载任务队列

读取 `.pipeline/tasks.json`，过滤出 `type: "implement"` 且 `status: "pending"` 的任务。
按 `priority` 排序，按 `dependencies` 确定可并行的任务。

### Step 2: 逐模块实现

对每个实现任务：

1. **读取模块规格**：从 `project_truth.md` 中找到该模块的架构蓝图描述
2. **确定文件位置**：根据模块类型创建对应文件
3. **实现代码**：
   - 遵循选定的实现方案（基础/进阶/创新）
   - 关键代码段添加中文注释
   - 函数签名使用 type hints
4. **编写单元测试**：每个模块至少 3 个测试用例
5. **更新注册表**：写入 `.pipeline/memory/implementation_registry.md`

### Step 3: 语言特定模式

**Python 风格：**
```python
"""模块名称 — 一句话描述"""
from typing import Dict, Optional
from collections import Counter
import heapq

def function_name(param: Type) -> ReturnType:
    """
    功能描述（中文）

    Args:
        param: 参数说明

    Returns:
        返回值说明
    """
    # 算法步骤1：...
    # 算法步骤2：...
    pass
```

**C 风格：**
```c
/**
 * 功能描述
 * @param param 参数说明
 * @return 返回值说明
 */
int function_name(Type* param) {
    // 算法步骤1
    // 算法步骤2
    return result;
}
```

**C++ 风格：**
```cpp
/**
 * 功能描述
 * @tparam T 类型参数
 * @param param 参数说明
 */
template<typename T>
auto function_name(const T& param) -> ReturnType {
    // 算法步骤1
    // 算法步骤2
}
```

### Step 4: 创建数据导出器

实现 `exporter.py`（或对应语言的导出模块），将算法内部数据导出为 JSON，供 Three.js 可视化使用。

导出数据结构（以哈夫曼为例）：
```json
{
  "metadata": {"source_name": "test.txt", "source_type": "text", "total_symbols": 1000},
  "metrics": {"entropy_bits_per_symbol": 4.12, "avg_code_length": 4.18, "compression_ratio": 0.523},
  "frequencies": {"65": 100, "66": 50},
  "codes": {"65": "00", "66": "010"},
  "tree": {"name": "Internal", "freq": 1000, "children": [...]},
  "symbols": [{"label": "A", "freq": 100, "code": "00", "bit_length": 2}]
}
```

每种 DS 类型需要适配不同的导出 schema：
- **树**：节点层级结构 + 属性（freq/balance/color）
- **图**：节点列表 + 边列表 + 权重 + 路径
- **排序**：每步状态快照 + 比较/交换记录
- **哈希表**：桶状态 + 冲突链 + 探测序列

### Step 5: Codex 并行委托

如果多个模块互不依赖（dependencies 无交集），可以：
```
[OMD] 检测到 2 个可并行模块：encoder, decoder
[OMD] 建议委托 Codex 并行实现？（Y/n）
```

委托时，为 Codex 提供：
- 模块规格（从 project_truth.md 摘取）
- 依赖模块的接口定义
- 目标文件路径
- 代码风格要求

### Step 6: 质量检查

每个模块完成后运行：
1. **单元测试**：`pytest tests/test_{module}.py -v`
2. **基础运行**：确认 `main.py` 的命令可正常执行
3. **导出验证**：确认 `exporter.py` 输出有效 JSON

### Step 7: 更新状态

更新 `.pipeline/tasks.json` 中完成任务的 `status: "done"`。
更新 `.pipeline/memory/implementation_registry.md`：

```markdown
| 模块 | 文件 | 函数 | 状态 | 测试 |
|------|------|------|------|------|
| 频率统计 | src/backend/frequency.py | count_frequencies() | done | test_frequency.py |
| 树构建 | src/backend/tree.py | build_huffman_tree() | done | test_tree.py |
```

更新 `orchestrator_state.md` 阶段为 `implementing` 或 `implemented`。
