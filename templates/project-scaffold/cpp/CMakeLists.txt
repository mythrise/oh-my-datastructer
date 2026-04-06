cmake_minimum_required(VERSION 3.14)
project({{PROJECT_NAME}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 主程序
add_executable(main src/main.cpp)

# 测试
add_executable(test_core tests/test_core.cpp)
enable_testing()
add_test(NAME test_core COMMAND test_core)
