"""可视化数据导出器

将核心算法的中间状态和结果导出为 JSON，供 Three.js 前端读取。
由 /ds:implement 根据具体数据结构填充 export_snapshot()。
"""
import json
from pathlib import Path


def export_snapshot(data: dict) -> dict:
    """将算法状态转换为可视化快照

    Args:
        data: 算法运行时状态数据

    Returns:
        符合前端约定的 JSON 结构
    """
    raise NotImplementedError("请根据具体数据结构实现 export_snapshot()")


def export_visualization_data(input_path: str, output_path: str):
    """完整的可视化数据导出流程"""
    # 1. 加载输入数据
    # 2. 运行算法获取中间状态
    # 3. 调用 export_snapshot() 转换
    # 4. 写入 JSON
    raise NotImplementedError("请先运行 /ds:implement 实现导出逻辑")


def save_json(data: dict, path: str):
    """保存 JSON 文件"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OMD] Exported: {path}")
