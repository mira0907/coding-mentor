"""範例 6-B 開關設定（2-SAT）的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
條件「i a j b」允許 i = j；有解與無解的測資都會出現。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, clauses, relabel=True):
    """印出一筆測資：clauses 是 (i, a, j, b)；relabel 時打亂開關編號與條件順序"""
    lab = list(range(n + 1))
    if relabel:
        lab = [0] + random.sample(range(1, n + 1), n)
        random.shuffle(clauses)
    print(n, len(clauses))
    print("\n".join(f"{lab[i]} {a} {lab[j]} {b}" for i, a, j, b in clauses))


def rand_clause(n):
    """完全隨機的一個條件"""
    return random.randint(1, n), random.randint(0, 1), random.randint(1, n), random.randint(0, 1)


def planted(n, x):
    """隨機產生一個被設定 x 滿足的條件（x[i] 是開關 i 的值）"""
    while True:
        i, a, j, b = rand_clause(n)
        if x[i] == a or x[j] == b:
            return i, a, j, b


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 8)
    x = [0] + [random.randint(0, 1) for _ in range(n)]   # 藏起來的一組解
    mode = seed % 5
    if mode == 0:                                # 少量隨機條件，多半有解
        cl = [rand_clause(n) for _ in range(random.randint(1, n + 2))]
    elif mode == 1:                              # 偏多的隨機條件，常常無解
        cl = [rand_clause(n) for _ in range(random.randint(2 * n, 3 * n + 2))]
    elif mode == 2:                              # 先藏一組解再出題：一定有解，通常有很多組
        cl = [planted(n, x) for _ in range(random.randint(1, 2 * n + 2))]
    elif mode == 3:                              # 用 i = j 的條件直接指定開關，偶爾互相矛盾
        cl = [(i, x[i], i, x[i]) for i in random.sample(range(1, n + 1), random.randint(1, n))]
        cl += [planted(n, x) for _ in range(random.randint(0, n))]
        if seed % 2 == 0:
            i = random.randint(1, n)
            cl += [(i, 0, i, 0), (i, 1, i, 1)]
    else:                                        # 混入「i 0 i 1」這種永遠成立的條件
        cl = [(i, 0, i, 1) for i in random.sample(range(1, n + 1), random.randint(1, n))]
        cl += [rand_clause(n) for _ in range(random.randint(0, n))]
    emit(n, cl)
elif size == "mid":
    n, m = 2000, 4000
    x = [0] + [random.randint(0, 1) for _ in range(n)]
    if seed % 2:                                 # 藏一組解：有解
        emit(n, [planted(n, x) for _ in range(m)])
    else:                                        # 完全隨機、條件數是 n 的兩倍：幾乎一定無解
        emit(n, [rand_clause(n) for _ in range(m)])
else:
    n, m = 100000, 200000
    shape = (seed - 1) % 5
    if shape == 0:                               # 藏一組解的隨機題：有解
        x = [0] + [random.randint(0, 1) for _ in range(n)]
        emit(n, [planted(n, x) for _ in range(m)])
    elif shape == 1:                             # 長串推論 1 → 2 → … → n，頭尾強制矛盾：無解
        cl = [(i, 0, i + 1, 1) for i in range(1, n)]          # 開關 i 為 1 → 開關 i+1 為 1
        cl += [(1, 1, 1, 1), (n, 0, n, 0)]                   # 開關 1 必為 1、開關 n 必為 0
        ones = [0] + [1] * n
        cl += [planted(n, ones) for _ in range(m - len(cl))] # 其餘條件全 1 都滿足，不影響矛盾
        emit(n, cl)
    elif shape == 2:                             # 同樣的長串推論，但只要求「n 為 1 → 1 為 0」：有解，遞迴很深
        k = random.randint(2, n)
        x = [0] + [0 if i < k else 1 for i in range(1, n + 1)]   # 前段 0、後段 1 的一組解
        cl = [(i, 0, i + 1, 1) for i in range(1, n)] + [(n, 0, 1, 0)]
        cl += [planted(n, x) for _ in range(m - len(cl))]
        emit(n, cl)
    elif shape == 3:                             # 每個開關都被 i = j 的條件指定：唯一解，另有永遠成立的條件
        x = [0] + [random.randint(0, 1) for _ in range(n)]
        cl = [(i, x[i], i, x[i]) for i in range(1, n + 1)]
        cl += [(i, 0, i, 1) for i in random.sample(range(1, n + 1), 20000)]
        cl += [planted(n, x) for _ in range(m - len(cl))]
        emit(n, cl)
    else:                                        # 完全隨機、條件數是 n 的兩倍：幾乎一定無解
        emit(n, [rand_clause(n) for _ in range(m)])
