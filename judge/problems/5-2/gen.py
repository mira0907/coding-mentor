"""實作 5-2 專案排程的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7），max 用題目上限並依 seed 換不同形狀。
題目沒說可以有自環或重複的相依關係，所以都不產生。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
BIG = 10**9                                    # t_i 的上限


def emit(t, edges):
    """印出一筆測資：t 是每項工作的天數、edges 是 (a, b) 相依關係（先打亂順序）"""
    edges = list(edges)
    random.shuffle(edges)
    print(len(t), len(edges))
    print(" ".join(map(str, t)))
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
    n = 1 if seed == 1 else random.randint(2, 7)
    perm = shuffled(n)
    maxt = BIG if seed % 3 == 0 else 5           # 有時用很大的天數
    t = [random.randint(1, maxt) for _ in range(n)]
    mode = seed % 5
    if mode == 0:                                # 沒有相依：答案是最大的 t
        edges = set()
    elif mode == 1:                              # 隨機 DAG
        edges = dag_edges(perm, random.randint(1, 10))
    elif mode in (2, 3):                         # DAG 加一條反向邊；mode 3 先放長鏈，一定有環 → -1
        chain = {(perm[i], perm[i + 1]) for i in range(n - 1)} if mode == 3 else None
        edges = dag_edges(perm, random.randint(1, 8), chain)
        if n >= 2:
            i, j = sorted(random.sample(range(n), 2))
            edges.discard((perm[i], perm[j]))
            edges.add((perm[j], perm[i]))
    else:                                        # 長鏈加捷徑：最長路徑要走完整條鏈
        edges = dag_edges(perm, n - 1 + random.randint(0, 3), {(perm[i], perm[i + 1]) for i in range(n - 1)})
    emit(t, edges)
elif size == "mid":
    n, m = 2000, 6000
    perm = shuffled(n)
    t = [random.randint(1, BIG) for _ in range(n)]
    edges = dag_edges(perm, m, span=None if seed % 2 else 40)
    if seed == 4:                                # 加一條反向邊造出環 → -1
        a, b = perm[0], perm[1]
        edges.discard((a, b))
        edges |= {(b, a), (a, perm[1000]), (perm[1000], b)}
    emit(t, edges)
else:
    n, m = 100000, 200000
    shape = (seed - 1) % 5
    perm = shuffled(n)
    if shape == 0:                               # 隨機 DAG，天數隨機
        t = [random.randint(1, BIG) for _ in range(n)]
        edges = dag_edges(perm, m, span=50)
    elif shape == 1:                             # 長鏈，每項 10⁹ 天：答案 10¹⁴，int 會溢位
        t = [BIG] * n
        edges = dag_edges(perm, m, {(perm[i], perm[i + 1]) for i in range(n - 1)}, span=3)
    elif shape == 2:                             # 星形：一項工作是其他所有工作的前置
        t = [random.randint(1, BIG) for _ in range(n)]
        edges = dag_edges(perm, m, {(perm[0], perm[i]) for i in range(1, n)})
    elif shape == 3:                             # 大環 1 → 2 → … → n → 1 再加捷徑：-1
        t = [BIG] * n
        perm = list(range(1, n + 1))
        edges = dag_edges(perm, m - 1, {(i, i + 1) for i in range(1, n)}) | {(n, 1)}
    else:                                        # 長鏈加隨機邊，最後兩項之間藏一個小環：-1
        t = [random.randint(1, BIG) for _ in range(n)]
        a, b = perm[-2], perm[-1]
        edges = dag_edges(perm, m - 1, {(perm[i], perm[i + 1]) for i in range(n - 1)}) | {(b, a)}
    emit(t, edges)
