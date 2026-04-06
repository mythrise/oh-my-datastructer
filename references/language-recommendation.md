# 语言推荐决策树

供 `/ds:init` 使用的语言自动推荐规则。

---

## 决策流程

```
作业是否明确指定语言？
├─ 是 → 使用指定语言
└─ 否 → 继续判断
     │
     作业是否涉及以下特征？
     ├─ 位操作 / 内存管理 / 系统级编程
     │  ├─ 是否要求面向对象？
     │  │  ├─ 是 → C++
     │  │  └─ 否 → C
     │  └─ 示例：文件压缩底层、内存池、OS 相关
     │
     ├─ 面向对象 / 泛型编程 / STL 使用
     │  → C++
     │  └─ 示例：容器设计、模板元编程、重载运算符
     │
     ├─ 算法逻辑为主 / 快速实现 / 数据分析
     │  → Python
     │  └─ 示例：图算法分析、排序比较、编码算法
     │
     └─ 无特殊要求
        → Python（默认）
```

## 语言特性对比

| 特性 | Python | C | C++ |
|------|--------|---|-----|
| 开发速度 | ★★★★★ | ★★ | ★★★ |
| 运行性能 | ★★ | ★★★★★ | ★★★★★ |
| 内存控制 | ★★ | ★★★★★ | ★★★★★ |
| 数据可视化 | ★★★★★ | ★ | ★★ |
| 库生态 | ★★★★★ | ★★★ | ★★★★ |
| 调试便捷 | ★★★★★ | ★★★ | ★★★ |
| 适合教学 | ★★★★★ | ★★★ | ★★★★ |

## 各语言脚手架说明

### Python
- 入口：`src/main.py`
- 测试：`pytest` + `tests/test_core.py`
- 基准：`benchmarks/run_benchmarks.py`
- 依赖：`requirements.txt`
- 可视化数据导出：`src/exporter.py` → JSON

### C
- 入口：`src/main.c`
- 头文件：`src/core.h`
- 测试：`tests/test_core.c`（assert 宏）
- 构建：`Makefile`
- 可视化数据导出：`src/exporter.c` → JSON（手动拼接或 cJSON）

### C++
- 入口：`src/main.cpp`
- 头文件：`src/core.hpp`
- 测试：`tests/test_core.cpp`
- 构建：`CMakeLists.txt`
- 可视化数据导出：`src/exporter.cpp` → JSON（nlohmann/json）

## 推荐话术模板

```
根据作业要求分析：
- 作业类型：{type}
- 关键特征：{features}
- 推荐语言：{language}
- 推荐理由：{reason}

如果你有其他偏好，可以指定使用 Python / C / C++。
```
