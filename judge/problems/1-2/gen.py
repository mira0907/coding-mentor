"""實作 1-2 傳話遊戲的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 9），max 用題目上限並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(a):
    """印出一筆測資：a[i] 是第 i + 1 位同學會傳給誰"""
    print(len(a))
    print(" ".join(map(str, a)))


def relabel(a):
    """把編號隨機打亂，形狀不變"""
    n = len(a)
    p = list(range(1, n + 1))
    random.shuffle(p)
    b = [0] * n
    for i in range(n):
        b[p[i] - 1] = p[a[i] - 1]
    return b


def shaped(n, mode):
    """依 mode 產生傳話對象：0 隨機、1 排列（每人都在環上）、2 長尾巴接小環、3 鏈加自環"""
    if mode == 0:
        return [random.randint(1, n) for _ in range(n)]
    if mode == 1:
        a = list(range(1, n + 1))
        random.shuffle(a)
        return a
    if mode == 2:
        return [random.randint(1, max(1, i)) for i in range(1, n + 1)]
    return [min(n, i + 1) if random.random() < 0.7 else random.randint(1, n) for i in range(1, n + 1)]


if size == "small":
    if seed == 1:                                # 只有一人，自己說給自己聽
        emit([1])
    elif seed == 2:                              # 每人都只說給自己聽
        n = random.randint(2, 9)
        emit(list(range(1, n + 1)))
    else:
        emit(shaped(random.randint(1, 9), seed % 4))
elif size == "mid":
    n = 2000
    emit(relabel(shaped(n, seed % 4)))
else:
    n = 200000
    kind = seed % 4
    if kind == 1:                                # 長鏈 1 → 2 → … → n → n，答案 n, n − 1, …, 1
        a = [i + 1 for i in range(1, n)] + [n]
    elif kind == 2:                              # 一個包含所有人的大環，編號打亂
        a = relabel([i % n + 1 for i in range(1, n + 1)])
    elif kind == 3:                              # ρ 形：10⁵ 長的尾巴接上 10⁵ 長的環，編號打亂
        h = n // 2
        a = [i + 1 for i in range(1, n)] + [h + 1]
        a = relabel(a)
    else:                                        # 隨機
        a = [random.randint(1, n) for _ in range(n)]
    emit(a)
