#!/usr/bin/env python3
"""{{PROJECT_NAME}} — 基准测试运行器

运行: python benchmarks/run_benchmarks.py
输出: benchmarks/benchmarks.json
"""
import json
import sys
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

OUTPUT_PATH = Path(__file__).parent / "benchmarks.json"


def measure(func, *args, repetitions=5):
    """测量函数的时间和内存，返回统计数据"""
    times = []
    memories = []

    for _ in range(repetitions):
        # 时间
        start = time.perf_counter()
        result = func(*args)
        elapsed = (time.perf_counter() - start) * 1000  # ms

        # 内存
        tracemalloc.start()
        func(*args)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed)
        memories.append(peak / 1024)  # KB

    return {
        "time_ms": {"mean": sum(times) / len(times), "min": min(times), "max": max(times)},
        "memory_kb": {"mean": sum(memories) / len(memories), "peak": max(memories)},
        "repetitions": repetitions,
    }


def build_test_cases():
    """构建多规模测试数据 — 由 /ds:test 填充"""
    # 示例结构，实际由 /ds:test 根据数据结构类型生成
    return {
        "small": {"description": "小规模数据", "size": 100},
        "medium": {"description": "中等规模数据", "size": 1000},
        "large": {"description": "大规模数据", "size": 10000},
        "xl": {"description": "超大规模数据", "size": 100000},
    }


def run_benchmarks():
    """运行全部基准测试"""
    results = {
        "metadata": {
            "project": "{{PROJECT_NAME}}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "baseline": {},
        "ablation": {},
        "comparison": {},
    }

    test_cases = build_test_cases()

    for name, case in test_cases.items():
        print(f"[OMD] Running baseline: {name} (size={case['size']})...")
        # results["baseline"][name] = measure(algo.run, test_data)

    # 保存结果
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[OMD] Benchmarks saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    run_benchmarks()
