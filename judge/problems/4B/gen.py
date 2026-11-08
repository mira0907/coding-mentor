"""範例 4-B 帳本矛盾的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 5、m ≤ 8），max 用題目上限並依 seed 換不同形狀。
做法：先替每個帳戶定好真正的餘額 val，一致的紀錄就寫 c = val[b] − val[a]，再在指定位置放矛盾的紀錄。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
C = 10**9                                      # |c| 的上限
TWO32 = 1 << 32                                # int 溢位時差值會差 2³²


def emit(n, recs):
    """印出一筆測資：n 個帳戶、recs 是 (a, b, c) 的清單（依序）"""
    print(n, len(recs))
    print("\n".join(f"{a} {b} {c}" for a, b, c in recs))


def good(val, a, b):
    """與 val 一致的紀錄 (a, b, c)"""
    return (a, b, val[b] - val[a])


def bump(c):
    """把 c 往 0 的方向改 1，讓紀錄變矛盾但 |c| 仍 ≤ 10⁹"""
    return c - 1 if c > 0 else c + 1


def random_consistent(n, m, val, star=False):
    """m 條與 val 一致的隨機紀錄；star = True 時一半的紀錄都從帳戶 1 出發。偶爾 a = b、c = 0"""
    recs = []
    for _ in range(m):
        a, b = random.randint(1, n), random.randint(1, n)
        if star and random.random() < 0.5:
            a = 1
        if random.random() < 0.02:
            b = a
        recs.append(good(val, a, b))
    return recs


def chain_with_trap(n, m):
    """長鏈：第 k 條紀錄「k+1 k c」讓並查集長成深度 n 的鏈，餘額差累積到約 10¹⁴。
    之後是相鄰帳戶的一致紀錄（常查到最深的帳戶 1），最後一條是真的矛盾，
    但它的 c 恰好等於真正差值減 2³²，用 int 存差值的程式會誤以為一致。"""
    val = [0] * (n + 1)
    for k in range(2, n + 1):
        val[k] = val[k - 1] + random.randint(C // 2, C)
    recs = [good(val, k + 1, k) for k in range(1, n)]
    while len(recs) < m - 1:
        k = random.choice([1, 1, 2, random.randint(1, n - 1)])
        r = random.random()
        recs.append(good(val, k, k + 1) if r < 0.45 else good(val, k + 1, k) if r < 0.9 else (k, k, 0))
    x = next(k for k in range(2, n + 1) if val[k] - val[1] >= TWO32 - C)
    recs.append((1, x, val[x] - val[1] - TWO32))
    return recs


if size == "small":
    style = seed % 5
    n = 1 if seed % 7 == 0 else random.randint(2, 5)   # seed 7、14 是只有一個帳戶的情況
    m = random.randint(1, 8)
    val = [0] + [random.randint(-5, 5) for _ in range(n)]
    if style == 0:                               # 全部一致（答案 −1）；seed 5 是 n = 1、只有「1 1 0」
        if seed == 5:
            emit(1, [(1, 1, 0)])
        else:
            emit(n, random_consistent(n, m, val))
    elif style == 1:                             # 大多一致，偶爾差 1
        recs = random_consistent(n, m, val)
        recs = [(a, b, c + random.choice([-1, 1])) if random.random() < 0.2 else (a, b, c) for a, b, c in recs]
        emit(n, recs)
    elif style == 2:                             # a = b 而 c ≠ 0 的矛盾
        recs = random_consistent(n, m, val)
        i = random.randrange(m)
        a = random.randint(1, n)
        recs[i] = (a, a, random.choice([-3, 2, C]))
        emit(n, recs)
    elif style == 3:                             # 方向反過來寫的紀錄：「b a c」只有在 c = 0 時才一致
        recs = random_consistent(n, m, val)
        recs = [(b, a, c) if random.random() < 0.2 else (a, b, c) for a, b, c in recs]
        emit(n, recs)
    else:                                        # 餘額差到 10⁹ 等級
        val = [0] + [random.randint(-C // 2, C // 2) for _ in range(n)]
        recs = random_consistent(n, m, val)
        if random.random() < 0.6:
            i = random.randrange(m)
            a, b, c = recs[i]
            recs[i] = (a, b, bump(c))
        emit(n, recs)
elif size == "mid":
    n, m = 2000, 5000
    style = seed % 3
    if style == 1:                               # 全部一致（答案 −1）
        val = [0] + [random.randint(-C // 2, C // 2) for _ in range(n)]
        emit(n, random_consistent(n, m, val))
    elif style == 2:                             # 長鏈加 int 溢位陷阱
        emit(n, chain_with_trap(n, m))
    else:                                        # 中間某條差 1
        val = [0] + [random.randint(-C // 2, C // 2) for _ in range(n)]
        recs = random_consistent(n, m, val)
        i = random.randrange(m // 2, m)
        a, b, c = recs[i]
        recs[i] = (a, b, bump(c))
        emit(n, recs)
else:
    n, m = 100000, 200000
    style = (seed - 1) % 5
    val = [0] + [random.randint(-C // 2, C // 2) for _ in range(n)]
    if style == 0:                               # 長鏈：深度 10⁵ 的遞迴、差值約 10¹⁴、最後一條是 int 溢位陷阱
        emit(n, chain_with_trap(n, m))
    elif style == 1:                             # 隨機且全部一致（答案 −1）
        emit(n, random_consistent(n, m, val))
    elif style == 2:                             # 隨機，後半某條差 1，之後還有更多矛盾
        recs = random_consistent(n, m, val)
        i = random.randrange(m // 2, m - 100)
        for j in [i] + random.sample(range(i + 1, m), 50):
            a, b, c = recs[j]
            recs[j] = (a, b, bump(c))
        emit(n, recs)
    elif style == 3:                             # 星狀：先把每個帳戶連到帳戶 1，再查葉子之間；最後一條矛盾
        recs = [good(val, 1, v) if random.random() < 0.5 else good(val, v, 1) for v in range(2, n + 1)]
        while len(recs) < m - 1:
            recs.append(good(val, random.randint(2, n), random.randint(2, n)))
        a, b = random.sample(range(2, n + 1), 2)
        recs.append((a, b, bump(val[b] - val[a])))
        emit(n, recs)
    else:                                        # 中間一條「a a c」c ≠ 0 的矛盾，其餘一致
        recs = random_consistent(n, m, val)
        a = random.randint(1, n)
        recs[random.randrange(m // 3, m)] = (a, a, random.choice([-C, C]))
        emit(n, recs)
