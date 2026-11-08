"""範例 3-B 優惠券航線的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7），max 用題目上限並依 seed 換不同形狀。
題目沒說可以有自環或重複航線，所以一律產生簡單無向圖。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 票價上限


def emit(n, K, edges):
    """印出一筆測資：n 座城市、K 張優惠券、edges 是 (u, v, w) 的清單（順序與方向打亂）"""
    random.shuffle(edges)
    print(n, len(edges), K)
    print("\n".join(f"{u} {v} {w}" if random.random() < 0.5 else f"{v} {u} {w}" for u, v, w in edges))


def small_pairs(n, m, ok=lambda u, v: True, used=()):
    """小圖：從所有點對裡隨機挑 m 條不重複的無向邊 (u, v)，u < v"""
    cand = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if (u, v) not in used and ok(u, v)]
    random.shuffle(cand)
    return cand[:m]


def local_graph(n, m, D, wf, chain_w=None):
    """大圖：只連相距 1 到 D 的城市，從 1 到 n 要飛很多段。
    chain_w 有給時先放整條 1–2–…–n 的鏈（票價 chain_w()），保證連通。wf() 產生其他航線的票價。"""
    edges, used = [], set()
    if chain_w:
        for i in range(1, n):
            edges.append((i, i + 1, chain_w()))
            used.add((i, i + 1))
    while len(edges) < m:
        u = random.randint(1, n - 1)
        v = min(n, u + random.randint(1, D))
        if (u, v) not in used:
            used.add((u, v))
            edges.append((u, v, wf()))
    return edges


if size == "small":
    style = seed % 5
    n = random.randint(2, 7)
    K = random.choice([0, 1, 1, 2, 2, 3, 10])
    full = n * (n - 1) // 2                      # 簡單無向圖最多幾條邊
    m = random.randint(min(full, n - 1), min(10, full))
    if style == 0:                               # 城市 n 和城市 1 不連通（答案 −1）；seed 5 是 n = 2、沒有航線
        if seed == 5:
            n, m = 2, 0
        k = random.randint(1, n - 1)             # 1..k 一塊、k+1..n 另一塊
        e = small_pairs(n, m, lambda u, v: (u <= k) == (v <= k))
        emit(n, K, [(u, v, random.randint(1, 20)) for u, v in e])
    elif style == 1:                             # 小票價，很多平手
        emit(n, random.choice([0, 1, 1, 2]), [(u, v, random.randint(1, 3)) for u, v in small_pairs(n, m)])
    elif style == 2:                             # 便宜的長鏈 vs. 貴的捷徑：考驗券要用在哪
        e = [(i, i + 1, random.randint(1, 5)) for i in range(1, n)]
        used = {(u, v) for u, v, _ in e}
        e += [(u, v, random.choice([8, 50, W])) for u, v in small_pairs(n, random.randint(1, 4), used=used)]
        emit(n, random.choice([1, 2]), e)
    elif style == 3:                             # 接近 10⁹ 的票價，答案可能超過 int
        e = [(i, i + 1, random.randint(W - 5, W)) for i in range(1, n)]
        used = {(u, v) for u, v, _ in e}
        e += [(u, v, random.randint(W - 5, W)) for u, v in small_pairs(n, random.randint(0, 3), lambda u, v: v - u >= 2, used)]
        emit(n, random.choice([0, 1]), e)
    else:                                        # 一般隨機
        emit(n, random.choice([0, 1, 1, 2]), [(u, v, random.randint(1, 30)) for u, v in small_pairs(n, m)])
elif size == "mid":
    n, m = 2000, 8000
    K = [3, 10, 0][seed % 3]
    maxw = [W, 10, W][seed % 3]
    emit(n, K, local_graph(n, m, random.choice([5, 20]), lambda: random.randint(1, maxw)))
else:
    n, m = 10000, 50000
    style = (seed - 1) % 5
    if style == 0:                               # 相近城市間的隨機航線，票價到 10⁹，K = 10
        emit(n, 10, local_graph(n, m, 20, lambda: random.randint(1, W)))
    elif style == 1:                             # 長鏈 1–2–…–n 全是 10⁹，捷徑只跨 2..10 站：答案約 10¹²，int 會溢位
        e = local_graph(n, m, 10, lambda: W, lambda: W)
        emit(n, 10, e)
    elif style == 2:                             # 城市 n 在另一個連通塊，答案 −1
        k = n - 50
        e = [(u, v, w) for u, v, w in local_graph(n, m + 2000, 20, lambda: random.randint(1, W))
             if (u <= k) == (v <= k)][:m]
        emit(n, 10, e)
    elif style == 3:                             # 票價全相同：大量平手
        emit(n, 10, local_graph(n, m, 6, lambda: 7))
    else:                                        # 沒有優惠券（K = 0）：長鏈加跨站捷徑，票價都很大
        e = local_graph(n, m, 30, lambda: W, lambda: random.randint(W // 2, W))
        emit(n, 0, e)
