---
name: ds-package
description: "Package the assignment for submission. Creates zip with correct Chinese naming convention (数据结构课设计作业X_学号_姓名.zip). Validates all deliverables exist (source code, Word report, test data). Excludes .git, node_modules, __pycache__, .pipeline, .tmp. Triggers: package, submit, zip, 打包, 提交, 交作业"
---

# /ds:package — 打包提交

将作业打包为符合课程要求的提交格式。

## 执行流程

### Step 1: 收集提交信息

如果 `project_truth.md` 中没有学号和姓名，询问用户：
```
[OMD] 请提供以下信息用于打包：
  - 作业编号（如"二"）：
  - 学号：
  - 姓名：
```

### Step 2: 验证交付物

检查所有必要文件是否存在：

```
[OMD] 交付物检查：
  ✅ 源代码：src/backend/ (5 个文件)
  ✅ 实验报告：reports/作业二_学号_姓名.docx
  ✅ 测试数据：data/ (3 个文件)
  ✅ 实验数据：reports/benchmarks.json
  ⚠️ 可视化：src/frontend/ (可选)
  ⚠️ 图表：reports/assets/ (6 张图表)
```

如果缺少必要文件，提示用户先运行对应的 skill。

### Step 3: 创建提交目录结构

按照课程要求的格式组织文件：

```
数据结构课设计作业{N}_{学号}_{姓名}/
├── source_code/              # 源代码
│   ├── src/
│   │   ├── backend/          # 核心算法
│   │   └── frontend/         # 可视化（如果有）
│   ├── tests/                # 测试代码
│   ├── benchmarks/           # 基准测试
│   ├── reports/              # 报告生成脚本
│   │   ├── gen_chart.py
│   │   └── generate_report.js
│   ├── data/                 # 测试数据
│   └── requirements.txt      # 依赖（如果有）
│
└── document/                 # 文档
    └── 作业{N}_{学号}_{姓名}.docx  # 实验报告
```

### Step 4: 排除文件

以下文件/目录不应包含在提交中：
- `.git/`
- `node_modules/`
- `__pycache__/`
- `*.pyc`
- `.pipeline/`
- `.tmp/`
- `.DS_Store`
- `.env`
- `package-lock.json`

### Step 5: 创建压缩文件

```bash
cd ..
zip -r "数据结构课设计作业{N}_{学号}_{姓名}.zip" \
  "数据结构课设计作业{N}_{学号}_{姓名}/" \
  -x "*.git*" "*node_modules*" "*__pycache__*" "*.pyc" \
     "*/.pipeline/*" "*/.tmp/*" "*/.DS_Store"
```

### Step 6: 验证压缩包

```
[OMD] ✅ 打包完成
[OMD] 文件：数据结构课设计作业二_20230001_张三.zip
[OMD] 大小：{size} KB
[OMD] 包含：
  - source_code/: {N} 个文件
  - document/: 实验报告 ({pages} 页)
[OMD]
[OMD] 提交前请确认：
  1. 报告格式是否符合要求（字体、行距）
  2. 代码关键部分是否有注释
  3. 测试数据是否包含
```

### 注意事项

- 如果是 C/C++ 项目，确认编译产物（.o, .exe, a.out）已排除
- 报告文件名必须与压缩包命名规则一致
- 如果文件过大（>50MB），提醒用户检查是否包含了不必要的大文件
