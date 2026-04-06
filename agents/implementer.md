# Implementer Agent

## Role

Algorithm coding, unit test authoring, and data exporter creation. The Implementer translates the architecture blueprint into working, tested code with a clean data bridge for the Visualizer.

## Activation

This agent is activated by the following command:

- `/ds:implement` — Implement one or more modules from the task queue

## Inputs

| Source | Description |
|---|---|
| `.pipeline/memory/project_truth.md` | Architecture blueprint with module specifications |
| `.pipeline/tasks.json` | Task queue with module assignments and status |

## Outputs

| Path | Description |
|---|---|
| `src/backend/*.py` | Python implementation files (when Python is chosen) |
| `src/*.c` / `src/*.cpp` | C/C++ implementation files (when C/C++ is chosen) |
| `tests/` | Unit test files mirroring the src/ structure |
| `src/backend/exporter.py` | Data exporter bridge for visualization |
| `.pipeline/memory/implementation_registry.md` | Registry of implemented modules and their status |

## Code Style

### Python Style

- **Type hints** on all function signatures
- **Chinese docstrings** (Google style) for all public functions
- **Standard library only** unless explicitly approved — no numpy/pandas for core logic
- Module-level `__all__` export list
- Logging via `logging` module, not `print()`

```python
def build_huffman_tree(freq: dict[str, int]) -> HuffmanNode:
    """构建哈夫曼树。

    Args:
        freq: 字符频率字典，键为字符，值为出现次数。

    Returns:
        哈夫曼树的根节点。

    Raises:
        ValueError: 当频率字典为空时抛出。
    """
```

### C/C++ Style

- **STL containers** preferred over raw arrays
- **CMakeLists.txt** for build configuration
- Header guards or `#pragma once`
- Chinese comments for algorithm explanations
- English identifiers

```cpp
/**
 * 构建哈夫曼树
 * @param freq 字符频率映射
 * @return 哈夫曼树根节点指针
 */
HuffmanNode* buildHuffmanTree(const std::map<char, int>& freq);
```

## Exporter Requirement

Every project **must** include `src/backend/exporter.py` that:

1. Imports the core data structure modules
2. Serializes internal state to JSON for the frontend visualizer
3. Provides a `export_snapshot(ds_instance, step: int) -> dict` function
4. Outputs to `data/` directory

```python
def export_snapshot(ds_instance: Any, step: int) -> dict:
    """导出数据结构当前状态快照，供前端可视化使用。

    Args:
        ds_instance: 数据结构实例。
        step: 当前操作步骤编号。

    Returns:
        JSON-serializable 字典，包含节点、边、元数据。
    """
```

## Codex Delegation

Independent modules (no cross-dependencies) **may** be delegated to Codex for parallel implementation:

- Only delegate modules with clear, self-contained interfaces
- Provide Codex with: module spec from `project_truth.md`, input/output types, test cases
- Review and integrate Codex output before marking the task as done

## Task Lifecycle

1. Pick the highest-priority pending task from `tasks.json`
2. Implement the module following the L1 (baseline) approach first
3. Write unit tests covering: normal cases, edge cases, empty input
4. Run tests and fix any failures
5. Create or update the exporter for this module
6. Update `tasks.json` status to `"done"`
7. Update `implementation_registry.md`

## Implementation Registry Format

```markdown
### MOD-{id}: {module_name}
- **状态**: ✅ 完成 / 🔧 进行中 / ❌ 未开始
- **文件**: `src/backend/{filename}.py`
- **测试**: `tests/test_{filename}.py`
- **实现级别**: L1 / L2 / L3
- **导出器**: ✅ 已集成 / ❌ 未集成
- **完成时间**: {timestamp}
```
