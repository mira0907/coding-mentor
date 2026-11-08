"""實作 4-2 颱風天的道路的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
題目允許重複道路與自環。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 耐風等級與颱風等級的上限


def emit(n, edges, queries):
    """印出一筆測資：n 個鄉鎮、edges 是 (u, v, w)、queries 是 (v, x)"""
    print(n, len(edges), len(queries))
    lines = [f"{u} {v} {w}" for u, v, w in edges] + [f"{v} {x}" for v, x in queries]
    print("\n".join(lines))


if size == "small":
    n = 1 if seed == 3 else random.randint(2, 8)   # seed 3 是只有一個鄉鎮的情況
    m = 0 if seed % 10 == 0 else random.randint(1, 12)   # seed 10、20 沒有道路
    q = random.randint(1, 8)
    maxw = random.choice([1, 3, 6, W])
    E = [(random.randint(1, n), random.randint(1, n), random.randint(1, maxw)) for _ in range(m)]
    if maxw < W:                                 # 颱風等級常常剛好等於某條路的耐風等級，也有超過全部的
        Q = [(random.randint(1, n), random.randint(1, maxw + 1)) for _ in range(q)]
    else:                                        # 大數值：颱風等級取某條路的耐風等級、±1 或隨機
        ws = [w for _, _, w in E] or [W]
        Q = [(random.randint(1, n), min(W, max(1, random.choice(ws) + random.choice([-1, 0, 0, 1])))
              if random.random() < 0.7 else random.randint(1, W)) for _ in range(q)]
    emit(n, E, Q)
elif size == "mid":
    n, m, q = 2000, 2000, 2000
    maxw = [10, 1000, W][seed % 3]
    E = [(random.randint(1, n), random.randint(1, n), random.randint(1, maxw)) for _ in range(m)]
    Q = [(random.randint(1, n), random.randint(1, maxw)) for _ in range(q)]
    emit(n, E, Q)
else:
    n, m, q = 100000, 100000, 100000
    style = (seed - 1) % 5
    E, Q = [], []
    if style == 0:                               # 完全隨機
        E = [(random.randint(1, n), random.randint(1, n), random.randint(1, W)) for _ in range(m)]
        Q = [(random.randint(1, n), random.randint(1, W)) for _ in range(q)]
    elif style == 1:                             # 鏈 1–2–…–n、越後面越不耐風：每個颱風等級把鏈切在不同位置
        E = [(i, i + 1, W - i) for i in range(1, n)]
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), 1))
        Q = [(random.randint(1, n), random.randint(W - n, W)) for _ in range(q)]
    elif style == 2:                             # 耐風等級全部相同，颱風等級只有 1、7、8 三種：大量平手
        E = [(random.randint(1, n), random.randint(1, n), 7) for _ in range(m)]
        Q = [(random.randint(1, n), random.choice([1, 7, 8])) for _ in range(q)]
    elif style == 3:                             # 隨機樹加自環與重複道路，每筆詢問都是 x = 1：每次答案都是整張圖
        E = [(random.randint(1, v - 1), v, random.randint(1, W)) for v in range(2, n + 1)]
        while len(E) < m:
            if random.random() < 0.5:
                v = random.randint(1, n)
                E.append((v, v, random.randint(1, W)))
            else:
                E.append(random.choice(E))
        random.shuffle(E)
        Q = [(random.randint(1, n), 1) for _ in range(q)]
    else:                                        # 星狀：中心是 1，葉子的道路耐風等級隨機
        E = [(1, v, random.randint(1, W)) for v in range(2, n + 1)]
        E.append((1, 1, W))
        Q = [(random.randint(1, n), random.randint(1, W)) for _ in range(q)]
    emit(n, E, Q)
