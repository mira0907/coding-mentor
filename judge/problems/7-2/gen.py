"""實作 7-2 路口監視器的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 12），max 用題目上限並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def tree(n, shape):
    """依形狀產生 n 個點的樹，回傳邊 (a, b) 的清單；編號會打亂"""
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
    lab = [0] + random.sample(range(1, n + 1), n)   # lab[v] = 打亂後的編號
    edges = [(lab[v], lab[par[v]]) for v in range(2, n + 1)]
    edges = [(a, b) if random.random() < 0.5 else (b, a) for a, b in edges]
    random.shuffle(edges)
    return edges


def emit(n, edges, cost):
    """印出一筆測資；cost() 產生一個路口的監視器費用"""
    out = [str(n), " ".join(str(cost()) for _ in range(n))] + [f"{a} {b}" for a, b in edges]
    print("\n".join(out))


if size == "small":
    n = [1, 2][seed - 1] if seed <= 2 else random.randint(1, 12)   # seed 1、2 是 n = 1、2
    shape = random.choice(["rand", "rand", "chain", "star", "cat", "broom"])
    mode = random.choice(["tie", "tie", "big", "mixed"])
    if mode == "tie":                          # 費用 1～5，大量平手
        cost = lambda: random.randint(1, 5)
    elif mode == "big":                        # 費用接近 10⁹
        cost = lambda: random.randint(10**9 - 10, 10**9)
    else:                                      # 便宜與昂貴混在一起
        cost = lambda: random.choice([1, random.randint(1, 10**9), 10**9])
    emit(n, tree(n, shape), cost)
elif size == "mid":
    n = 2000
    emit(n, tree(n, random.choice(["rand", "broom", "cat"])), lambda: random.randint(1, 10**9))
else:
    n = 200000
    if seed % 4 == 1:                          # 長鏈、費用接近 10⁹：答案約 10¹⁴，考驗 long long
        emit(n, tree(n, "chain"), lambda: 10**9 - random.randint(0, 3))
    elif seed % 4 == 2:                        # 星狀、費用全是 10⁹：處處平手，只裝中心最省
        emit(n, tree(n, "star"), lambda: 10**9)
    elif seed % 4 == 3:                        # 隨機樹、隨機費用
        emit(n, tree(n, "rand"), lambda: random.randint(1, 10**9))
    else:                                      # 掃把、費用 1 或 10⁹
        emit(n, tree(n, "broom"), lambda: random.choice([1, 10**9]))
