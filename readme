# fast_scale

基于 `pybind11` 的 Python C++ 扩展示例，用于对 NumPy 一维 `float32` 数组进行缩放操作。

## 功能

- `scale_inplace`：原地缩放 NumPy 数组，零拷贝修改输入数组。
- `scale_new`：返回一个新的缩放后的 NumPy 数组，不修改原数组。
- 使用 CMake Presets 简化配置与构建流程。
- 使用 C++17 和 `pybind11` 构建 Python 扩展模块。

## 环境要求

- CMake >= 3.20
- 支持 C++17 的编译器
- Python 3.x，包含 Python Development 组件
- Python 包：
  - `pybind11`
  - `numpy`

安装 Python 依赖：

```bash
python -m pip install pybind11 numpy
```

如果使用虚拟环境，请先激活虚拟环境，并确保 `python` 指向该环境。

## 构建

项目提供了 `CMakePresets.json`，可以直接使用 CMake Presets 构建。

### Release 构建

```bash
cmake --preset default
cmake --build --preset release
```

### Debug 构建

```bash
cmake --preset default
cmake --build --preset debug
```

如果不使用 Presets，也可以手动构建：

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

构建产物 `fast_scale` 扩展模块会输出到 `build`、`build/Release` 或 `build/Debug`，具体取决于生成器和构建配置。

## 运行测试

构建完成后运行：

```bash
python test_scale.py
```

预期输出类似：

```text
in-place: [ 2. -4.  7.]
new array: [ 2. -4.  7.]
original unchanged: [ 1. -2.  3.5]
```

`test_scale.py` 会自动尝试将以下目录加入 `sys.path`：

- `build`
- `build/Release`
- `build/Debug`

以兼容 Windows 和 Linux/macOS 的不同构建输出结构。

## 使用示例

```python
import numpy as np
import fast_scale

# 原地修改
arr = np.array([1.0, -2.0, 3.5], dtype=np.float32)
fast_scale.scale_inplace(arr, 2.0)
print(arr)
# 输出: [ 2. -4.  7.]

# 返回新数组
arr2 = np.array([1.0, -2.0, 3.5], dtype=np.float32)
result = fast_scale.scale_new(arr2, 2.0)
print(result)
# 输出: [ 2. -4.  7.]

print(arr2)
# 输出: [ 1. -2.  3.5]
```

## API

### `scale_inplace(input, factor)`

原地缩放输入数组。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `input` | `numpy.ndarray` | 一维 `float32` 数组，必须可写 |
| `factor` | `float` | 缩放因子 |

返回值：`None`

说明：

- 直接修改输入数组。
- 如果输入不是一维数组，会抛出 `RuntimeError: Input must be a 1-D array`。
- 如果输入数组不可写，会抛出 `RuntimeError: Input array is not writeable`。

### `scale_new(input, factor)`

返回一个新的缩放后的数组，不修改输入数组。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `input` | `numpy.ndarray` | 一维 `float32` 数组 |
| `factor` | `float` | 缩放因子 |

返回值：`numpy.ndarray`，新的一维 `float32` 数组。

说明：

- 原输入数组保持不变。
- 如果输入不是一维数组，会抛出 `RuntimeError: Input must be a 1-D array`。

## 项目结构

```text
.
├── CMakeLists.txt
├── CMakePresets.json
├── scale.cpp
└── test_scale.py
```

## 实现说明

- `CMakeLists.txt`
  - 使用 `find_package(Python COMPONENTS Interpreter Development REQUIRED)` 查找 Python。
  - 通过 `python -m pybind11 --cmakedir` 获取 `pybind11` 的 CMake 配置路径。
  - 使用 `pybind11_add_module(fast_scale scale.cpp)` 创建扩展模块。
  - 启用 C++17：`target_compile_features(fast_scale PRIVATE cxx_std_17)`。
  - 设置输出目录到 `${CMAKE_BINARY_DIR}/$<CONFIG>`。

- `CMakePresets.json`
  - `default`：配置预设，构建目录为 `${sourceDir}/build`，并开启 `CMAKE_EXPORT_COMPILE_COMMANDS`。
  - `release`：Release 构建预设。
  - `debug`：Debug 构建预设。

- `scale.cpp`
  - 使用 `py::array_t<float>` 和 `py::buffer_info` 访问 NumPy 数组。
  - `scale_inplace` 检查数组维度与可写性。
  - `scale_new` 创建新的 `py::array_t<float>` 并填充结果。
  - 通过 `PYBIND11_MODULE(fast_scale, module)` 导出模块。

- `test_scale.py`
  - 将构建目录加入 `sys.path`。
  - 导入 `fast_scale`。
  - 测试原地缩放和返回新数组两种模式。

## 注意事项

- `scale_inplace` 会直接修改输入数组，调用前请注意是否需要保留原始数据。
- 为了获得真正的零拷贝效果，建议传入 `dtype=np.float32` 且内存连续的 NumPy 数组。
- 当前实现主要针对一维数组，非一维输入会抛出异常。
- 构建产物路径可能因操作系统、CMake 生成器和构建配置不同而变化，测试脚本已对常见路径做了兼容处理。