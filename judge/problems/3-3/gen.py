"""實作 3-3 救護車路線的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7、m ≤ 14），max 用題目上限並依 seed 換不同形狀。
題目允許重複道路與自環。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 道路時間上限


def emit(n, s, t, edges):
    """印出一筆測資：n 個路口、醫院 s、災區 t、edges 是 (u, v, w) 的清單"""
    print(n, len(edges), s, t)
    print("\n".join(f"{u} {v} {w}" for u, v, w in edges))


if size == "small":
    style = seed % 4
    n = random.randint(2, 7)
    s, t = random.sample(range(1, n + 1), 2)
    E = []
    if style == 0:                               # 完全隨機：可能有自環、重邊、到不了 t、m = 0
        maxw = random.choice([1, 2, 3, W])
        for _ in range(0 if seed == 4 else random.randint(0, 10)):
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, maxw)))
    elif style == 1:                             # 分層：跨一或兩層的邊權等於層差，大量平手
        layer = {v: random.randint(1, 3) for v in range(1, n + 1)}
        layer[s], layer[t] = 0, 4
        for _ in range(random.randint(4, 14)):
            u, v = random.randint(1, n), random.randint(1, n)
            d = layer[v] - layer[u]
            E.append((u, v, d if d in (1, 2) and random.random() < 0.85 else random.randint(1, 3)))
    else:                                        # 埋幾條長度都是 L 的 s→t 路線，再加雜訊邊與完全重複的邊
        L = random.randint(2, 6)
        others = [v for v in range(1, n + 1) if v not in (s, t)]
        for _ in range(random.randint(1, 4)):
            k = random.randint(0, min(len(others), L - 1))
            seq = [s] + random.sample(others, k) + [t]
            cuts = sorted(random.sample(range(1, L), len(seq) - 2))
            parts = [b - a for a, b in zip([0] + cuts, cuts + [L])]
            for i in range(len(seq) - 1):
                E.append((seq[i], seq[i + 1], parts[i]))
        for _ in range(random.randint(0, 4)):
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, 4)))
        if random.random() < 0.3:
            E.append(random.choice(E))
        random.shuffle(E)
        E = E[:14]
    emit(n, s, t, E)
elif size == "mid":
    n = 2000
    s, t = 1, n
    E = []
    if seed % 2 == 1:                            # 鏈加跨兩站的邊；雜訊邊跨 d 站時間至少 d·Wm，不會比鏈快但可能一樣快
        Wm = random.choice([1, 2, 3])
        for v in range(1, n):
            E.append((v, v + 1, random.randint(1, Wm)))
            if random.random() < 0.5:
                E.append((v, min(n, v + 2), random.randint(1, 2 * Wm)))
        for _ in range(3000):
            u, v = random.randint(1, n), random.randint(1, n)
            E.append((u, v, max(1, (v - u) * Wm) + random.randint(0, 1)))
    else:                                        # 分層圖：只連到下一層、邊權 1 或 2，再加少量雜訊，ALL、SOME、NONE 都有
        Wd = random.randint(2, 5)                # 每層寬度
        L = (n - 2) // Wd
        node = lambda a, j: 2 + a * Wd + j
        for j in range(Wd):
            E.append((s, node(0, j), random.randint(1, 2)))
            E.append((node(L - 1, j), t, random.randint(1, 2)))
        for a in range(L - 1):
            for _ in range(random.randint(1, Wd + 1)):
                E.append((node(a, random.randrange(Wd)), node(a + 1, random.randrange(Wd)), random.randint(1, 2)))
            E.append((node(a, 0), node(a + 1, 0), 2))      # 保證每層都接得下去
        for _ in range(500):
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, W)))
    random.shuffle(E)
    emit(n, s, t, E)
else:
    n, m = 100000, 200000
    style = (seed - 1) % 5
    E = []
    s, t = 1, n
    if style == 0:                               # 隨機圖，s、t 隨機
        s, t = random.sample(range(1, n + 1), 2)
        for _ in range(m):
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, W)))
    elif style == 1:                             # 1 → 2 → … → n 全是 10⁹：距離約 10¹⁴，鏈上每條都是 ALL
        for i in range(1, n):
            E.append((i, i + 1, W))
        while len(E) < m:
            u = random.randint(2, n)
            E.append((u, random.randint(1, u - 1), W))
    elif style == 2:                             # 每層 4 個點、邊權 1 只連到下一層：每條邊都在某條最短路上
        Wd = 4
        L = (n - 2) // Wd
        node = lambda a, j: 2 + a * Wd + j
        for j in range(Wd):
            E.append((s, node(0, j), 1))
            E.append((node(L - 1, j), t, 1))
        for a in range(L - 1):
            for j in range(Wd):
                E.append((node(a, j), node(a + 1, j), 1))
        E.append((node(L // 2, 0), node(L // 2 + 1, 0), 1))   # 一條完全重複的邊
        while len(E) < m:
            a = random.randint(0, L - 2)
            E.append((node(a, random.randrange(Wd)), node(a + 1, random.randrange(Wd)), 1))
    elif style == 3:                             # 單一道路與「兩條等長平行路線」交替出現
        v, nxt = 1, 2
        while nxt + 3 <= n and len(E) + 5 <= m:
            a, b, c = nxt, nxt + 1, nxt + 2
            E += [(v, a, 5), (a, b, 3), (b, c, 4), (a, c, 7)]
            v = c
            nxt += 3
        E.append((v, t, 1))
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), W))
    else:                                        # 相鄰樞紐間有兩條等長路線，每 1000 段才有一段只有單一道路（ALL）
        cur, nxt = 1, 2
        while nxt + 2 <= n - 1 and len(E) + 4 <= m - 1:
            a, b, c = nxt, nxt + 1, nxt + 2
            if (nxt // 3) % 1000 == 0:
                E.append((cur, c, 2))
            else:
                E += [(cur, a, 1), (a, c, 1), (cur, b, 1), (b, c, 1)]
            cur = c
            nxt += 3
        E.append((cur, t, 1))
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, W)))
    random.shuffle(E)
    emit(n, s, t, E)
