"""實作 3-1 夜市聯合會議的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 6），max 用題目上限並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, t, edges):
    """印出一筆測資：n 個點、會場 t、edges 是 (u, v, w) 的清單"""
    print(n, len(edges), t)
    print("\n".join(f"{u} {v} {w}" for u, v, w in edges))


if size == "small":
    n = random.randint(1, 6)
    m = 0 if seed % 10 == 0 else random.randint(0, 12)
    t = random.randint(1, n)
    maxw = random.choice([1, 3, 10, 10**9])
    emit(n, t, [(random.randint(1, n), random.randint(1, n), random.randint(1, maxw)) for _ in range(m)])
elif size == "mid":
    n, m = 2000, 6000
    t = random.randint(1, n)
    emit(n, t, [(random.randint(1, n), random.randint(1, n), random.randint(1, 10**9)) for _ in range(m)])
else:
    n, m = 100000, 200000
    edges = []
    if seed % 2 == 1:                            # 隨機圖
        t = random.randint(1, n)
        edges = [(random.randint(1, n), random.randint(1, n), random.randint(1, 10**9)) for _ in range(m)]
    else:                                        # 雙向長鏈，來回距離可達約 2×10¹⁴，考驗 long long
        t = 1
        for i in range(1, n):
            edges.append((i, i + 1, 10**9))
            edges.append((i + 1, i, 10**9))
        while len(edges) < m:
            edges.append((1, 1, 10**9))
    emit(n, t, edges)
