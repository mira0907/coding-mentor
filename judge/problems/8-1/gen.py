"""實作 8-1 躲避球分隊的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 12），max 用題目上限並依 seed 換不同形狀。
同一組可能重複出現，也可能前後顛倒；不會有 u = v。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資；每組隨機前後顛倒，順序打亂"""
    edges = [(a, b) if random.random() < 0.5 else (b, a) for a, b in edges]
    random.shuffle(edges)
    print("\n".join([f"{n} {len(edges)}"] + [f"{a} {b}" for a, b in edges]))


def bip(n, m, plus):
    """先把人隨機分兩邊，只在兩邊之間連 m 組（做得到）；plus = True 時再加一組同邊的（多半做不到）"""
    side = [random.randint(0, 1) for _ in range(n + 1)]   # side[u] = u 偷偷被分到哪一邊
    edges = []
    for _ in range(50 * m):
        if len(edges) == m:
            break
        u, v = random.randint(1, n), random.randint(1, n)
        if side[u] != side[v]:
            edges.append((u, v))
    if plus and n >= 2:
        edges.append(tuple(random.sample(range(1, n + 1), 2)))
    return edges


if size == "small":
    n = random.randint(1, 12)
    kind = seed % 6
    if seed == 1:                              # 最小：1 個人、沒有任何一組
        emit(1, [])
    elif kind == 0 or n == 1:                  # 沒有任何一組：全部第 1 隊
        emit(n, [])
    elif kind == 1:                            # 樹：一定做得到
        emit(n, [(random.randint(1, v - 1), v) for v in range(2, n + 1)])
    elif kind == 2:                            # 隨機圖，多半有奇環
        emit(n, [tuple(random.sample(range(1, n + 1), 2)) for _ in range(random.randint(1, 15))])
    else:                                      # 二分圖（可能再加一組破壞它），夾雜重複的組
        edges = bip(n, random.randint(0, 14), kind == 5)
        if edges and random.random() < 0.5:
            edges.append(random.choice(edges))
        emit(n, edges)
elif size == "mid":
    n = 2000
    emit(n, bip(n, 2000, seed % 2 == 0))
else:
    n = m = 200000
    kind = (seed - 1) % 4
    perm = random.sample(range(1, n + 1), n)   # perm = 打亂的編號，用來排鏈和環
    if kind == 0:                              # 長鏈加一組重複的：BFS 很深，做得到
        edges = [(perm[i], perm[i + 1]) for i in range(n - 1)] + [(perm[0], perm[1])]
        emit(n, edges)
    elif kind == 1:                            # 長度 199999 的奇環，再掛一個人：做不到
        k = n - 1
        emit(n, [(perm[i], perm[(i + 1) % k]) for i in range(k)] + [(perm[k], perm[0])])
    elif kind == 2:                            # 隨機二分圖：做得到，很多連通塊
        emit(n, bip(n, m, False))
    else:                                      # 星狀加重複的組：中心第 1 或 2 隊、其他人相反
        c = random.randint(1, n)               # c = 中心
        edges = [(c, v) for v in range(1, n + 1) if v != c]
        emit(n, edges + [(c, random.choice([v for v in (1, 2) if v != c]))])
