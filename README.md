# fast_scale

一个 **C++ / Python 混合编程示例**：使用 `pybind11` 将 C++ 函数暴露给 Python 调用，并实现 **真正的零拷贝** 数组操作。

本项目复现自 **[AllinfraGuide](https://caomaolufei.github.io/AIInfraGuide/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/%E7%AC%AC1%E7%AB%A0-%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80%E5%9F%BA%E7%A1%80/#10-%E7%BB%BC%E5%90%88%E5%AE%9E%E6%88%98%E7%BB%99-python-%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA-c-%E7%AE%97%E5%AD%90)** 第 10 章，并在原教程基础上改进了 **自动类型转换导致的深拷贝开销**，使用 `py::array_t` 直接操作 NumPy 底层内存。

##  特性

- 使用 **C++17** 编写核心计算逻辑
- 通过 **pybind11** 自动生成 Python 绑定
- **零拷贝**：使用 `py::array_t<float>` 直接访问 NumPy 数组内存，避免 `std::vector` 的元素级拷贝
- 提供两个版本：
  - `scale_inplace`：原地修改输入数组（零拷贝，无内存分配）
  - `scale_new`：返回新数组（由 NumPy 管理内存，零拷贝返回）
- 使用 **CMake** 构建，支持 Windows / Linux / macOS
- 提供 Python 测试脚本验证功能
- 包含 `.gitignore`，避免将编译产物提交到仓库

##  环境要求

| 依赖 | 版本要求 | 说明 |
| :--- | :--- | :--- |
| CMake | ≥ 3.20 | 构建系统 |
| C++ 编译器 | 支持 C++17 | MSVC / GCC / Clang |
| Python | ≥ 3.8 | 解释器与开发头文件 |
| pybind11 | 最新版 | 通过 `pip install pybind11` 安装 |
| NumPy | 最新版 | 用于测试和实际使用 |

> **Windows 用户**：需要安装 Visual Studio 的“使用 C++ 的桌面开发”工作负载。  
> **Linux 用户**：确保已安装 `python3-dev`（或 `python3-devel`）和 `g++`。  
> **macOS 用户**：确保已安装 Xcode Command Line Tools。

##  构建步骤

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/fast_scale.git
cd fast_scale
```

### 2. 创建并激活 Python 虚拟环境（可选，推荐）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 3. 安装 pybind11 和 NumPy

```bash
python -m pip install pybind11 numpy
```

### 4. 配置 CMake

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
```

> **Windows + Visual Studio 用户**：CMake 会自动选择 Visual Studio 生成器，无需指定 `-DCMAKE_BUILD_TYPE`，可以直接使用 `cmake -S . -B build`。  
> 如果使用 `CMakePresets.json`，可以直接在 VS Code 中点击“配置”按钮，或运行：
> ```bash
> cmake --preset default
> ```

### 5. 构建

```bash
cmake --build build --parallel
```

编译成功后，会在 `build/` 目录下生成：
- Windows：`fast_scale.pyd`（可能位于 `build/Release/`）
- Linux / macOS：`fast_scale.so`

##  运行测试

```bash
python test_scale.py
```

预期输出：

```
in-place: [ 2. -4.  7.]
new array: [ 2. -4.  7.]
original unchanged: [ 1. -2.  3.5]
```

##  项目结构

```
fast_scale/
├── CMakeLists.txt          # CMake 构建脚本
├── CMakePresets.json       # CMake 预设配置（跨平台）
├── scale.cpp               # C++ 核心实现与 pybind11 绑定
├── test_scale.py           # Python 测试脚本
├── .gitignore              # Git 忽略规则
└── README.md               # 本文件
```

##  使用示例

```python
import sys
import os
import numpy as np

# 自动查找编译输出目录（兼容 Windows 和 Linux/macOS）
for path in ["build/Release", "build/Debug", "build"]:
    if os.path.exists(path):
        sys.path.insert(0, path)
        break

import fast_scale

# 示例 1：原地修改（零拷贝，无内存分配）
arr = np.array([1.0, -2.0, 3.5], dtype=np.float32)
fast_scale.scale_inplace(arr, 2.0)
print(arr)  # [ 2. -4.  7.]

# 示例 2：返回新数组（由 NumPy 管理内存）
arr2 = np.array([1.0, -2.0, 3.5], dtype=np.float32)
result = fast_scale.scale_new(arr2, 2.0)
print(result)  # [ 2. -4.  7.]
print(arr2)    # [ 1. -2.  3.5] 原数组不变
```

##  改进说明：零拷贝

原教程使用 `std::vector<float>` 作为参数和返回类型。由于 Python 列表和 `std::vector` 的内存布局完全不同，`pybind11/stl.h` 会在两个方向上各产生一次**元素级深拷贝**：

```
Python list  ──深拷贝──►  std::vector<float>  ──深拷贝──►  Python list
```

本项目改用 `py::array_t<float>`，通过 Python 的 **缓冲区协议（Buffer Protocol）** 直接访问 NumPy 数组底层内存：

```
NumPy ndarray  ◄──零拷贝──►  float* 指针
```

- 传入时：直接拿到内存首地址，不复制任何元素。
- 返回时：`py::array_t<float>` 封装 NumPy 内存，零拷贝返回。
- 代价：要求输入必须是 `dtype=np.float32` 的 NumPy 数组（或可被 `forcecast` 转换）。

##  跨平台说明

本项目已尽量做到跨平台。关键点：

- `CMakeLists.txt` 使用 `find_package(Python)` 和 `find_package(pybind11)` 自动探测依赖，不硬编码路径。
- 通过 `execute_process` 动态获取 `pybind11` 的 CMake 路径，避免写死绝对路径。
- 使用生成器表达式 `$<CONFIG>` 控制输出目录，兼容多配置生成器（Visual Studio）和单配置生成器（Makefile / Ninja）。
- `CMakePresets.json` 不指定生成器和架构，交由 CMake 自动选择。

在 Windows、Linux、macOS 上均使用同一套命令构建。

##  来源与致谢

本项目复现自 **[AllinfraGuide](https://caomaolufei.github.io/AIInfraGuide/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/%E7%AC%AC1%E7%AB%A0-%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80%E5%9F%BA%E7%A1%80/#10-%E7%BB%BC%E5%90%88%E5%AE%9E%E6%88%98%E7%BB%99-python-%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA-c-%E7%AE%97%E5%AD%90)** 第 10 章“综合实战：给 Python 添加一个 C++ 算子”。

- 原教程作者：caomaoluofei
- 原教程地址：https://caomaolufei.github.io/AIInfraGuide/guides/
- 本项目的代码根据教程思路自行编写与整理，并在此基础上改进了零拷贝方案。
- 部分概念与接口设计参考原教程，版权归原作者所有。

感谢原教程提供的清晰指引。

##  注意事项

- 使用 `py::array_t` 时，输入数组的 `dtype` 必须是 `float32`。
- 原地修改版本 `scale_inplace` 会直接修改输入数组，调用前请确认这是预期行为。
- 如果传入只读数组或非一维数组，C++ 会抛出 `RuntimeError`，Python 端可捕获。


