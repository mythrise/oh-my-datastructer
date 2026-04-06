#!/usr/bin/env python3
"""OMD 项目初始化脚本：创建 .pipeline/ 目录和初始状态文件"""
import json
import os
import sys
from datetime import datetime, timezone


def init_pipeline(project_dir: str, assignment_name: str, topic: str, language: str):
    """初始化 .pipeline/ 目录结构和状态文件"""
    pipeline = os.path.join(project_dir, ".pipeline")
    memory = os.path.join(pipeline, "memory")
    tasks_dir = os.path.join(pipeline, "tasks")
    checkpoints = os.path.join(pipeline, "checkpoints")

    for d in [pipeline, memory, tasks_dir, checkpoints]:
        os.makedirs(d, exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # tasks.json
    tasks = {
        "project_id": f"{topic}-{now[:10]}",
        "assignment_name": assignment_name,
        "topic": topic,
        "language": language,
        "created": now,
        "tasks": [],
        "experiments": [],
    }
    with open(os.path.join(pipeline, "tasks.json"), "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    # project_truth.md
    with open(os.path.join(memory, "project_truth.md"), "w", encoding="utf-8") as f:
        f.write(f"# 项目真相\n\n")
        f.write(f"## 作业信息\n")
        f.write(f"- 名称：{assignment_name}\n")
        f.write(f"- 类型：{topic}\n")
        f.write(f"- 语言：{language}\n")
        f.write(f"- 创建时间：{now}\n")

    # orchestrator_state.md
    with open(os.path.join(memory, "orchestrator_state.md"), "w", encoding="utf-8") as f:
        f.write(f"# 管线状态\n\n")
        f.write(f"## 当前阶段\ninit -> 已完成\n\n")
        f.write(f"## 下一步\n运行 /ds:get-information 进行作业拆解\n\n")
        f.write(f"## 时间线\n- {now}: 项目初始化完成\n")

    # 空状态文件
    for name in [
        "experiment_log.md",
        "auto_research_log.md",
        "decision_log.md",
        "innovation_points.md",
        "implementation_registry.md",
    ]:
        with open(os.path.join(memory, name), "w", encoding="utf-8") as f:
            f.write(f"# {name.replace('.md', '').replace('_', ' ').title()}\n\n")

    print(f"[OMD] .pipeline/ initialized at {pipeline}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: init_project.py <project_dir> <assignment_name> <topic> [language]")
        sys.exit(1)
    project_dir = sys.argv[1]
    assignment_name = sys.argv[2]
    topic = sys.argv[3]
    language = sys.argv[4] if len(sys.argv) > 4 else "python"
    init_pipeline(project_dir, assignment_name, topic, language)
