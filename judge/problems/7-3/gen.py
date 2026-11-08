"""實作 7-3 樹上配送的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 10、q ≤ 10），max 用題目上限並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def tree(n, shape, keep=False):
    """依形狀產生 n 個點的樹，回傳邊 (a, b) 的清單；keep = True 時不打亂編號"""
    par = [0] * (n + 1)                        # par[v] = v 的父節點（打亂編號前）
    for v in range(2, n + 1):
        if shape == "chain":                   # 長鏈
            par[v] = v - 1
        elif shape == "star":                  # 星狀
            par[v] = 1
        elif shape == "cat":                   # 毛毛蟲：主幹加上單點的腳
            par[v] = v - 1 if v % 2 == 0 else max(1, v - 2)
        elif shape == "broom":                 # 掃把：前半是鏈，後半隨機掛在鏈尾附近
            par[v] = v - 1 if v <= n // 2 else random.randint(n // 2, v - 1)
        else:                                  # 隨機樹
            par[v] = random.randint(1, v - 1)
    lab = list(range(n + 1)) if keep else [0] + random.sample(range(1, n + 1), n)   # lab[v] = 輸出用的編號
    edges = [(lab[v], lab[par[v]]) for v in range(2, n + 1)]
    edges = [(a, b) if random.random() < 0.5 else (b, a) for a, b in edges]
    random.shuffle(edges)
    return edges


def emit(n, edges, queries):
    """印出一筆測資：樹邊之後接 q 筆配送 (u, v)"""
    out = [f"{n} {len(queries)}"] + [f"{a} {b}" for a, b in edges] + [f"{u} {v}" for u, v in queries]
    print("\n".join(out))


if size == "small":
    n = 1 if seed == 1 else random.randint(1, 10)   # seed 1 是只有一個站點
    q = random.randint(1, 10)
    shape = random.choice(["rand", "rand", "chain", "star", "cat", "broom"])
    qs = []
    for _ in range(q):
        u = random.randint(1, n)
        v = u if random.random() < 0.2 else random.randint(1, n)   # 兩成機率起點等於終點
        qs.append((u, v))
    emit(n, tree(n, shape), qs)
elif size == "mid":
    n, q = 2000, 2000
    emit(n, tree(n, random.choice(["rand", "broom", "cat"])),
         [(random.randint(1, n), random.randint(1, n)) for _ in range(q)])
else:
    n = q = 200000
    kind = (seed - 1) % 5
    if kind == 0:                              # V 字形：根 1 下面掛兩條長鏈 A（15 萬點）、B（約 5 萬點）
        A = 150000                             # A = 第一條鏈的長度
        lab = [1] + random.sample(range(2, n + 1), n - 1)   # lab[i] = 第 i 個點的編號，根固定是 1
        edges = [(lab[0], lab[1]), (lab[0], lab[A + 1])]
        edges += [(lab[i], lab[i + 1]) for i in range(1, A)]          # A 鏈：lab[1..A]，深度 1..A
        edges += [(lab[i], lab[i + 1]) for i in range(A + 1, n - 1)]  # B 鏈：lab[A+1..n-1]，深度 1..n-1-A
        random.shuffle(edges)
        qs = []
        for _ in range(q):
            if random.random() < 0.1:          # 一成只經過根，讓根成為唯一的最大值
                qs.append((1, 1))
            else:                              # 九成從 A 深處到 B 淺處：深度差超過 2^17，倍增層數不夠會求錯 LCA，
                u = lab[random.randint(140000, A)]   # 而且每筆路徑長約 14 萬，逐點標記會超時
                v = lab[A + random.randint(1, 8000)]
                qs.append((u, v) if random.random() < 0.5 else (v, u))
        emit(n, edges, qs)
    elif kind == 1:                            # 星狀：每筆配送都經過中心，答案 = q
        emit(n, tree(n, "star"), [(random.randint(1, n), random.randint(1, n)) for _ in range(q)])
    elif kind == 2:                            # 隨機樹、隨機配送，夾雜起點等於終點
        qs = []
        for _ in range(q):
            u = random.randint(1, n)
            qs.append((u, u if random.random() < 0.1 else random.randint(1, n)))
        emit(n, tree(n, "rand"), qs)
    elif kind == 3:                            # 掃把：一半的點在長鏈上
        emit(n, tree(n, "broom"), [(random.randint(1, n), random.randint(1, n)) for _ in range(q)])
    else:                                      # 編號 1..n 的長鏈、根在一端，每筆都走過整條鏈
        far = lambda: (random.randint(1, 1000), random.randint(n - 1000, n))
        emit(n, tree(n, "chain", keep=True), [far() for _ in range(q)])
