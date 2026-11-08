"""範例 6-A 關鍵道路的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
題目允許重邊（u ≠ v），圖也可能不連通。"""
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


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 8)
    mode = seed % 5
    edges = []
    if n >= 2:
        if mode == 1:                            # 隨機樹：每條都是關鍵道路
            edges = tree(n)
        elif mode == 2:                          # 樹再把幾條邊複製一次：重邊不是關鍵道路
            edges = tree(n)
            edges += random.sample(edges, random.randint(1, (len(edges) + 1) // 2))
        elif mode == 3:                          # 隨機多重圖，常有環和重邊
            for _ in range(random.randint(1, 10)):
                edges.append(tuple(random.sample(range(1, n + 1), 2)))
        elif mode == 4:                          # 稀疏，常不連通
            for _ in range(random.randint(1, n)):
                edges.append(tuple(random.sample(range(1, n + 1), 2)))
        # mode 0：沒有道路
    emit(n, edges)
elif size == "mid":
    n = 2000
    edges = tree(n)                              # 樹 + 一些額外邊，關鍵道路有多有少
    for _ in range(seed * 150):
        edges.append(tuple(random.sample(range(1, n + 1), 2)))
    if seed % 2 == 0:                            # 複製幾條樹邊：重邊讓它們不再關鍵
        edges += random.sample(edges[:n - 1], 200)
    emit(n, edges)
else:
    n, m = 100000, 200000
    shape = (seed - 1) % 5
    if shape == 0:                               # 長鏈：DFS 深度 10⁵，全部都是關鍵道路
        edges = [(i, i + 1) for i in range(1, n)]
        emit(n, edges, relabel=False)
    elif shape == 1:                             # 長鏈，偶數段有兩條重邊：只有奇數段是關鍵道路
        edges = []
        for i in range(1, n):
            edges.append((i, i + 1))
            if i % 2 == 0:
                edges.append((i + 1, i))
        emit(n, edges, relabel=False)
    elif shape == 2:                             # 星形加一些重邊
        edges = [(1, v) for v in range(2, n + 1)]
        edges += [(1, v) for v in random.sample(range(2, n + 1), 50000)]
        emit(n, edges)
    elif shape == 3:                             # 隨機樹加 10⁵ 條隨機邊：大部分邊都在環上
        edges = tree(n) + [tuple(random.sample(range(1, n + 1), 2)) for _ in range(m - n + 1)]
        emit(n, edges)
    else:                                        # 許多小環用橋串起來，另有不連通的部分
        edges = []
        v = 1
        while v + 5 <= 90000:                    # 每 5 個點一個環，環與環之間一條橋
            edges += [(v + i, v + (i + 1) % 5) for i in range(5)]
            edges.append((v + 4, v + 5))
            v += 5
        edges += tree(5000)                      # 1..5000 另外接一棵樹（和環有共用點）
        while len(edges) < m:                    # 剩下的點之間隨機連邊
            edges.append(tuple(random.sample(range(90001, n + 1), 2)))
        emit(n, edges)
