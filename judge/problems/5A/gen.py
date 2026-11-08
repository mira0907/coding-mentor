"""範例 5-A 字典序最小選課的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7），max 用題目上限並依 seed 換不同形狀。
題目沒說可以有自環或重複的關係，所以都不產生。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：n 門課、edges 是 (a, b) 先修關係的清單（先打亂順序）"""
    random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{a} {b}" for a, b in edges))


def dag_edges(perm, m, have=None, span=None):
    """依 perm 的順序加不重複的順向邊（perm 中前面 → 後面），直到共 m 條；span = 往後最多跳幾格（None 表示不限）"""
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


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 7)
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    mode = seed % 5
    if mode == 0:                                # 沒有先修關係：答案是 1 2 … n
        edges = []
    elif mode == 1:                              # 隨機 DAG
        edges = list(dag_edges(perm, random.randint(1, 10)))
    elif mode == 2:                              # DAG 再加一條反向邊，常常出現環 → IMPOSSIBLE
        edges = list(dag_edges(perm, random.randint(1, 8)))
        if n >= 2:
            i, j = sorted(random.sample(range(n), 2))
            edges.append((perm[j], perm[i]))
    elif mode == 3:                              # 編號大的課當先修，最小字典序和一般拓撲序差很多
        perm = list(range(n, 0, -1))
        edges = list(dag_edges(perm, random.randint(0, 6)))
    else:                                        # 完全隨機的邊（不重複、無自環），可能有環
        s = set()
        for _ in range(random.randint(0, 9)):
            a, b = random.randint(1, n), random.randint(1, n)
            if a != b and (b, a) not in s:
                s.add((a, b))
        if seed % 2 == 0 and n >= 2:             # 偶爾放一個二元環
            a, b = random.sample(range(1, n + 1), 2)
            s.discard((a, b)); s.discard((b, a))
            s |= {(a, b), (b, a)}
        edges = list(s)
    emit(n, edges)
elif size == "mid":
    n, m = 2000, 6000
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    edges = list(dag_edges(perm, m))
    if seed % 4 == 0:                            # 加一條反向邊造出環 → IMPOSSIBLE
        edges[0] = (perm[n - 1], perm[0])
        edges.append((perm[0], perm[n // 2]))
        edges.append((perm[n // 2], perm[n - 1]))
        edges = list(dict.fromkeys(edges))
    emit(n, edges)
else:
    n, m = 100000, 200000
    shape = (seed - 1) % 5
    if shape == 0:                               # 隨機 DAG，編號打亂
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        edges = list(dag_edges(perm, m))
    elif shape == 1:                             # 長鏈 n → n-1 → … → 1 再加順向邊：答案 n n-1 … 1
        perm = list(range(n, 0, -1))
        have = {(i + 1, i) for i in range(1, n)}
        edges = list(dag_edges(perm, m, have))
    elif shape == 2:                             # 星形：課 n 是其他所有課的先修，之後一次有很多課可選
        perm = list(range(1, n))
        random.shuffle(perm)
        have = {(n, i) for i in range(1, n)}
        edges = list(dag_edges(perm, m, have))
    elif shape == 3:                             # 大環 1 → 2 → … → n → 1：一開始就沒有課能修
        have = {(i, i + 1) for i in range(1, n)}
        perm = list(range(1, n + 1))
        edges = list(dag_edges(perm, m - 1, have)) + [(n, 1)]
    else:                                        # 隨機 DAG，只在拓撲序最後面藏一個小環 → IMPOSSIBLE
        perm = list(range(1, n + 1))
        random.shuffle(perm)
        a, b = perm[-2], perm[-1]
        edges = list(dag_edges(perm, m - 1, {(a, b)})) + [(b, a)]
    emit(n, edges)
