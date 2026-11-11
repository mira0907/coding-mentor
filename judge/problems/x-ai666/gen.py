"""x-ai666 的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（N ≤ 10），max 用題目上限並依 seed 換不同形狀。
所有測資的價格都在 1～10⁷。每次交易獲利 < 10⁷，K ≤ 100，所以最大獲利 < 10⁹，自動符合「不超過 1.5×10⁹」。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
PMAX = 10_000_000                              # 價格上限
def emit(p, k):
    p = [min(PMAX, max(1, x)) for x in p]
    print(len(p), k)
    print(" ".join(map(str, p)))


def shaped(n, mode, hi):
    """0 隨機、1 鋸齒（漲跌交替）、2 隨機漫步、3 少數大波段"""
    if mode == 0:
        return [random.randint(1, hi) for _ in range(n)]
    if mode == 1:
        return [random.randint(1, hi // 2) if i % 2 == 0 else random.randint(hi // 2, hi) for i in range(n)]
    if mode == 2:
        p, x = [], random.randint(1, hi)
        for _ in range(n):
            x = min(hi, max(1, x + random.randint(-hi // 10 - 1, hi // 10 + 1)))
            p.append(x)
        return p
    p = []
    waves = random.randint(1, 6)
    for i in range(n):
        t = i * waves * 2 // n
        base = hi if t % 2 else 1
        p.append(max(1, min(hi, base + random.randint(-hi // 20, hi // 20))))
    return p


if size == "small":
    n = random.randint(2, 10)
    if seed == 1:                                # 一路下跌，答案 0
        p = sorted(random.sample(range(1, 50), n), reverse=True)
        emit(p, random.randint(1, 3))
    elif seed == 2:                              # 全部相同，答案 0
        emit([7] * n, random.randint(1, 3))
    elif seed == 3:                              # 一路上漲，一次交易就夠
        emit(sorted(random.sample(range(1, 50), n)), random.randint(1, 5))
    elif seed == 4:                              # 只有兩個時間點
        emit([random.randint(1, 20) for _ in range(2)], 1)
    elif seed == 5:                              # K 比 N 還大
        emit(shaped(n, 1, 30), n + 3)
    else:
        emit(shaped(n, seed % 4, random.choice([5, 20, 100])), random.randint(1, 6))
elif size == "mid":
    n = 1000
    emit(shaped(n, seed % 4, PMAX), random.randint(1, 100))
else:
    n = 100000
    kind = seed % 6
    if kind == 1:                                # 鋸齒、K = 100：交易機會遠多於 K
        emit(shaped(n, 1, PMAX), 100)
    elif kind == 2:                              # 一路上漲、K = 100
        emit(sorted(random.randint(1, PMAX) for _ in range(n)), 100)
    elif kind == 3:                              # 一路下跌，答案 0
        emit(sorted((random.randint(1, PMAX) for _ in range(n)), reverse=True), 100)
    elif kind == 4:                              # 少數大波段、K = 1
        emit(shaped(n, 3, PMAX), 1)
    elif kind == 5:                              # 隨機漫步、K 隨機
        emit(shaped(n, 2, PMAX), random.randint(1, 100))
    else:                                        # 隨機
        emit(shaped(n, 0, PMAX), 100)
