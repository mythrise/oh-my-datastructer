/**
 * {{PROJECT_NAME}} — 主入口
 *
 * 编译: make
 * 运行: ./build/main <command> [args...]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "core.h"

static void print_usage(const char *prog) {
    printf("Usage: %s <command> [options]\n", prog);
    printf("Commands:\n");
    printf("  run <input> [output]    运行核心算法\n");
    printf("  analyze <input>         分析结果\n");
    printf("  export <input> [output] 导出可视化数据\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "run") == 0) {
        if (argc < 3) {
            fprintf(stderr, "Error: run 需要输入文件路径\n");
            return 1;
        }
        const char *output = argc > 3 ? argv[3] : "output.txt";
        return core_run(argv[2], output);
    }

    if (strcmp(argv[1], "analyze") == 0) {
        if (argc < 3) {
            fprintf(stderr, "Error: analyze 需要输入文件路径\n");
            return 1;
        }
        return core_analyze(argv[2]);
    }

    if (strcmp(argv[1], "export") == 0) {
        if (argc < 3) {
            fprintf(stderr, "Error: export 需要输入文件路径\n");
            return 1;
        }
        const char *output = argc > 3 ? argv[3] : "viz_data.json";
        return core_export(argv[2], output);
    }

    fprintf(stderr, "Unknown command: %s\n", argv[1]);
    print_usage(argv[0]);
    return 1;
}
