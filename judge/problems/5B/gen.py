"""範例 5-B 可達點計數的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
保證無環；題目沒說可以有重邊，所以不產生重邊。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 個點、edges 是 (a, b) 有向邊的清單（先打亂順序）"""
    edges = list(edges)
    random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{a} {b}" for a, b in edges))


def dag_edges(perm, m, have=None, span=None):
    """依 perm 的順序加不重複的順向邊，直到共 m 條；span = 往後最多跳幾格（None 表示不限）"""
    n = len(perm)
    s = set() if have is None else have
    pos = {v: i for i, v in enumerate(perm)}                      # pos[v] = v 在 perm 中的位置
    reach = n - 1 if span is None else span                         # 最多往後跳幾格
    ok = lambda a, b: a in pos and b in pos and 0 < pos[b] - pos[a] <= reach
    total = sum(min(reach, n - 1 - i) for i in range(n))            # 可以加的順向邊總數
    m = min(m, len(s) + total - sum(1 for a, b in s if ok(a, b)))   # 邊不夠時就少給幾條
    while len(s) < m:
        i = random.randrange(n)
        j = random.randrange(n) if span is None else i + random.randint(1, span)
        if i != j and j < n:
            s.add((perm[min(i, j)], perm[max(i, j)]))
    return s


def shuffled(n):
    """回傳打亂過的 1..n，當作拓撲序"""
    p = list(range(1, n + 1))
    random.shuffle(p)
    return p


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 8)
    perm = shuffled(n)
    mode = seed % 5
    if mode == 0:                                # 沒有邊：每個點都是 1
        edges = set()
    elif mode == 1:                              # 隨機 DAG
        edges = dag_edges(perm, random.randint(1, 14))
    elif mode == 2:                              # 完全 DAG（任兩點都有邊）
        edges = dag_edges(perm, n * (n - 1) // 2)
    elif mode == 3:                              # 長鏈再加幾條捷徑，有很多菱形（同一點有多條路可到）
        edges = dag_edges(perm, n - 1 + random.randint(0, 4), {(perm[i], perm[i + 1]) for i in range(n - 1)})
    else:                                        # 稀疏、常不連通
        edges = dag_edges(perm, random.randint(0, n // 2))
    emit(n, edges)
elif size == "mid":
    n, m = 2000, 6000
    emit(n, dag_edges(shuffled(n), m, span=None if seed % 2 else 30))
else:
    n, m = 30000, 100000
    shape = (seed - 1) % 4
    perm = shuffled(n)
    if shape == 0:                               # 隨機 DAG：多數點能到很多點
        edges = dag_edges(perm, m)
    elif shape == 1:                             # 長鏈加短跳躍邊：可達點數 n, n-1, …，路徑數爆炸
        edges = dag_edges(perm, m, {(perm[i], perm[i + 1]) for i in range(n - 1)}, span=5)
    elif shape == 2:                             # 起點 perm[0] 指向所有點，其餘是只往後跳一點點的 DAG
        have = {(perm[0], perm[i]) for i in range(1, n)}
        edges = dag_edges(perm, m, have, span=20)
    else:                                        # 前一半是長鏈，後一半每點連到鏈上隨機三個點
        half = n // 2
        edges = {(perm[i], perm[i + 1]) for i in range(half - 1)}
        for i in range(half, n):
            for k in random.sample(range(half), 3):
                edges.add((perm[i], perm[k]))
        edges = dag_edges(perm[half:], m, edges)  # 後一半之間再補順向邊到 m 條
    emit(n, edges)
