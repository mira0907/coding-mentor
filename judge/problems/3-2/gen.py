"""實作 3-2 最短路計數的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7），max 用題目上限並依 seed 換不同形狀。
題目允許重邊（視為不同的邊），沒提到自環，所以不產生自環。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 邊權上限


def emit(n, edges):
    """印出一筆測資：n 個點、edges 是 (u, v, w) 的清單（順序與方向打亂）"""
    random.shuffle(edges)
    print(n, len(edges))
    print("\n".join(f"{u} {v} {w}" if random.random() < 0.5 else f"{v} {u} {w}" for u, v, w in edges))


def rand_edge(n, wf):
    """隨機一條不是自環的邊"""
    u, v = random.sample(range(1, n + 1), 2)
    return (u, v, wf())


def grid(R, C, wf):
    """R × C 的方格，點 1 在左上、點 R·C 在右下，只連右邊和下面的鄰居"""
    idx = lambda r, c: r * C + c + 1
    e = []
    for r in range(R):
        for c in range(C):
            if c + 1 < C:
                e.append((idx(r, c), idx(r, c + 1), wf()))
            if r + 1 < R:
                e.append((idx(r, c), idx(r + 1, c), wf()))
    return e


if size == "small":
    style = seed % 5
    n = random.randint(2, 7)
    m = random.randint(0, 12)
    if style == 0:                               # 點 n 走不到（答案 −1）；seed 5 是 n = 2、沒有邊
        if seed == 5:
            n, m = 2, 0
        k = random.randint(1, n - 1)             # 只在 1..k 之間連邊
        e = [rand_edge(k, lambda: random.randint(1, 3)) for _ in range(m)] if k >= 2 else []
        emit(n, e)
    elif style == 1:                             # 邊權 1..2，大量平手
        emit(n, [rand_edge(n, lambda: random.randint(1, 2)) for _ in range(m)])
    elif style == 2:                             # 鏈加上重邊：路徑數相乘
        e = [(i, i + 1, 1) for i in range(1, n)]
        e += [random.choice(e) for _ in range(random.randint(1, 5))]
        e += [rand_edge(n, lambda: random.randint(1, 4)) for _ in range(random.randint(0, 3))]
        emit(n, e)
    elif style == 3:                             # 大邊權，最短距離超過 int
        e = [(i, i + 1, W) for i in range(1, n)]
        e += [rand_edge(n, lambda: W) for _ in range(random.randint(0, 4))]
        emit(n, e)
    else:                                        # 一般隨機
        emit(n, [rand_edge(n, lambda: random.randint(1, 5)) for _ in range(m)])
elif size == "mid":
    if seed % 2 == 1:                            # 約 2000 個點的方格，邊權 1 或 1..2：路徑數很大，要取餘數
        R, C = [(40, 50), (25, 80)][seed // 2 % 2]
        emit(R * C, grid(R, C, lambda: 1 if seed == 1 else random.choice([1, 1, 2])))
    else:                                        # 隨機圖，邊權 1..3
        n = 2000
        emit(n, [rand_edge(n, lambda: random.randint(1, 3)) for _ in range(6000)])
else:
    n, m = 100000, 200000
    style = (seed - 1) % 5
    if style == 0:                               # 每層 2 個點、相鄰兩層全連：路徑數約 2⁵⁰⁰⁰⁰，要取餘數
        L = (n - 2) // 2                         # 層數
        node = lambda a, j: 2 + 2 * a + j       # 第 a 層第 j 個點
        e = [(1, node(0, 0), 1), (1, node(0, 1), 1), (node(L - 1, 0), n, 1), (node(L - 1, 1), n, 1)]
        for a in range(L - 1):
            for j in range(2):
                for k in range(2):
                    e.append((node(a, j), node(a + 1, k), 1))
        while len(e) < m:                        # 補幾條重邊
            e.append(random.choice(e))
        emit(n, e)
    elif style == 1:                             # 長鏈每段兩條 10⁹ 的重邊：距離約 10¹⁴，路徑數 2⁹⁹⁹⁹⁹
        e = []
        for i in range(1, n):
            e += [(i, i + 1, W), (i, i + 1, W)]
        emit(n, e)
    elif style == 2:                             # 點 n 孤立，走不到（答案 −1）
        emit(n, [rand_edge(n - 1, lambda: random.randint(1, W)) for _ in range(m)])
    elif style == 3:                             # 隨機圖，邊權到 10⁹
        emit(n, [rand_edge(n, lambda: random.randint(1, W)) for _ in range(m)])
    else:                                        # 250 × 400 方格，邊權 1 或 2：大量平手
        emit(n, grid(250, 400, lambda: random.choice([1, 1, 1, 2])))
