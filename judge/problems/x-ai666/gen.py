"""x-ai666 的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（N ≤ 10）；mid 依 seed 產生子題 1、2、3 的測資；max 產生子題 3、4 的最大測資。
保證價格在 1～10⁷，且最大獲利不超過 1.5×10⁹。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
PMAX = 10_000_000                              # 價格上限
LIMIT = 1_500_000_000                          # 最大獲利上限


def rise(p):
    """所有上漲幅度的總和：K 夠大時就是答案，也是任何交易方式的上界"""
    return sum(max(0, b - a) for a, b in zip(p, p[1:]))


def fit(p, k):
    """必要時把價格往 1 壓縮，保證最大獲利 ≤ LIMIT。
    最大獲利 ≤ min(上漲總和, k × (最高價 − 最低價))。"""
    while True:
        r = rise(p)
        bound = min(r, k * (max(p) - min(p)))
        if bound <= LIMIT:
            return p
        f = LIMIT / bound * 0.99
        p = [1 + int((x - 1) * f) for x in p]


def emit(p, k):
    p = fit([min(PMAX, max(1, x)) for x in p], k)
    sys.stdout.write(f"{len(p)} {k}\n")
    sys.stdout.write(" ".join(map(str, p)) + "\n")


def shaped(n, mode, hi):
    """0 隨機、1 鋸齒（漲跌交替、幅度不一）、2 隨機漫步、3 少數大波段、4 波段裡夾小波動"""
    if mode == 0:
        return [random.randint(1, hi) for _ in range(n)]
    if mode == 1:
        return [random.randint(1, hi // 2) if i % 2 == 0 else random.randint(hi // 2, hi) for i in range(n)]
    if mode == 2:
        p, x = [], random.randint(1, hi)
        step = max(1, hi // 10)
        for _ in range(n):
            x = min(hi, max(1, x + random.randint(-step, step)))
            p.append(x)
        return p
    waves = random.randint(1, 6) if mode == 3 else random.randint(20, 200)
    noise = hi // 20 if mode == 3 else hi // 4
    p = []
    for i in range(n):
        t = i * waves * 2 // n
        base = hi if t % 2 else 1
        p.append(max(1, min(hi, base + random.randint(-noise, noise))))
    return p


if size == "small":
    n = random.randint(2, 10)
    if seed == 1:                                # 一路下跌，答案 0
        emit(sorted(random.sample(range(1, 50), n), reverse=True), random.randint(1, 3))
    elif seed == 2:                              # 全部相同，答案 0
        emit([7] * n, random.randint(1, n))
    elif seed == 3:                              # 一路上漲，一次交易就夠
        emit(sorted(random.sample(range(1, 50), n)), random.randint(1, n))
    elif seed == 4:                              # 只有兩個時間點
        emit([random.randint(1, 20) for _ in range(2)], random.choice([1, 2]))
    elif seed == 5:                              # K = N
        emit(shaped(n, 1, 30), n)
    elif seed <= 9:                              # K = 1（子題 1）
        emit(shaped(n, seed % 5, random.choice([5, 20, 100])), 1)
    else:
        emit(shaped(n, seed % 5, random.choice([5, 20, 100])), random.randint(1, n))
elif size == "mid":
    if seed <= 2:                                # 子題 1：N = 1000、K = 1
        emit(shaped(1000, 3 if seed == 1 else 0, PMAX), 1)
    elif seed <= 4:                              # 子題 2：N = 50000、K = 100
        emit(shaped(50000, 1 if seed == 3 else 4, PMAX), 100)
    else:                                        # 子題 3：N = 50000、K 大
        n = 50000
        emit(shaped(n, 1 if seed == 5 else 4, PMAX), random.randint(n // 20, n))
else:
    if seed <= 3:                                # 子題 3 的最大規模：N = 200000
        n = 200000
        if seed == 1:                            # 鋸齒、K = N：答案是所有上漲的總和
            emit(shaped(n, 1, PMAX), n)
        elif seed == 2:                          # 波段夾小波動、K 中等：一定要選擇與合併
            emit(shaped(n, 4, PMAX), random.randint(100, 5000))
        else:                                    # 隨機漫步、K 隨機
            emit(shaped(n, 2, PMAX), random.randint(1, n))
    else:                                        # 子題 4：N = 2000000
        n = 2000000
        if seed == 4:                            # 鋸齒、K 中等
            emit(shaped(n, 1, PMAX), random.randint(1000, 100000))
        elif seed == 5:                          # 波段夾小波動、K = N
            emit(shaped(n, 4, PMAX), n)
        else:                                    # 一路下跌，答案 0
            emit(sorted((random.randint(1, PMAX) for _ in range(n)), reverse=True), n)
