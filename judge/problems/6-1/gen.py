"""實作 6-1 關鍵路口的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 9），max 用題目上限並依 seed 換不同形狀。
題目允許重複的道路（u ≠ v），圖也可能不連通。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges, relabel=True):
    """印出一筆測資：n 個路口、edges 是 (u, v) 道路；relabel 時打亂點的編號與道路順序"""
    lab = list(range(n + 1))
    if relabel:
        lab = [0] + random.sample(range(1, n + 1), n)
        random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{lab[u]} {lab[v]}" if random.random() < 0.5 else f"{lab[v]} {lab[u]}"
                        for u, v in edges))


def tree(n):
    """隨機樹的 n - 1 條邊"""
    return [(random.randint(1, v - 1), v) for v in range(2, n + 1)]


def pair(lo, hi):
    """lo..hi 之間兩個不同的點"""
    return tuple(random.sample(range(lo, hi + 1), 2))


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 9)
    mode = seed % 5
    edges = []
    if n >= 2:
        if mode == 1:                            # 隨機樹再多幾條邊：割點多
            edges = tree(n) + [pair(1, n) for _ in range(random.randint(0, 2))]
        elif mode == 2:                          # 隨機多重圖，常有重複的道路
            for _ in range(random.randint(1, 14)):
                e = pair(1, n)
                edges.append(e)
                if random.random() < 0.25:
                    edges.append(e[::-1])
        elif mode == 3:                          # 稀疏隨機圖，常不連通
            edges = [pair(1, n) for _ in range(random.randint(0, n + 2))]
        elif mode == 4:                          # 兩個環共用一個點（蝴蝶結），或一條鏈
            if n >= 5 and seed % 10 == 4:
                k = random.randint(3, n - 2)     # 1..k 一個環，k..n 一個環，k 是割點
                edges = [(i, i + 1) for i in range(1, k)] + [(k, 1)]
                edges += [(i, i + 1) for i in range(k, n)] + [(n, k)]
            else:
                edges = [(i, i + 1) for i in range(1, n)]
        # mode 0：沒有道路
    emit(n, edges)
elif size == "mid":
    n = 2000
    edges = tree(n) + [pair(1, n) for _ in range(seed * 100)]   # 樹 + 額外的邊，割點由多到少
    if seed % 2 == 0:
        edges += random.sample(edges, 300)       # 一些重複的道路
    emit(n, edges)
else:
    n = m = 200000
    shape = (seed - 1) % 6
    if shape == 0:                               # 長鏈：DFS 深度 2×10⁵，割點是中間所有點
        emit(n, [(i, i + 1) for i in range(1, n)])
    elif shape == 1:                             # 星形：只有中心是割點
        emit(n, [(1, v) for v in range(2, n + 1)])
    elif shape == 2:                             # 大環：沒有割點
        emit(n, [(i, i % n + 1) for i in range(1, n + 1)])
    elif shape == 3:                             # 隨機樹加一條邊，m = 2×10⁵
        emit(n, tree(n) + [pair(1, n)])
    elif shape == 4:                             # 每段兩條重複道路的長鏈：重邊不影響割點
        n = 100001
        emit(n, [(i, i + 1) for i in range(1, n)] * 2, relabel=False)
    else:                                        # 三角形一個接一個共用頂點（仙人掌）：沒有橋，但很多割點
        edges = []
        v = 1
        while v + 2 <= 133333:
            edges += [(v, v + 1), (v + 1, v + 2), (v + 2, v)]
            v += 2
        while len(edges) < m:                    # 其餘的點隨機連成一團
            edges.append(pair(133334, n))
        emit(n, edges)
