"""範例 1-A 握手統計的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 6），max 用題目上限並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 個人、edges 是 (u, v) 的清單"""
    print(n, len(edges))
    if edges:
        print("\n".join(f"{u} {v}" for u, v in edges))


def pair(n):
    """隨機挑兩個不同的人"""
    u, v = random.sample(range(1, n + 1), 2)
    return u, v


if size == "small":
    n = 1 if seed == 1 else random.randint(1, 6)
    mode = seed % 4
    if n == 1 or mode == 0:                      # 只有一人或沒有握手
        edges = []
    elif mode == 1:                              # 同一對人握很多次
        u, v = pair(n)
        edges = [(u, v) if random.random() < 0.5 else (v, u) for _ in range(random.randint(1, 7))]
    else:                                        # 隨機握手，常有重複的一對
        edges = [pair(n) for _ in range(random.randint(1, 12))]
    emit(n, edges)
elif size == "mid":
    n, m = 2000, 6000
    emit(n, [pair(n) for _ in range(m)])
else:
    n, m = 100000, 200000
    kind = seed % 4
    if kind == 1:                                # 隨機握手
        edges = [pair(n) for _ in range(m)]
    elif kind == 2:                              # 星形：每次都有第 1 人，他的次數是 2×10⁵
        edges = [(1, i % (n - 1) + 2) for i in range(m)]
    elif kind == 3:                              # 所有握手都是同一對人
        edges = [(1, 2) if i % 2 == 0 else (2, 1) for i in range(m)]
    else:                                        # 長鏈加隨機握手，人數為奇數的分布較平均
        edges = [(i, i + 1) for i in range(1, n)]
        while len(edges) < m:
            edges.append(pair(n))
    emit(n, edges)
