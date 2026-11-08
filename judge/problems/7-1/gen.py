"""實作 7-1 變電所歲修的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 10），max 用題目上限並依 seed 換不同形狀。"""
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


def emit(n, edges):
    """印出一筆測資：n 座變電所與 n − 1 條電纜"""
    print("\n".join([str(n)] + [f"{a} {b}" for a, b in edges]))


if size == "small":
    n = [1, 2, 3][seed - 1] if seed <= 3 else random.randint(1, 12)   # seed 1～3 是 n = 1、2、3
    shape = random.choice(["rand", "rand", "chain", "star", "cat", "broom"])
    emit(n, tree(n, shape))
elif size == "mid":
    n = random.choice([2000, 2001])            # 偶數長鏈會有兩個重心
    emit(n, tree(n, random.choice(["rand", "broom", "cat", "chain"])))
else:
    n = 200000
    shape = ["chain", "star", "rand", "broom"][(seed - 1) % 4]
    # chain：長鏈，有兩個重心 100000 附近；star：中心就是答案；rand：隨機樹；broom：掃把
    emit(n, tree(n, shape))
