"""實作 4-1 修路計畫的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
題目允許重複道路與自環。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 座城市、edges 是 (u, v) 的清單"""
    print(n, len(edges))
    print("\n".join(f"{u} {v}" for u, v in edges))


if size == "small":
    style = seed % 4
    n = random.randint(2, 8)
    if seed == 4:                                # 只有一座城市、沒有道路（答案 0）
        emit(1, [])
    elif seed == 8:                              # 沒有道路（答案 n − 1）
        emit(n, [])
    elif style == 1:                             # 隨機邊，含自環與重複道路
        emit(n, [(random.randint(1, n), random.randint(1, n)) for _ in range(random.randint(0, 12))])
    elif style == 2:                             # 只有自環和重複道路：多出來的邊不能少算連通塊
        e = [(v, v) for v in random.sample(range(1, n + 1), random.randint(1, n))]
        if n >= 2:
            u, v = random.sample(range(1, n + 1), 2)
            e += [(u, v)] * random.randint(1, 4)
        random.shuffle(e)
        emit(n, e)
    elif style == 3:                             # 幾個環：邊數 ≥ n 但不一定連通
        e = []
        k = random.randint(1, n)                 # 前 k 座城市繞成一圈
        e += [(i, i % k + 1) for i in range(1, k + 1)]
        e += [(random.randint(k, n), random.randint(k, n)) for _ in range(random.randint(0, 3))]
        random.shuffle(e)
        emit(n, e)
    else:                                        # 一棵樹加一條邊，再拆掉一些（剛好連通或差幾條）
        e = [(random.randint(1, v - 1), v) for v in range(2, n + 1)]
        random.shuffle(e)
        e = e[:len(e) - random.randint(0, 2)] + [(random.randint(1, n), random.randint(1, n))]
        emit(n, e)
elif size == "mid":
    n = 2000
    m = [1000, 2000, 6000, 1500][seed % 4]       # 邊數小於、約等於、大於 n
    emit(n, [(random.randint(1, n), random.randint(1, n)) for _ in range(m)])
else:
    n, m = 100000, 200000
    style = (seed - 1) % 5
    if style == 0:                               # 先連成 1–2–…–n 的鏈，之後全是 (1, x)：不壓縮路徑的並查集會 TLE
        e = [(i, i + 1) for i in range(1, n)]
        e += [(1, random.randint(1, n)) for _ in range(m - len(e))]
        emit(n, e)
    elif style == 1:                             # 每 7 座城市一塊、塊內隨機連邊（含自環與重邊）：很多連通塊
        blk = lambda: random.randrange(n // 7) * 7
        e = []
        for _ in range(m):
            b = blk()
            e.append((b + random.randint(1, 7), b + random.randint(1, 7)))
        emit(n, e)
    elif style == 2:                             # 星狀，加上自環與重複道路；有一半的城市沒接上
        star = [(1, v) for v in range(2, n // 2 + 1)]
        e = list(star)
        while len(e) < m:
            if random.random() < 0.5:
                v = random.randint(1, n)
                e.append((v, v))                 # 自環
            else:
                e.append(random.choice(star))    # 重複的道路
        random.shuffle(e)
        emit(n, e)
    elif style == 3:                             # 沒有任何道路：答案 n − 1
        emit(n, [])
    else:                                        # 完全隨機
        emit(n, [(random.randint(1, n), random.randint(1, n)) for _ in range(m)])
