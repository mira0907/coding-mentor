"""實作 5-3 單車路線的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7），max 用題目上限並依 seed 換不同形狀。
題目允許自環與重複的車道。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 個地點、edges 是 (u, v) 車道的清單（先打亂順序）"""
    random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{u} {v}" for u, v in edges))


def route_order(n):
    """回傳地點的排列：1 在最前、n 在最後，中間打亂；順著它加邊就是往終點走"""
    mid = list(range(2, n))
    random.shuffle(mid)
    return [1] + mid + ([n] if n > 1 else [])


if size == "small":
    n = 1 if seed in (1, 2) else random.randint(2, 7)
    mode = seed % 7
    m = 0 if mode == 0 else random.randint(1, 14)
    perm = route_order(n)
    edges = []
    if seed == 1:                                # n = 1、沒有車道：什麼都不騎也算一條，答案 1
        edges = []
    elif seed == 2:                              # n = 1 加一條自環：無限多條
        edges = [(1, 1)]
    else:
        for _ in range(m):
            if mode in (1, 2, 3) and n >= 2:     # 順向邊為主；偶爾加反向邊或自環，環在不在路線上都有
                i, j = sorted(random.sample(range(n), 2))
                a, b = perm[i], perm[j]
                r = random.random()
                if mode == 2 and r < 0.12:
                    a, b = b, a
                elif mode == 3 and r < 0.1:
                    b = a
            elif mode == 4 and n >= 2:           # 純 DAG，常有重複的車道
                i, j = sorted(random.sample(range(n), 2))
                a, b = perm[i], perm[j]
                if random.random() < 0.3:
                    edges.append((a, b))
            elif mode == 5 and n >= 3:           # 順向邊，但不從死路點 dead 出發（dead 在下面設定）
                i, j = sorted(random.sample(range(n), 2))
                a, b = perm[i], perm[j]
                if a == perm[1]:
                    continue
            else:                                # 完全隨機
                a, b = random.randint(1, n), random.randint(1, n)
            edges.append((a, b))
        if mode == 5 and n >= 3:                 # dead = perm[1] 只有自環：從 1 走得到、卻到不了 n 的環，答案仍有限
            dead = perm[1]
            edges += [(dead, dead), (1, dead), (1, n)]
    emit(n, edges)
elif size == "mid":
    n = 2000
    perm = route_order(n)
    main, side = perm[:-1][:1900] + [n], perm[1900:-1]   # main = 主幹（1 … n），side = 旁邊 99 個點
    edges = [(main[i], main[i + 1]) for i in range(len(main) - 1)]
    while len(edges) < 4900:                     # 主幹上往後短跳的順向邊
        i = random.randrange(len(main) - 1)
        edges.append((main[i], main[min(len(main) - 1, i + random.randint(1, 6))]))
    edges += [(side[i], side[(i + 1) % len(side)]) for i in range(len(side))]   # side 自成一個環
    x, y = random.sample(main[1:-1], 2)          # 主幹上的兩個點
    if seed % 4 == 2:                            # 主幹 → 環：環到不了 n，答案有限
        edges.append((x, side[0]))
    elif seed % 4 == 3:                          # 主幹 → 環 → 主幹：環在路線上 → INFINITE
        edges += [(x, side[0]), (side[1], y)]
    elif seed % 4 == 0:                          # 環 → 主幹：從 1 走不到環，答案有限
        edges.append((side[0], y))
    emit(n, edges)
else:
    MOD = 10**9 + 7
    shape = (seed - 1) % 6
    edges = []
    if shape == 0:                               # 每段兩條重複車道的長鏈：答案 2^(n-1) 取餘數
        n = 100001
        for i in range(1, n):
            edges += [(i, i + 1), (i, i + 1)]
    elif shape == 1:                             # i → i+1、i → i+2：費氏數列，要記得取餘數
        n = 100001
        for i in range(1, n):
            edges.append((i, i + 1))
            if i + 2 <= n:
                edges.append((i, i + 2))
    elif shape == 2:                             # 長鏈 1 → … → half → n，點 2 通往一個到不了 n 的大環：答案 1
        n, half = 200000, 100000
        edges = [(i, i + 1) for i in range(1, half)] + [(half, n)]
        edges += [(i, i + 1) for i in range(half + 1, n - 1)] + [(n - 1, half + 1), (2, half + 1)]
    elif shape == 3:                             # 從 1 走不到的大環指向鏈上：答案 1
        n, half = 200000, 100000
        edges = [(i, i + 1) for i in range(1, half)] + [(half, n)]
        edges += [(i, i + 1) for i in range(half + 1, n - 1)] + [(n - 1, half + 1), (n - 1, 5)]
    elif shape == 4:                             # 長鏈走到 n，n 有自環：可以在終點一直繞 → INFINITE
        n = 200000
        edges = [(i, i + 1) for i in range(1, n)] + [(n, n)]
    else:                                        # 隨機 DAG，主幹加往後短跳的邊（編號打亂）
        n = 100000
        perm = route_order(n)
        edges = [(perm[i], perm[i + 1]) for i in range(n - 1)]
        while len(edges) < 200000:
            i = random.randrange(n - 1)
            edges.append((perm[i], perm[min(n - 1, i + random.randint(1, 5))]))
    emit(n, edges)
