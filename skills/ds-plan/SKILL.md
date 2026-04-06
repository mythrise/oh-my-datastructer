---
name: ds-plan
description: "Multi-round interactive planning with gstack-style review rounds. Round 1: Office Hours (6 forcing questions on requirements). Round 2: Algorithm Review (Architect perspective, ASCII diagrams, method selection). Round 3: Innovation Review (user's creative ideas, feasibility assessment). Round 4: Experiment Review (baseline/ablation/comparison design, metric selection). Produces tasks.json and decision_log.md. Triggers: plan, planning, 规划, 讨论, 方案, review"
---

# /ds:plan — 多轮规划讨论

参考 gstack 的多角色 review 机制，通过 4 轮结构化讨论与用户共同确定实现方案。

## 前置条件

- 已运行 `/ds:init`（项目已初始化）
- 已运行 `/ds:get-information`（架构蓝图已生成）

## 执行流程

### Round 1: Office Hours（需求澄清）

像产品经理一样拷问需求。向用户提出 6 个强制问题：

1. **核心功能边界**："作业要求的必做项有哪些？哪些是加分项？"
2. **输入输出规格**："输入数据的格式和规模？期望的输出是什么？"
3. **评分标准**："老师最看重什么？代码正确性？创新性？报告质量？"
4. **时间约束**："截止日期是什么时候？你能投入多少时间？"
5. **已有知识**："你对这个数据结构的理解到什么程度？有没有已经写好的部分？"
6. **特殊要求**："有没有必须用的语言、库、框架？报告模板有固定格式吗？"

**等待用户回答每个问题。** 根据回答调整后续规划的深度和范围。

输出：需求设计文档（追加到 `project_truth.md`）

### Round 2: 算法 Review（Architect 视角）

对架构蓝图中的每个模块，呈现方案选择：

```
┌─────────────────────────────────────────────────────┐
│ 模块：哈夫曼树构建                                    │
├─────────────────────────────────────────────────────┤
│ [A] 基础方案：标准哈夫曼（优先队列）                   │
│     复杂度：O(n log n)                               │
│     优点：简单、教科书标准                             │
│     缺点：解码端需要完整的树结构                       │
│                                                     │
│ [B] 进阶方案：范式哈夫曼（Canonical Huffman）          │
│     复杂度：O(n log n) 构建 + O(M) 编码表重建         │
│     优点：只需存码长表，头部更紧凑                      │
│     缺点：实现稍复杂                                  │
│                                                     │
│ [C] 创新方案：自适应哈夫曼 + 范式混合                  │
│     复杂度：O(n log n) 摊销                           │
│     优点：无需预扫描，可流式处理                       │
│     缺点：实现复杂度高，可能超出课程要求                │
└─────────────────────────────────────────────────────┘
你选择哪个方案？（A/B/C/自定义）
```

用 ASCII 图展示整体数据流：

```
输入文件 → [频率统计] → [树构建] → [编码生成] → [文件编码] → 压缩文件
                                                              ↓
压缩文件 → [头部解析] → [编码表重建] → [位流解码] → 还原文件
```

对每个模块，等待用户选择方案。记录到 `decision_log.md`。

### Round 3: 创新 Review（用户参与）

主动询问用户的创新想法：

```
现在是创新环节。你有没有自己想尝试的创新点？

常见创新方向（供参考）：
1. 算法层面：改进核心算法的效率或适用范围
2. 工程层面：添加可视化、并行化、流式处理等
3. 应用层面：支持更多数据类型、自适应策略等
4. 分析层面：更深入的理论分析、与其他算法的比较

请描述你的想法，我来评估可行性。
```

对用户提出的每个创新点，评估：
- **可行性**（1-5分）：技术上能否实现
- **工作量**（低/中/高）：大约需要多少额外代码
- **加分潜力**（1-5分）：对评分的帮助程度
- **建议**：保留 / 修改后保留 / 建议替换为...

交互式决策：用户确认每个创新点的去留。写入 `innovation_points.md`。

### Round 4: 实验 Review（Experimenter 视角）

设计三类实验方案：

**Baseline 实验：**
- 用最基础的实现方式，测量基准性能
- 确定使用的测试数据集（规模、类型）
- 确定核心指标

**消融实验：**
- 列出所有创新/优化模块
- 每次只禁用一个，测量性能变化
- 验证每个创新点的贡献

**对比实验：**
- 选择 2-3 个替代算法/实现
- 在相同数据集上对比
- 确定对比维度

向用户确认：
```
实验方案：
1. Baseline：标准哈夫曼 vs 等长编码
2. 消融：禁用范式编码 → 测量头部大小变化
3. 对比：哈夫曼 vs LZ77 vs 算术编码

测试数据：
- 小规模：1KB 英文文本
- 中规模：100KB 混合文本
- 大规模：1MB 二进制文件
- 极端：全相同字节 / 均匀分布字节

评估指标：
- 主要：压缩率
- 辅助：编码效率、编码时间、解码时间

是否同意？（可以修改）
```

### Step 5: 生成任务树

汇总 4 轮 review 结果，生成 `.pipeline/tasks.json`：

```json
{
  "tasks": [
    {"id": "T001", "module": "frequency-analysis", "type": "implement", "status": "pending", "priority": 1, "dependencies": []},
    {"id": "T002", "module": "tree-building", "type": "implement", "status": "pending", "priority": 2, "dependencies": ["T001"]},
    {"id": "T003", "module": "canonical-codes", "type": "implement", "status": "pending", "priority": 3, "dependencies": ["T002"]},
    {"id": "T004", "module": "encoder", "type": "implement", "status": "pending", "priority": 4, "dependencies": ["T003"]},
    {"id": "T005", "module": "decoder", "type": "implement", "status": "pending", "priority": 4, "dependencies": ["T003"]},
    {"id": "T006", "module": "exporter", "type": "implement", "status": "pending", "priority": 5, "dependencies": ["T001", "T002", "T003"]},
    {"id": "T007", "module": "unit-tests", "type": "test", "status": "pending", "priority": 6, "dependencies": ["T004", "T005"]},
    {"id": "T008", "module": "baseline-experiment", "type": "experiment", "status": "pending", "priority": 7, "dependencies": ["T007"]},
    {"id": "T009", "module": "ablation-experiment", "type": "experiment", "status": "pending", "priority": 8, "dependencies": ["T008"]},
    {"id": "T010", "module": "comparison-experiment", "type": "experiment", "status": "pending", "priority": 9, "dependencies": ["T008"]}
  ]
}
```

### Step 6: 输出总结

```
[OMD] 规划完成！

方案摘要：
- {N} 个实现任务 + {M} 个实验任务
- 创新点 {K} 个：{列表}
- 预计实现顺序：{模块依赖链}

下一步：运行 /ds:implement 开始实现
```

更新 `orchestrator_state.md` 阶段为 `planned`。
