"""實作 1-1 整理路網的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 6），max 用題目上限並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 個路口、edges 是 (u, v) 的清單"""
    print(n, len(edges))
    if edges:
        print("\n".join(f"{u} {v}" for u, v in edges))


if size == "small":
    n = 1 if seed == 1 else random.randint(1, 6)
    mode = seed % 5
    if mode == 0:                                # 沒有道路
        edges = []
    elif mode == 1:                              # 全部是自環
        edges = [(u, u) for u in (random.randint(1, n) for _ in range(random.randint(1, 6)))]
    elif mode == 2:                              # 同一對路口記很多次，正反都有
        u, v = random.randint(1, n), random.randint(1, n)
        edges = [(u, v) if random.random() < 0.5 else (v, u) for _ in range(random.randint(1, 8))]
    else:                                        # 隨機，約兩成自環，重邊很多
        edges = []
        for _ in range(random.randint(1, 12)):
            u = random.randint(1, n)
            edges.append((u, u if random.random() < 0.2 else random.randint(1, n)))
    emit(n, edges)
elif size == "mid":
    n, m = 2000, 6000
    pool = [(random.randint(1, n), random.randint(1, n)) for _ in range(1500)]   # 從小池子挑，重邊多
    edges = []
    for _ in range(m):
        u, v = random.choice(pool)
        edges.append((u, v) if random.random() < 0.5 else (v, u))
    emit(n, edges)
else:
    n, m = 200000, 200000
    kind = seed % 5
    if kind == 1:                                # 隨機，幾乎沒有重邊
        edges = [(random.randint(1, n), random.randint(1, n)) for _ in range(m)]
    elif kind == 2:                              # 星形：路口 1 連到所有人，度數接近 2×10⁵
        edges = [(1, i % (n - 1) + 2) if i % 3 else (i % (n - 1) + 2, 1) for i in range(m)]
    elif kind == 3:                              # 全部是同一對路口，正反交錯：多餘的有 m − 1 條
        edges = [(1, 2) if i % 2 == 0 else (2, 1) for i in range(m)]
    elif kind == 4:                              # 全部是自環
        edges = [(u, u) for u in (random.randint(1, n) for _ in range(m))]
    else:                                        # 從 5×10⁴ 條道路的池子挑，正反都有、夾雜自環
        pool = [(random.randint(1, n), random.randint(1, n)) for _ in range(50000)]
        edges = []
        for _ in range(m):
            u, v = random.choice(pool)
            edges.append((u, v) if random.random() < 0.5 else (v, u))
    emit(n, edges)
