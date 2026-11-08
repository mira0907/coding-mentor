"""實作 6-2 颱風停課通知的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 5），max 用題目上限並依 seed 換不同形狀。
題目允許重複的線路和 u = v 的線路。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges, relabel=False):
    """印出一筆測資：n 所學校、edges 是 (u, v) 線路；relabel 時打亂學校編號與線路順序"""
    lab = list(range(n + 1))
    if relabel:
        lab = [0] + random.sample(range(1, n + 1), n)
        random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{lab[u]} {lab[v]}" for u, v in edges))


if size == "small":
    n = 1 if seed in (1, 2) else random.randint(2, 5)
    mode = seed % 5
    if seed == 1:                                # n = 1、沒有線路：答案 1 0
        m = 0
    elif mode == 0:
        m = random.randint(0, 2)                 # 幾乎沒有線路
    elif mode == 1:
        m = random.randint(n, 3 * n)             # 偏密，常常整張圖強連通
    else:
        m = random.randint(0, 2 * n)
    edges = []
    for _ in range(m):
        u, v = random.randint(1, n), random.randint(1, n)   # 允許 u = v
        edges.append((u, v))
        if mode == 4 and random.random() < 0.3:
            edges.append((u, v))                 # 重複的線路
    if mode == 3 and n >= 2:                     # 大環缺一條：只差一點就強連通
        ring = [(i, i % n + 1) for i in range(1, n + 1)]
        ring.pop(random.randrange(n))
        edges += ring
    random.shuffle(edges)
    emit(n, edges)
elif size == "mid":
    n = 2000
    m = [1000, 2000, 3000, 4000][(seed - 1) % 4]  # 線路由少到多：SCC 由碎到大
    emit(n, [(random.randint(1, n), random.randint(1, n)) for _ in range(m)])
else:
    n = 200000
    shape = (seed - 1) % 6
    if shape == 0:                               # 有向長鏈 1 → 2 → … → n：答案 1 1，Tarjan 深度 2×10⁵
        emit(n, [(i, i + 1) for i in range(1, n)])
    elif shape == 1:                             # 反向長鏈 n → … → 1：從 1 開始 DFS 很淺，從 n 開始才深
        emit(n, [(i + 1, i) for i in range(1, n)])
    elif shape == 2:                             # 大環：已經強連通，答案 1 0
        emit(n, [(i, i % n + 1) for i in range(1, n + 1)])
    elif shape == 3:                             # 1 通知其他所有學校：源 1 個、匯 n-1 個
        emit(n, [(1, v) for v in range(2, n + 1)], relabel=True)
    elif shape == 4:                             # 隨機有向圖，m = 2×10⁵
        emit(n, [(random.randint(1, n), random.randint(1, n)) for _ in range(200000)])
    else:                                        # 一個 10⁵ 點的大環 + 其他學校隨機指向環、或被環指向，含自環與重複線路
        half = 100000
        edges = [(i, i % half + 1) for i in range(1, half + 1)]
        while len(edges) < 199000:
            v = random.randint(half + 1, n)
            edges.append((random.randint(1, half), v) if random.random() < 0.5 else (v, random.randint(1, half)))
        edges += [(v, v) for v in random.sample(range(1, n + 1), 500)]
        edges += random.sample(edges, 500)
        emit(n, edges, relabel=True)
