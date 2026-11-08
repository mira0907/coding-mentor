"""實作 5-1 卡住的關卡的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
題目允許重複的規則和 a = b（自環）。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 個關卡、edges 是 (a, b) 規則的清單"""
    print(n, len(edges))
    if edges:
        print("\n".join(f"{a} {b}" for a, b in edges))


def forward(perm):
    """依 perm 的順序隨機挑一條順向邊（perm 中前面 → 後面）"""
    i, j = sorted(random.sample(range(len(perm)), 2))
    return perm[i], perm[j]


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 8)
    mode = seed % 6
    m = 0 if mode == 0 else random.randint(1, 12)
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    edges = []
    if seed == 1:                                # n = 1 加一條自環：唯一的關卡卡住
        edges = [(1, 1)]
    elif mode in (1, 2):                         # 大多是 DAG 邊，偶爾一條反向邊或自環
        for _ in range(m):
            a, b = forward(perm)
            r = random.random()
            if r < 0.12:
                a, b = b, a
            elif r < 0.18:
                b = a
            edges.append((a, b))
    elif mode == 3:                              # 純 DAG：全部都能通過
        edges = [forward(perm) for _ in range(m)]
    elif mode == 4:                              # 純 DAG，但很多重複的規則
        for _ in range(m):
            e = forward(perm)
            edges += [e] * random.randint(1, 3)
    elif mode == 5:                              # 完全隨機
        edges = [(random.randint(1, n), random.randint(1, n)) for _ in range(m)]
    random.shuffle(edges)
    emit(n, edges)
elif size == "mid":
    n, m = 2000, 4000
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    edges = [(perm[i], perm[i + 1]) for i in range(n - 1) if random.random() < 0.85]   # 有缺口的主幹
    while len(edges) < m:                        # 只往後跳 1～3 格的順向邊，路徑很長
        i = random.randrange(n - 1)
        edges.append((perm[i], perm[min(n - 1, i + random.randint(1, 3))]))
    for _ in range(seed - 1):                    # 加 seed - 1 條短的反向邊，卡住的範圍由小到大
        i = random.randrange(n // 2, n - 60)
        edges.append((perm[i + random.randint(5, 50)], perm[i]))
    random.shuffle(edges)
    emit(n, edges)
else:
    n = m = 200000
    shape = (seed - 1) % 5
    if shape == 0:                               # 長鏈 1 → 2 → … → n：全部能通過，答案 0
        edges = [(i, i + 1) for i in range(1, n)]
        edges.append((1, n))
    elif shape == 1:                             # 大環：全部卡住
        edges = [(i, i % n + 1) for i in range(1, n + 1)]
    elif shape == 2:                             # 關卡 1 自環，1 是所有關卡的前置：全部卡住
        edges = [(1, 1)] + [(1, v) for v in range(2, n + 1)]
    elif shape == 3:                             # 隨機 DAG 加一條反向邊：一部分卡住
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        edges = [forward(perm) for _ in range(m - 1)]
        a, b = forward(perm)
        edges.append((b, a))
    else:                                        # 每條規則重複兩次的長鏈，中間一個關卡自環
        half = n // 2
        edges = []
        for i in range(1, half):
            edges += [(i, i + 1), (i, i + 1)]
        edges.append((half // 2, half // 2))
        edges.append((half, half + 1))
    random.shuffle(edges)
    emit(n, edges)
