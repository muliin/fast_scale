import sys
import os
import numpy as np

# 兼容 Windows (build/Release, build/Debug) 和 Linux/macOS (build)
for path in ["build", "build/Release", "build/Debug"]:
    if os.path.exists(path):
        sys.path.insert(0, path)
        
import fast_scale

# --- 测试原地修改版本 ---
arr = np.array([1.0, -2.0, 3.5], dtype=np.float32)
fast_scale.scale_inplace(arr, 2.0)
print("in-place:", arr)   # 输出: [2.0, -4.0, 7.0]

# --- 测试返回新数组版本 ---
arr2 = np.array([1.0, -2.0, 3.5], dtype=np.float32)
result = fast_scale.scale_new(arr2, 2.0)
print("new array:", result)  # 输出: [2.0, -4.0, 7.0]
print("original unchanged:", arr2)  # 输出: [1.0, -2.0, 3.5]