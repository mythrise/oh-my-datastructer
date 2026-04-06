#!/usr/bin/env python3
"""OMD 通用指标评估框架：用于 auto-research 循环的评分计算"""
import json
import math
import time
import tracemalloc
from typing import Any, Callable, Dict, List


def measure_time(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """测量函数执行时间（毫秒）"""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms


def measure_memory(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """测量函数峰值内存（KB）"""
    tracemalloc.start()
    result = func(*args, **kwargs)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024


def normalize(value: float, direction: str, all_values: List[float]) -> float:
    """Min-Max 标准化，direction='minimize' 则取反"""
    if not all_values or max(all_values) == min(all_values):
        return 0.5
    v_min, v_max = min(all_values), max(all_values)
    normalized = (value - v_min) / (v_max - v_min)
    return 1.0 - normalized if direction == "minimize" else normalized


def entropy_weight(data_matrix: List[List[float]]) -> List[float]:
    """熵权法计算客观权重"""
    m = len(data_matrix)      # 样本数
    n = len(data_matrix[0])   # 指标数
    if m <= 1:
        return [1.0 / n] * n

    # 标准化
    cols = list(zip(*data_matrix))
    norm_cols = []
    for col in cols:
        c_min, c_max = min(col), max(col)
        rng = c_max - c_min if c_max != c_min else 1.0
        norm_cols.append([(v - c_min) / rng + 1e-10 for v in col])

    # 计算概率矩阵和信息熵
    weights = []
    for col in norm_cols:
        total = sum(col)
        probs = [v / total for v in col]
        entropy = -sum(p * math.log(p) for p in probs if p > 0) / math.log(m)
        weights.append(1.0 - entropy)

    # 归一化
    w_sum = sum(weights)
    return [w / w_sum for w in weights] if w_sum > 0 else [1.0 / n] * n


def composite_score(
    metrics: Dict[str, float],
    indicators: List[Dict],
    reference_data: List[Dict[str, float]],
) -> float:
    """计算综合评分

    Args:
        metrics: 当前指标值 {"metric_name": value}
        indicators: 指标定义 [{"name": str, "direction": str, "weight": float}]
        reference_data: 历史数据用于标准化 [{"metric_name": value}, ...]
    """
    score = 0.0
    for ind in indicators:
        name = ind["name"]
        direction = ind["direction"]
        weight = ind["weight"]
        value = metrics.get(name, 0.0)
        all_vals = [d.get(name, 0.0) for d in reference_data] + [value]
        norm_val = normalize(value, direction, all_vals)
        score += weight * norm_val
    return score


def save_evaluation(results: Dict, output_path: str = "evaluation_result.json"):
    """保存评估结果为 JSON"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 示例用法
    indicators = [
        {"name": "time_ms", "direction": "minimize", "weight": 0.4},
        {"name": "memory_kb", "direction": "minimize", "weight": 0.3},
        {"name": "accuracy", "direction": "maximize", "weight": 0.3},
    ]
    current = {"time_ms": 5.2, "memory_kb": 128, "accuracy": 0.95}
    history = [
        {"time_ms": 8.0, "memory_kb": 256, "accuracy": 0.90},
        {"time_ms": 6.5, "memory_kb": 200, "accuracy": 0.92},
    ]
    score = composite_score(current, indicators, history)
    print(f"Composite score: {score:.4f}")
