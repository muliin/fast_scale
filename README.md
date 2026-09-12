# fast_scale

一个 **C++ / Python 混合编程示例**：使用 `pybind11` 将 C++ 函数暴露给 Python 调用，实现 **真正的零拷贝** 数组操作，并通过基准测试对比 **零拷贝版本** 与 **传统深拷贝版本** 的性能差异。

本项目复现自 **[AllinfraGuide](https://caomaolufei.github.io/AIInfraGuide/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/%E7%AC%AC1%E7%AB%A0-%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80%E5%9F%BA%E7%A1%80/#10-%E7%BB%BC%E5%90%88%E5%AE%9E%E6%88%98%E7%BB%99-python-%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA-c-%E7%AE%97%E5%AD%90)** 第 10 章，并在原教程基础上改进了 **自动类型转换导致的深拷贝开销**，使用 `py::array_t` 直接操作 NumPy 底层内存。同时保留 `scale_legacy` 作为深拷贝基线，并新增 `benchmark.py` 量化性能差异。

## 特性

- 使用 **C++17** 编写核心计算逻辑
- 通过 **pybind11** 自动生成 Python 绑定
- **零拷贝**：使用 `py::array_t<float>` 直接访问 NumPy 数组内存，避免 `std::vector` 的元素级拷贝
- 提供三个版本：
  - `scale_inplace`：原地修改输入数组（零拷贝，无内存分配）
  - `scale_new`：返回新数组（输入零拷贝，输出由 NumPy 管理）
  - `scale_legacy`：传统 `std::vector` 版本（存在深拷贝，仅用于对比）
- 使用 **CMake** 构建，支持 Windows / Linux / macOS
- 提供 Python 测试脚本验证功能
- 提供 **benchmark.py** 性能基准测试，对比零拷贝与深拷贝的耗时和加速比
- 包含 `.gitignore`，避免将编译产物提交到仓库

## 环境要求

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

## 构建步骤

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
>
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

## 运行测试

```bash
python test_scale.py
```

预期输出：

```text
in-place: [ 2. -4.  7.]
new array: [ 2. -4.  7.]
original unchanged: [ 1. -2.  3.5]
```

## 运行性能基准测试

构建完成后，可以运行：

```bash
python benchmark.py
```

该脚本会对比：

- `scale_new`：零拷贝版本，输入为 NumPy 数组，返回新的 NumPy 数组
- `scale_legacy`：传统深拷贝版本，输入为 Python list，内部转换为 `std::vector<float>`，返回时再转换回 Python list
- `scale_inplace`：原地修改版本，额外测试 10,000,000 元素的原地缩放耗时

输出格式类似：

```text
       数组大小 | 零拷贝-new (ms) | 深拷贝-legacy (ms) |    加速比
------------------------------------------------------------------------
       100,000 |             ... |                ... |    ...x
     1,000,000 |             ... |                ... |    ...x
    10,000,000 |             ... |                ... |    ...x

额外：原地修改版本（in-place）
  10,000,000 元素原地修改：平均 ... ms
```

具体数值因机器、编译器、Python 版本和构建配置而异。`scale_legacy` 的耗时包含 Python list 与 `std::vector` 之间的双向深拷贝，因此通常明显慢于零拷贝版本。

## 项目结构

```text
fast_scale/
├── CMakeLists.txt          # CMake 构建脚本
├── CMakePresets.json       # CMake 预设配置（跨平台）
├── scale.cpp               # C++ 核心实现与 pybind11 绑定
├── test_scale.py           # Python 功能测试脚本
├── benchmark.py            # Python 性能基准测试脚本
├── .gitignore              # Git 忽略规则
└── README.md               # 本文件
```

## 使用示例

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

# 示例 2：返回新数组（输入零拷贝，输出由 NumPy 管理）
arr2 = np.array([1.0, -2.0, 3.5], dtype=np.float32)
result = fast_scale.scale_new(arr2, 2.0)
print(result)  # [ 2. -4.  7.]
print(arr2)    # [ 1. -2.  3.5] 原数组不变

# 示例 3：传统深拷贝版本（仅用于对比，不推荐高性能场景）
arr_list = [1.0, -2.0, 3.5]
result_legacy = fast_scale.scale_legacy(arr_list, 2.0)
print(result_legacy)  # [2.0, -4.0, 7.0]
print(arr_list)       # [1.0, -2.0, 3.5]
```

## API

### `scale_inplace(input, factor)`

原地缩放输入数组。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `input` | `numpy.ndarray` | 一维 `float32` 数组，必须可写 |
| `factor` | `float` | 缩放因子 |

返回值：`None`

说明：

- 直接修改输入数组。
- 如果输入不是一维数组，会抛出 `RuntimeError: Input must be a 1-D array`。
- 如果输入数组不可写，会抛出 `RuntimeError: Input array is not writeable`。

### `scale_new(input, factor)`

返回一个新的缩放后的 NumPy 数组，不修改输入数组。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `input` | `numpy.ndarray` | 一维 `float32` 数组 |
| `factor` | `float` | 缩放因子 |

返回值：`numpy.ndarray`，新的一维 `float32` 数组。

说明：

- 原输入数组保持不变。
- 输入通过 `py::array_t<float>` 直接访问，避免元素级深拷贝。
- 如果输入不是一维数组，会抛出 `RuntimeError: Input must be a 1-D array`。

### `scale_legacy(input, factor)`

传统深拷贝版本，使用 `std::vector<float>` 实现。

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `input` | `list[float]` 或可转换为 `std::vector<float>` 的序列 | Python list 等 |
| `factor` | `float` | 缩放因子 |

返回值：`list[float]`，缩放后的新列表。

说明：

- 通过 `pybind11/stl.h` 自动完成 Python list 与 `std::vector<float>` 之间的转换。
- 转换过程存在元素级深拷贝，性能较差。
- 仅用于与零拷贝版本进行性能对比，不推荐在生产高性能路径中使用。

## 改进说明：零拷贝 vs 深拷贝

原教程使用 `std::vector<float>` 作为参数和返回类型。由于 Python list 和 `std::vector` 的内存布局完全不同，`pybind11/stl.h` 会在两个方向上各产生一次 **元素级深拷贝**：

```text
Python list  ──深拷贝──►  std::vector<float>  ──深拷贝──►  Python list
```

本项目改用 `py::array_t<float>`，通过 Python 的 **缓冲区协议（Buffer Protocol）** 直接访问 NumPy 数组底层内存：

```text
NumPy ndarray  ◄──零拷贝──►  float* 指针
```

- 传入时：直接拿到内存首地址，不复制任何元素。
- `scale_inplace`：直接在原数组上修改，无输出分配。
- `scale_new`：创建新的 NumPy 数组并写入结果，返回时由 NumPy 管理内存，不经过 Python list / `std::vector` 转换。
- `scale_legacy`：保留传统 `std::vector` 路径，作为深拷贝基线。
- `benchmark.py`：量化 `scale_new` 与 `scale_legacy` 的耗时差异，并计算加速比。

代价：零拷贝版本要求输入必须是 `dtype=np.float32` 的 NumPy 数组（或可被 `forcecast` 转换），而 `scale_legacy` 可以接收普通 Python list。

## 跨平台说明

本项目已尽量做到跨平台。关键点：

- `CMakeLists.txt` 使用 `find_package(Python)` 和 `find_package(pybind11)` 自动探测依赖，不硬编码路径。
- 通过 `execute_process` 动态获取 `pybind11` 的 CMake 路径，避免写死绝对路径。
- 使用生成器表达式 `$<CONFIG>` 控制输出目录，兼容多配置生成器（Visual Studio）和单配置生成器（Makefile / Ninja）。
- `CMakePresets.json` 不指定生成器和架构，交由 CMake 自动选择。

在 Windows、Linux、macOS 上均使用同一套命令构建。

## 来源与致谢

本项目复现自 **[AllinfraGuide](https://caomaolufei.github.io/AIInfraGuide/guides/%E6%A8%A1%E5%9D%97%E4%B8%80-%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86/%E7%AC%AC1%E7%AB%A0-%E7%BC%96%E7%A8%8B%E8%AF%AD%E8%A8%80%E5%9F%BA%E7%A1%80/#10-%E7%BB%BC%E5%90%88%E5%AE%9E%E6%88%98%E7%BB%99-python-%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA-c-%E7%AE%97%E5%AD%90)** 第 10 章“综合实战：给 Python 添加一个 C++ 算子”。

- 原教程作者：caomaoluofei
- 原教程地址：https://caomaolufei.github.io/AIInfraGuide/
- 本项目的代码根据教程思路自行编写与整理，并在此基础上改进了零拷贝方案。
- 部分概念与接口设计参考原教程，版权归原作者所有。

感谢原教程提供的清晰指引。

## 注意事项

- 使用 `py::array_t` 时，输入数组的 `dtype` 必须是 `float32`。
- 原地修改版本 `scale_inplace` 会直接修改输入数组，调用前请确认这是预期行为。
- 如果传入只读数组或非一维数组，C++ 会抛出 `RuntimeError`，Python 端可捕获。
- `scale_legacy` 接收 Python list 等序列类型，内部存在深拷贝，性能较差，仅用于对比。
- `benchmark.py` 中的 in-place 测试会反复修改同一个数组，可能导致数值溢出，但仅用于测量耗时。