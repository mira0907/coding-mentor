"""實作 6-3 寶石收集的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 7），max 用題目上限並依 seed 換不同形狀。
題目沒說可以有自環或重複的通道，所以都不產生。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
BIG = 10**9                                    # a_i 的上限


def emit(a, edges, keep_one=True):
    """印出一筆測資：a 是每個房間的寶石數、edges 是 (u, v) 通道（去重、打亂）。
    打亂房間編號時，keep_one = True 會讓原本的 1 號房間保持是起點 1。"""
    n = len(a)
    edges = list(dict.fromkeys(e for e in edges if e[0] != e[1]))
    lab = [0] + [1] + random.sample(range(2, n + 1), n - 1) if keep_one else list(range(n + 1))
    random.shuffle(edges)
    gems = [0] * (n + 1)
    for i in range(1, n + 1):
        gems[lab[i]] = a[i - 1]
    print(n, len(edges))
    print(" ".join(map(str, gems[1:])))
    if edges:
        print("\n".join(f"{lab[u]} {lab[v]}" for u, v in edges))


def rand_edges(lo, hi, k):
    """lo..hi 之間 k 條隨機有向邊（u ≠ v）"""
    return [tuple(random.sample(range(lo, hi + 1), 2)) for _ in range(k)]


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 7)
    maxa = BIG if seed % 4 == 0 else 6           # 有時用很大的寶石數
    a = [random.randint(0, maxa) for _ in range(n)]
    mode = seed % 5
    if n == 1 or mode == 0:                      # 沒有通道：只拿得到房間 1
        edges = []
    elif mode in (1, 2):                         # 隨機有向圖
        edges = rand_edges(1, n, random.randint(1, 2 * n))
    elif mode == 3:                              # DAG（順著編號走），要選對分支
        edges = [tuple(sorted(e)) for e in rand_edges(1, n, random.randint(1, 2 * n))]
    else:                                        # 一個環加上幾條往外的邊，常有走不到的房間
        k = random.randint(2, n)
        edges = [(i, i % k + 1) for i in range(1, k + 1)] + rand_edges(1, n, random.randint(0, 3))
    emit(a, edges)
elif size == "mid":
    n = 2000
    a = [random.randint(0, BIG) for _ in range(n)]
    emit(a, rand_edges(1, n, [1500, 2500, 3500, 5000][(seed - 1) % 4]))
else:
    n, m = 100000, 200000
    shape = (seed - 1) % 6
    if shape == 0:                               # 長鏈 1 → 2 → … → n，每間 10⁹：答案 10¹⁴，遞迴深度 10⁵
        a = [BIG] * n
        edges = [(i, i + 1) for i in range(1, n)]
        while len(edges) < m:                    # 再補往後跳 2～50 格的捷徑
            i = random.randint(1, n - 50)
            edges.append((i, i + random.randint(2, 50)))
        emit(a, edges, keep_one=False)
    elif shape == 1:                             # 大環：全部同一個 SCC，可以拿光
        a = [BIG] * n
        edges = [(i, i % n + 1) for i in range(1, n + 1)] + rand_edges(1, n, m - n)
        emit(a, edges)
    elif shape == 2:                             # 反向長鏈 n → … → 1：房間 1 哪裡都去不了，其他房間的寶石拿不到
        a = [random.randint(0, BIG) for _ in range(n)]
        emit(a, [(i + 1, i) for i in range(1, n)], keep_one=False)
    elif shape == 3:                             # 星形：1 通往所有房間，只能挑一間（最大的那間）
        a = [random.randint(0, BIG) for _ in range(n)]
        emit(a, [(1, v) for v in range(2, n + 1)])
    elif shape == 4:                             # 很多小 SCC 排成 DAG，每間 0～10⁹：要選對路線
        a = [random.randint(0, BIG) for _ in range(n)]
        edges = []
        for b in range(0, n, 4):                 # 每 4 間一組，組內成環
            grp = list(range(b + 1, min(n, b + 4) + 1))
            edges += [(grp[i], grp[(i + 1) % len(grp)]) for i in range(len(grp))]
        while len(edges) < m:                    # 組之間只往編號大的組走（DAG）
            u = random.randint(1, n - 8)
            edges.append((u, min(n, u + random.randint(4, 40))))
        emit(a, edges, keep_one=False)
    else:                                        # 隨機有向圖，寶石數有大有小
        a = [random.choice([0, random.randint(0, BIG)]) for _ in range(n)]
        emit(a, rand_edges(1, n, m))
