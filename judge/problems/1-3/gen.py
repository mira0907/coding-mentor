"""實作 1-3 停駛的渡輪的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
停駛紀錄可能重複、可能正反寫，但 u ≠ v。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges, shuffle=True):
    """印出一筆測資：n 座島、edges 是停駛的 (u, v) 清單，兩端隨機對調"""
    if shuffle:
        random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{u} {v}" if random.random() < 0.5 else f"{v} {u}" for u, v in edges))


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 8)
    pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    mode = seed % 4
    if mode == 0:                                # 分成幾組，跨組全部停駛：很多航運圈
        g = [random.randint(0, 2) for _ in range(n + 1)]
        chosen = [p for p in pairs if g[p[0]] != g[p[1]] or random.random() < 0.4]
    elif mode == 1:                              # 大部分停駛
        chosen = [p for p in pairs if random.random() < 0.85]
    elif mode == 2:                              # 少數停駛
        chosen = [p for p in pairs if random.random() < 0.3]
    else:                                        # 全部停駛（每島自成一圈）或只剩一條
        chosen = pairs[:]
        if pairs and random.random() < 0.5:
            chosen.remove(random.choice(pairs))
    edges = []
    for p in chosen:
        edges.append(p)
        if random.random() < 0.2:                # 重複的停駛紀錄
            edges.append(p)
    emit(n, edges)
elif size == "mid":
    n = 2000
    sizes = [random.randint(1, 4) for _ in range(random.randint(2, 6))]   # 幾個小航運圈的大小
    grp = []                                     # grp[i] = 第 i + 1 座島屬於哪一組，0 是大組
    for k, s in enumerate(sizes, 1):
        grp += [k] * s
    grp += [0] * (n - len(grp))
    random.shuffle(grp)
    grp = [None] + grp
    edges = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if grp[u] != grp[v]]
    extra = 0                                    # 同組內再隨機停駛 5000 條（小組可能因此再分裂）
    while extra < 5000:
        u, v = random.sample(range(1, n + 1), 2)
        if grp[u] == grp[v] and (grp[u] == 0 or random.random() < 0.05):
            edges.append((u, v))
            extra += 1
    edges += random.sample(edges, 2000)          # 重複紀錄
    emit(n, edges)
else:
    kind = seed % 6
    edges = []
    if kind == 1:                                # 星形：島 1 和其他所有島都停駛，n = 2×10⁵，答案 1 與 199999
        n = 200000
        edges = [(1, v) for v in range(2, n + 1)]
    elif kind == 2:                              # 632 座島兩兩全部停駛：632 個單島航運圈
        n = 632
        edges = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    elif kind == 3:                              # 隨機停駛，n = m = 2×10⁵，全部同一圈
        n = 200000
        while len(edges) < 200000:
            u, v = random.randint(1, n), random.randint(1, n)
            if u != v:
                edges.append((u, v))
    elif kind == 4:                              # 400 座和 500 座之間全部停駛：補圖是兩個完全圖
        n = 900
        edges = [(u, v) for u in range(1, 401) for v in range(401, 901)]
    elif kind == 5:                              # 前 447 座島兩兩停駛，n = 2×10⁵
        n = 200000
        edges = [(u, v) for u in range(1, 448) for v in range(u + 1, 448)]
    else:                                        # 星形每條都記兩次（正反各一）：重複紀錄塞滿 m
        n = 100001
        edges = [(1, v) for v in range(2, n + 1)] * 2
    emit(n, edges)
