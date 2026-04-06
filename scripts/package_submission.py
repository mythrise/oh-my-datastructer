#!/usr/bin/env python3
"""OMD 打包脚本：将作业项目打包为课程要求的提交格式"""
import os
import shutil
import sys
import zipfile
from pathlib import Path

EXCLUDE_PATTERNS = {
    ".git", "node_modules", "__pycache__", ".pipeline", ".tmp",
    ".DS_Store", ".env", "package-lock.json", ".pyc",
}


def should_exclude(path: str) -> bool:
    parts = Path(path).parts
    return any(p in EXCLUDE_PATTERNS or p.endswith(".pyc") for p in parts)


def package(project_dir: str, assignment_num: str, student_id: str, student_name: str):
    project = Path(project_dir)
    folder_name = f"数据结构课设计作业{assignment_num}_{student_id}_{student_name}"
    output_dir = project.parent / folder_name
    zip_path = project.parent / f"{folder_name}.zip"

    # 清理旧输出
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # 创建提交目录
    source_code = output_dir / "source_code"
    document = output_dir / "document"
    source_code.mkdir(parents=True)
    document.mkdir(parents=True)

    # 复制源代码
    for item in ["src", "tests", "benchmarks", "data", "requirements.txt"]:
        src = project / item
        if src.exists():
            dst = source_code / item
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                    "*.pyc", "__pycache__", ".DS_Store", "node_modules"
                ))
            else:
                shutil.copy2(src, dst)

    # 复制报告
    reports = project / "reports"
    if reports.exists():
        for f in reports.glob("*.docx"):
            shutil.copy2(f, document / f.name)
        # 也复制报告生成脚本
        scripts_dst = source_code / "reports"
        scripts_dst.mkdir(exist_ok=True)
        for f in reports.iterdir():
            if f.suffix in (".py", ".js") and not should_exclude(str(f)):
                shutil.copy2(f, scripts_dst / f.name)

    # 创建 zip
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(output_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_PATTERNS]
            for file in files:
                filepath = Path(root) / file
                if not should_exclude(str(filepath)):
                    arcname = filepath.relative_to(output_dir.parent)
                    zf.write(filepath, arcname)

    # 清理临时目录
    shutil.rmtree(output_dir)

    size_kb = zip_path.stat().st_size / 1024
    print(f"[OMD] Packaged: {zip_path.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: package_submission.py <project_dir> <assignment_num> <student_id> <student_name>")
        sys.exit(1)
    package(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
