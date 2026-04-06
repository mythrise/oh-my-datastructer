#!/usr/bin/env python3
"""{{PROJECT_NAME}} — 主入口

Usage:
    python src/main.py [command] [options]
"""
import argparse
import sys
from pathlib import Path

# 确保 src 在搜索路径中
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import algo  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="{{PROJECT_DESCRIPTION}}")
    sub = parser.add_subparsers(dest="command")

    # 示例子命令 — 按实际需求替换
    run_p = sub.add_parser("run", help="运行核心算法")
    run_p.add_argument("input", help="输入文件路径")
    run_p.add_argument("-o", "--output", default="output.txt", help="输出路径")

    analyze_p = sub.add_parser("analyze", help="分析结果")
    analyze_p.add_argument("input", help="输入文件路径")

    export_p = sub.add_parser("export", help="导出可视化数据")
    export_p.add_argument("input", help="输入文件路径")
    export_p.add_argument("-o", "--output", default="viz_data.json", help="JSON 输出路径")

    args = parser.parse_args()

    if args.command == "run":
        algo.run(args.input, args.output)
    elif args.command == "analyze":
        algo.analyze(args.input)
    elif args.command == "export":
        from utils.exporter import export_visualization_data
        export_visualization_data(args.input, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
