"""範例 3-A 負環偵測的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 6），max 用題目上限並依 seed 換不同形狀。
題目沒說可以有自環或重邊，所以一律產生簡單有向圖。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 邊權絕對值上限


def emit(n, edges):
    """印出一筆測資：n 個點、edges 是 (u, v, w) 的清單"""
    print(n, len(edges))
    print("\n".join(f"{u} {v} {w}" for u, v, w in edges))


def pick_pairs(n, m, ok=lambda u, v: True):
    """隨機挑至多 m 個不同的有向點對 (u, v)，u ≠ v，且 ok(u, v) 成立"""
    cand = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v and ok(u, v)]
    random.shuffle(cand)
    return cand[:m]


def pick_pairs_big(n, m, ok=lambda u, v: True, used=None):
    """大圖用：反覆抽樣直到湊滿 m 個不重複點對"""
    used = set() if used is None else used
    res = []
    while len(res) < m:
        u, v = random.randint(1, n), random.randint(1, n)
        if u != v and (u, v) not in used and ok(u, v):
            used.add((u, v))
            res.append((u, v))
    return res


def potential_weights(pairs, n, spread):
    """用位能 p 產生邊權 w = c + p[u] − p[v]（c ≥ 0），保證沒有負環但有很多負邊"""
    p = [random.randint(0, spread) for _ in range(n + 1)]
    out = []
    for u, v in pairs:
        lo = max(0, -W - p[u] + p[v])
        hi = max(lo, min(spread, W - p[u] + p[v]))
        out.append((u, v, random.randint(lo, hi) + p[u] - p[v]))
    return out


if size == "small":
    style = seed % 6
    n = random.randint(2, 6)
    full = n * (n - 1)                           # 簡單有向圖最多幾條邊
    m = random.randint(min(full, n), min(12, full))
    if style == 0:                               # 沒有邊；seed 6 是 n = 1 的最小情況
        emit(1 if seed == 6 else n, [])
    elif style == 1:                             # 隨機正負邊權，再埋一個點 1 走得到、總和為負的環
        maxw = random.choice([3, 6, W])
        cyc = random.sample(range(1, n + 1), random.randint(2, n))    # 環上的點依序
        planted = {(cyc[i], cyc[(i + 1) % len(cyc)]): random.randint(-maxw, maxw) for i in range(len(cyc))}
        last = (cyc[-1], cyc[0])
        planted[last] = 0
        planted[last] = max(-maxw, -sum(planted.values()) - random.randint(1, 3))   # 盡量讓環的總和 < 0
        if 1 not in cyc:                         # 補一條從點 1 進入環的邊
            planted[(1, cyc[0])] = random.randint(-maxw, maxw)
        rest = [p for p in pick_pairs(n, m) if p not in planted]
        edges = [(u, v, w) for (u, v), w in planted.items()] + [(u, v, random.randint(-maxw, maxw)) for u, v in rest]
        random.shuffle(edges)
        emit(n, edges)
    elif style == 2:                             # 位能法：有負邊但沒有負環
        spread = random.choice([3, 10, W // 2])
        emit(n, potential_weights(pick_pairs(n, m), n, spread))
    elif style == 3:                             # 負環在點 1 走不到的地方：不能誤判
        n = max(n, 3)
        k = random.randint(2, n - 1)             # 點 1..k 是點 1 走得到的部分，k+1..n 走不到
        pairs = pick_pairs(n, 14, lambda u, v: not (u <= k < v))
        emit(n, [(u, v, random.randint(-5, 2) if u > k else random.randint(0, 5)) for u, v in pairs])
    elif style == 4:                             # 有些點到不了，邊權全為 −10⁹ 的 DAG（u < v）
        pairs = pick_pairs(n, m, lambda u, v: u < v and random.random() < 0.7)
        emit(n, [(u, v, -W) for u, v in pairs])
    else:                                        # 小環藏在鏈的尾端，總和為 0（不是負環）或 −1
        edges = [(i, i + 1, random.randint(0, 4)) for i in range(1, n)]
        edges.append((n, n - 1, -edges[-1][2] - (seed // 6) % 2))
        random.shuffle(edges)
        emit(n, edges)
elif size == "mid":
    n, m = 1000, 5000
    style = seed % 3
    if style == 1:                               # 位能法，沒有負環
        emit(n, potential_weights(pick_pairs_big(n, m), n, W // 2))
    elif style == 2:                             # 隨機正負邊權，幾乎一定有可達負環
        emit(n, [(u, v, random.randint(-W, W)) for u, v in pick_pairs_big(n, m)])
    else:                                        # 後半的點走不到，裡面通常有負環
        k = n // 2
        pairs = pick_pairs_big(n, m, lambda u, v: not (u <= k < v))
        emit(n, [(u, v, random.randint(-W, W) if u > k else random.randint(0, W)) for u, v in pairs])
else:
    n, m = 2500, 5000
    style = (seed - 1) % 5
    if style == 0:                               # 位能法隨機圖：很多負邊但沒有負環
        emit(n, potential_weights(pick_pairs_big(n, m), n, W // 2))
    elif style == 1:                             # 長鏈 1→2→…→n 邊權約 −10⁹、倒序給邊，要跑滿 n−1 輪，距離約 −2.5×10¹²
        chain = [(i, i + 1, -random.randint(W - 10**6, W)) for i in range(1, n)]
        used = {(u, v) for u, v, _ in chain}
        extra = [(u, v, random.randint(-W, W)) for u, v in pick_pairs_big(n, m - len(chain), lambda u, v: u < v, used)]
        edges = extra + chain[::-1]
        emit(n, edges)
    elif style == 2:                             # 鏈尾端才有負環（總和 −1），倒序給邊，第 n 輪才發現
        chain = [(i, i + 1, random.randint(1, W - 1)) for i in range(1, n)]
        back = (n, n - 1, -chain[-1][2] - 1)
        used = {(u, v) for u, v, _ in chain} | {(n, n - 1)}
        extra = [(u, v, W) for u, v in pick_pairs_big(n, m - n, lambda u, v: True, used)]
        emit(n, [back] + extra + chain[::-1])
    elif style == 3:                             # 走不到的那一半全是 −10⁹ 的負環，不檢查 INF 會誤判
        k = n // 2
        chain = [(i, i + 1, W) for i in range(1, k)]                         # 點 1..k 走得到
        cyc = [(i, i + 1 if i < n else k + 1, -W) for i in range(k + 1, n + 1)]   # k+1..n 繞成一個負環
        used = {(u, v) for u, v, _ in chain + cyc}
        rest = pick_pairs_big(n, m - len(chain) - len(cyc), lambda u, v: not (u <= k < v), used)
        extra = [(u, v, -W if u > k else W) for u, v in rest]
        edges = chain[::-1] + cyc + extra
        random.shuffle(edges)
        emit(n, edges)
    else:                                        # 邊權全是 10⁹ 的長鏈加隨機邊：大量相同邊權，距離約 2.5×10¹²
        chain = [(i, i + 1, W) for i in range(1, n)]
        used = {(u, v) for u, v, _ in chain}
        extra = [(u, v, W) for u, v in pick_pairs_big(n, m - len(chain), lambda u, v: v < u, used)]
        emit(n, chain[::-1] + extra)
