#!/usr/bin/env python3
"""OMD 通用评估器 — 供 /ds:auto-research 使用

集成 AHP 主观权重 + 熵权法客观权重的综合评分框架。
"""
import json
import math
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ===== 测量工具 =====

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


def measure_all(func: Callable, *args, repetitions: int = 5, **kwargs) -> Dict:
    """综合测量：多次运行取统计值"""
    times = []
    memories = []
    result = None

    for _ in range(repetitions):
        result, t = measure_time(func, *args, **kwargs)
        times.append(t)
        _, m = measure_memory(func, *args, **kwargs)
        memories.append(m)

    return {
        "result": result,
        "time_ms": {"mean": sum(times) / len(times), "min": min(times), "max": max(times), "values": times},
        "memory_kb": {"mean": sum(memories) / len(memories), "peak": max(memories), "values": memories},
        "repetitions": repetitions,
    }


# ===== AHP 层次分析法 =====

def ahp_weights(comparison_matrix: List[List[float]]) -> tuple[List[float], float]:
    """AHP 计算主观权重

    Args:
        comparison_matrix: n×n 判断矩阵（Saaty 1-9 标度）

    Returns:
        (权重向量, 一致性比率 CR)
    """
    n = len(comparison_matrix)

    # 几何平均法求权重
    weights = []
    for row in comparison_matrix:
        product = 1.0
        for val in row:
            product *= val
        weights.append(product ** (1.0 / n))

    w_sum = sum(weights)
    weights = [w / w_sum for w in weights]

    # 一致性检验
    # λ_max
    lambda_max = 0.0
    for i in range(n):
        col_sum = sum(comparison_matrix[j][i] * weights[j] for j in range(n))
        lambda_max += col_sum / weights[i]
    lambda_max /= n

    # CI 和 CR
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri_table = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    ri = ri_table.get(n, 1.49)
    cr = ci / ri if ri > 0 else 0.0

    return weights, cr


# ===== 熵权法 =====

def entropy_weights(data_matrix: List[List[float]]) -> List[float]:
    """熵权法计算客观权重

    Args:
        data_matrix: m×n 矩阵（m 个样本，n 个指标）

    Returns:
        n 维权重向量
    """
    m = len(data_matrix)
    n = len(data_matrix[0])
    if m <= 1:
        return [1.0 / n] * n

    cols = list(zip(*data_matrix))
    norm_cols = []
    for col in cols:
        c_min, c_max = min(col), max(col)
        rng = c_max - c_min if c_max != c_min else 1.0
        norm_cols.append([(v - c_min) / rng + 1e-10 for v in col])

    weights = []
    for col in norm_cols:
        total = sum(col)
        probs = [v / total for v in col]
        entropy = -sum(p * math.log(p) for p in probs if p > 0) / math.log(m)
        weights.append(1.0 - entropy)

    w_sum = sum(weights)
    return [w / w_sum for w in weights] if w_sum > 0 else [1.0 / n] * n


# ===== 综合评分 =====

def composite_weights(
    ahp_w: List[float],
    entropy_w: List[float],
    alpha: float = 0.5
) -> List[float]:
    """组合 AHP + 熵权法权重

    Args:
        ahp_w: AHP 主观权重
        entropy_w: 熵权法客观权重
        alpha: AHP 权重占比（默认 0.5）
    """
    combined = [alpha * a + (1 - alpha) * e for a, e in zip(ahp_w, entropy_w)]
    w_sum = sum(combined)
    return [w / w_sum for w in combined]


def normalize(value: float, direction: str, all_values: List[float]) -> float:
    """Min-Max 标准化，direction='minimize' 则取反"""
    if not all_values or max(all_values) == min(all_values):
        return 0.5
    v_min, v_max = min(all_values), max(all_values)
    normalized = (value - v_min) / (v_max - v_min)
    return 1.0 - normalized if direction == "minimize" else normalized


def compute_score(
    metrics: Dict[str, float],
    indicators: List[Dict],
    weights: List[float],
    reference_data: Optional[List[Dict[str, float]]] = None,
) -> float:
    """计算综合评分

    Args:
        metrics: 当前指标值
        indicators: 指标定义 [{"name": str, "direction": str}]
        weights: 权重向量
        reference_data: 历史数据用于标准化
    """
    ref = reference_data or []
    score = 0.0
    for ind, w in zip(indicators, weights):
        name = ind["name"]
        direction = ind["direction"]
        value = metrics.get(name, 0.0)
        all_vals = [d.get(name, 0.0) for d in ref] + [value]
        norm_val = normalize(value, direction, all_vals)
        score += w * norm_val
    return score


# ===== 评估结果管理 =====

def save_evaluation(results: Dict, output_path: str = "evaluation_result.json"):
    """保存评估结果"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def load_evaluation(path: str) -> Dict:
    """加载评估结果"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # 示例：哈夫曼编码评估
    indicators = [
        {"name": "compression_ratio", "direction": "maximize"},
        {"name": "encoding_time_ms", "direction": "minimize"},
        {"name": "decoding_time_ms", "direction": "minimize"},
        {"name": "memory_peak_kb", "direction": "minimize"},
    ]

    # AHP 判断矩阵（4 个指标）
    ahp_matrix = [
        [1,   3,   3,   2],    # compression_ratio
        [1/3, 1,   1,   1/2],  # encoding_time
        [1/3, 1,   1,   1/2],  # decoding_time
        [1/2, 2,   2,   1],    # memory
    ]
    ahp_w, cr = ahp_weights(ahp_matrix)
    print(f"AHP weights: {[f'{w:.3f}' for w in ahp_w]}, CR={cr:.4f}")

    # 模拟历史数据
    history = [
        {"compression_ratio": 0.45, "encoding_time_ms": 8.0, "decoding_time_ms": 6.0, "memory_peak_kb": 256},
        {"compression_ratio": 0.50, "encoding_time_ms": 6.5, "decoding_time_ms": 5.0, "memory_peak_kb": 200},
    ]

    # 熵权法
    data_matrix = [[d[ind["name"]] for ind in indicators] for d in history]
    ent_w = entropy_weights(data_matrix)
    print(f"Entropy weights: {[f'{w:.3f}' for w in ent_w]}")

    # 综合权重
    final_w = composite_weights(ahp_w, ent_w)
    print(f"Final weights: {[f'{w:.3f}' for w in final_w]}")

    # 评分
    current = {"compression_ratio": 0.55, "encoding_time_ms": 5.2, "decoding_time_ms": 4.0, "memory_peak_kb": 128}
    score = compute_score(current, indicators, final_w, history)
    print(f"Composite score: {score:.4f}")
