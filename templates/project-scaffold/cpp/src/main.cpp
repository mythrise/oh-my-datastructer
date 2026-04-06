/**
 * {{PROJECT_NAME}} — 主入口 (C++)
 *
 * 编译: cmake -B build && cmake --build build
 * 运行: ./build/main <command> [args...]
 */
#include <iostream>
#include <string>
#include "core.hpp"

void print_usage(const char* prog) {
    std::cout << "Usage: " << prog << " <command> [options]\n"
              << "Commands:\n"
              << "  run <input> [output]    运行核心算法\n"
              << "  analyze <input>         分析结果\n"
              << "  export <input> [output] 导出可视化数据\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    std::string cmd = argv[1];

    if (cmd == "run") {
        if (argc < 3) {
            std::cerr << "Error: run 需要输入文件路径\n";
            return 1;
        }
        std::string output = argc > 3 ? argv[3] : "output.txt";
        return core::run(argv[2], output);
    }

    if (cmd == "analyze") {
        if (argc < 3) {
            std::cerr << "Error: analyze 需要输入文件路径\n";
            return 1;
        }
        return core::analyze(argv[2]);
    }

    if (cmd == "export") {
        if (argc < 3) {
            std::cerr << "Error: export 需要输入文件路径\n";
            return 1;
        }
        std::string output = argc > 3 ? argv[3] : "viz_data.json";
        return core::export_data(argv[2], output);
    }

    std::cerr << "Unknown command: " << cmd << "\n";
    print_usage(argv[0]);
    return 1;
}
