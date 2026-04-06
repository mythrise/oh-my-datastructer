/**
 * {{PROJECT_NAME}} — 核心算法头文件
 *
 * 由 /ds:implement 根据架构蓝图填充具体声明。
 */
#ifndef CORE_H
#define CORE_H

#include <stddef.h>
#include <stdint.h>

/* ===== 数据结构定义 ===== */

// TODO: 由 /ds:implement 定义具体数据结构
// 示例:
// typedef struct Node {
//     int key;
//     struct Node *left, *right;
// } Node;

/* ===== 核心接口 ===== */

/**
 * 运行核心算法
 * @param input_path  输入文件路径
 * @param output_path 输出文件路径
 * @return 0=成功, 非0=错误码
 */
int core_run(const char *input_path, const char *output_path);

/**
 * 分析输入数据或运行结果
 * @param input_path 输入文件路径
 * @return 0=成功, 非0=错误码
 */
int core_analyze(const char *input_path);

/**
 * 导出可视化数据为 JSON
 * @param input_path  输入文件路径
 * @param output_path JSON 输出路径
 * @return 0=成功, 非0=错误码
 */
int core_export(const char *input_path, const char *output_path);

#endif /* CORE_H */
