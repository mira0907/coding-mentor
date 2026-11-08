"""實作 8-2 掃街車路線的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7、m ≤ 10），max 用題目上限並依 seed 換不同形狀。
可能有重邊、自環與沒有街道的路口。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資；每條街道隨機前後顛倒，順序打亂"""
    edges = [(a, b) if random.random() < 0.5 else (b, a) for a, b in edges]
    random.shuffle(edges)
    print("\n".join([f"{n} {len(edges)}"] + [f"{a} {b}" for a, b in edges]))


def walk(n, m, closed, loop_p):
    """隨機走 m 步留下的街道：一定有歐拉路徑；closed = True 時最後走回起點（歐拉迴路）。
    loop_p = 走成自環的機率"""
    cur = start = random.randint(1, n)
    edges = []
    for i in range(m):
        if closed and i == m - 1:
            nxt = start
        elif random.random() < loop_p:
            nxt = cur
        else:
            nxt = random.randint(1, n)
        edges.append((cur, nxt))
        cur = nxt
    return edges


if size == "small":
    n = random.randint(1, 7)
    kind = seed % 6
    if seed == 1:                              # 最小：一個路口、一條環狀巷
        emit(1, [(1, 1)])
    elif seed == 2:                            # 一條街道，兩端不同
        emit(2, [(2, 1)])
    elif kind in (0, 1):                       # 隨機走，有路徑
        emit(n, walk(n, random.randint(1, 10), False, 0.12))
    elif kind == 2:                            # 隨機走回起點，有迴路
        emit(n, walk(n, random.randint(1, 10), True, 0.12))
    elif kind == 3:                            # 隨機走再多一條街道：常常有 4 個奇度點 → -1
        emit(n, walk(n, random.randint(1, 9), False, 0.1) + [(random.randint(1, n), random.randint(1, n))])
    elif kind == 4 and n >= 2:                 # 兩個分開的迴路：度數全偶但不連通 → -1
        verts = random.sample(range(1, n + 1), n)
        k = random.randint(1, n - 1)
        edges = []
        for part in (verts[:k], verts[k:]):
            cur = s = random.choice(part)
            L = random.randint(1, 4)
            for i in range(L):
                nxt = s if i == L - 1 else random.choice(part)
                edges.append((cur, nxt))
                cur = nxt
        emit(n, edges)
    else:                                      # 完全隨機的街道
        emit(n, [(random.randint(1, n), random.randint(1, n)) for _ in range(random.randint(1, 10))])
elif size == "mid":
    n = 2000
    emit(n, walk(n, 4000, seed % 2 == 0, 0.01))
else:
    n, m = 100000, 200000
    kind = (seed - 1) % 5
    if kind == 0:                              # 1-2-…-n 走過去再走回來，加兩個自環：堆疊深度約 m
        edges = [(i, i + 1) for i in range(1, n)] * 2 + [(1, 1), (1, 1)]
    elif kind == 1:                            # 隨機走：有歐拉路徑，起點是編號小的奇度點
        edges = walk(n, m, False, 0.0)
    elif kind == 2:                            # 星狀重邊加大量自環
        edges = [(1, i) for i in range(2, 50001)] * 2
        while len(edges) < m:
            u = random.randint(1, 50000)
            edges.append((u, u))
    elif kind == 3:                            # 兩個分開的大環加自環：度數全偶但不連通 → -1
        edges = [(i, i + 1) for i in range(1, 50000)] + [(50000, 1)]
        edges += [(i, i + 1) for i in range(50001, 100000)] + [(100000, 50001)]
        while len(edges) < m:
            u = random.randint(1, n)
            edges.append((u, u))
    else:                                      # 隨機走回起點：歐拉迴路
        edges = walk(n, m, True, 0.0)
    emit(n, edges)
