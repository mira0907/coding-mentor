"""實作 4-3 光纖網路的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8、m ≤ 13），max 用題目上限並依 seed 換不同形狀。
一定先放一棵生成樹保證連通；題目允許重複光纖與自環。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 成本上限


def emit(n, edges, relabel=True):
    """印出一筆測資：n 個機房、edges 是 (u, v, w)；順序、方向打亂，relabel 時也把機房重新編號"""
    perm = list(range(1, n + 1))
    if relabel:
        random.shuffle(perm)
    random.shuffle(edges)
    print(n, len(edges))
    out = []
    for u, v, w in edges:
        a, b = perm[u - 1], perm[v - 1]
        if random.random() < 0.5:
            a, b = b, a
        out.append(f"{a} {b} {w}")
    print("\n".join(out))


if size == "small":
    big = seed % 2 == 0                          # 偶數 seed：點多、成本只有 1、2，同成本的大組
    n = random.randint(5, 8) if big else random.randint(2, 6)
    if seed == 1:
        n = 1                                    # 只有一個機房：所有光纖都是自環
    maxw = random.choice([1, 2]) if big else random.choice([1, 2, 3, W])
    cap = 13 if big else 9                       # 最多幾條光纖（暴力解要列舉 C(m, n−1) 種選法）
    E = [(random.randint(1, v - 1), v, random.randint(1, maxw)) for v in range(2, n + 1)]   # 先放一棵樹
    for _ in range(random.randint(0, cap - len(E)) if len(E) < cap else 0):
        r = random.random()
        if r < 0.1:
            x = random.randint(1, n)
            E.append((x, x, random.randint(1, maxw)))           # 自環
        elif r < 0.25 and E:
            E.append(random.choice(E))                          # 完全重複的光纖
        else:
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, maxw)))
    if seed == 1:
        E += [(1, 1, 5), (1, 1, 5)]
    emit(n, E)
elif size == "mid":
    n = 2000
    Wm = [1, 3, 20, W][seed % 4]
    E = [(random.randint(max(1, v - 3), v - 1), v, random.randint(1, Wm)) for v in range(2, n + 1)]
    for _ in range(4000):
        E.append((random.randint(1, n), random.randint(1, n), random.randint(1, Wm)))
    emit(n, E)
else:
    n, m = 100000, 200000
    style = (seed - 1) % 5
    E = []

    def tree(wf):
        """每個點接到前 5 個點之一，形成一棵很深的樹"""
        for v in range(2, n + 1):
            E.append((random.randint(max(1, v - 5), v - 1), v, wf()))

    if style == 0:                               # 成本全部相同：幾乎全是 SOME
        tree(lambda: 1)
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), 1))
    elif style == 1:                             # 成本隨機到 10⁹
        tree(lambda: random.randint(1, W))
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, W)))
    elif style == 2:                             # 成本只有 1..10：很多同成本的組
        tree(lambda: random.randint(1, 10))
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), random.randint(1, 10)))
    elif style == 3:                             # 長鏈 1–2–…–n 成本 1，加上 (i, i+2) 與首尾相連的同成本捷徑，其餘是成本 10⁹ 的 NONE
        for i in range(1, n):
            E.append((i, i + 1, 1))
        for i in range(n - 2, 0, -2):
            if len(E) >= m - 1:
                break
            E.append((i, i + 2, 1))
        E.append((1, n, 1))
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), W))
    else:                                        # 成本 1 的長鏈，只有每 1000 段有一條平行的重複光纖：大多是 ALL
        for i in range(1, n):
            E.append((i, i + 1, 1))
            if i % 1000 == 0:
                E.append((i, i + 1, 1))
        while len(E) < m:
            E.append((random.randint(1, n), random.randint(1, n), 2))
    emit(n, E, relabel=style != 3)
