cmake_minimum_required(VERSION 3.20)
project(fast_scale LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
# 先找到 Python 解释器（前面已经 find_package 过了）
# 这里利用 Python 来获取 pybind11 的 CMake 配置路径
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
# 将获取到的路径设置为 CMake 变量，供 find_package 使用
set(pybind11_DIR "${pybind11_DIR}" CACHE PATH "Path to pybind11 CMake directory")
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(fast_scale scale.cpp)
target_compile_features(fast_scale PRIVATE cxx_std_17)

set_target_properties(fast_scale PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}"
    )