/**
 * {{PROJECT_NAME}} — 核心算法头文件 (C++)
 *
 * 由 /ds:implement 根据架构蓝图填充具体实现。
 */
#pragma once

#include <string>
#include <vector>
#include <memory>

namespace core {

/* ===== 数据结构定义 ===== */

// TODO: 由 /ds:implement 定义具体数据结构
// 示例:
// struct Node {
//     int key;
//     std::unique_ptr<Node> left, right;
// };

/* ===== 核心接口 ===== */

/**
 * 运行核心算法
 * @param input_path  输入文件路径
 * @param output_path 输出文件路径
 * @return 0=成功, 非0=错误码
 */
int run(const std::string& input_path, const std::string& output_path);

/**
 * 分析输入数据或运行结果
 * @param input_path 输入文件路径
 * @return 0=成功, 非0=错误码
 */
int analyze(const std::string& input_path);

/**
 * 导出可视化数据为 JSON
 * @param input_path  输入文件路径
 * @param output_path JSON 输出路径
 * @return 0=成功, 非0=错误码
 */
int export_data(const std::string& input_path, const std::string& output_path);

} // namespace core
