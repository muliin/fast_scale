import sys
import os
import time
import numpy as np


for path in ["build/Release", "build/Debug", "build"]:
    if os.path.exists(path):
        sys.path.insert(0, path)
        break

import fast_scale


def bench(func, data, factor, repeat=10, warmup=2):
    """跑 repeat 次，返回最短时间和平均时间（秒）。"""

    for _ in range(warmup):
        func(data, factor)

    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        func(data, factor)
        times.append(time.perf_counter() - start)

    return min(times), sum(times) / len(times)


def main():
    sizes = [100_000, 1_000_000, 10_000_000]
    factor = 2.0

    print(f"{'数组大小':>14} | {'零拷贝-new (ms)':>16} | {'深拷贝-legacy (ms)':>18} | {'加速比':>8}")
    print("-" * 72)

    for size in sizes:

        arr_np = np.random.rand(size).astype(np.float32)
        _, avg_zc = bench(fast_scale.scale_new, arr_np, factor)

        arr_list = arr_np.tolist()
        _, avg_dc = bench(fast_scale.scale_legacy, arr_list, factor)

        speedup = avg_dc / avg_zc
        print(f"{size:>14,} | {avg_zc * 1000:>16.3f} | {avg_dc * 1000:>18.3f} | {speedup:>7.2f}x")


    print()
    print("额外：原地修改版本（in-place）")
    arr = np.random.rand(10_000_000).astype(np.float32)
    _, avg_ip = bench(fast_scale.scale_inplace, arr, factor)
    print(f"  10,000,000 元素原地修改：平均 {avg_ip * 1000:.3f} ms")


if __name__ == "__main__":
    main()