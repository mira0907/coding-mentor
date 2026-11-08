"""範例 8-B 專案選擇的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 10、m ≤ 8），max 用題目上限並依 seed 換不同形狀。
每個專案需要的工具編號互不重複。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(p, c, need):
    """印出一筆測資：p = 專案獲利，c = 工具價格，need[i] = 專案 i 需要的工具"""
    out = [f"{len(p)} {len(c)}", " ".join(map(str, p)), " ".join(map(str, c))]
    out += [" ".join(map(str, [len(x)] + x)) for x in need]
    print("\n".join(out))


def rand_need(n, m, kmax):
    """每個專案隨機需要 0～kmax 種不同的工具"""
    return [random.sample(range(1, m + 1), random.randint(0, min(m, kmax))) for _ in range(n)]


if size == "small":
    n, m = random.randint(1, 10), random.randint(1, 8)
    if seed == 1:                              # 最小：一個專案、一種工具，獲利與價格都是 0
        emit([0], [0], [[1]])
    elif seed == 2:                            # 每個專案都賠錢，答案 0
        need = [random.sample(range(1, m + 1), random.randint(1, m)) for _ in range(n)]
        emit([random.randint(0, 5) for _ in range(n)], [random.randint(6, 10) for _ in range(m)], need)
    else:
        top = random.choice([5, 20, 10**6])    # top = 數值上限；小的時候常常平手
        emit([random.randint(0, top) for _ in range(n)], [random.randint(0, top) for _ in range(m)],
             rand_need(n, m, random.choice([2, m])))
elif size == "mid":
    n = m = 50
    emit([random.randint(0, 10**6) for _ in range(n)], [random.randint(0, 10**6) for _ in range(m)],
         rand_need(n, m, 15))
else:
    n = m = 200
    kind = (seed - 1) % 4
    if kind == 0:                              # 隨機：每個專案最多 50 種工具
        emit([random.randint(0, 10**6) for _ in range(n)], [random.randint(0, 10**6) for _ in range(m)],
             rand_need(n, m, 50))
    elif kind == 1:                            # 全部 10⁶、每個專案都要全部工具：總獲利 = 總花費，處處平手，答案 0
        emit([10**6] * n, [10**6] * m, [list(range(1, m + 1)) for _ in range(n)])
    elif kind == 2:                            # 鏈狀共用：專案 i 要工具 i、i+1，獲利略高於一半的工具錢
        need = [[i, i + 1] if i < m else [i] for i in range(1, n + 1)]
        emit([random.randint(10**6 // 2, 10**6) for _ in range(n)], [random.randint(10**6 // 2, 10**6) for _ in range(m)], need)
    else:                                      # 獲利全是 10⁶、工具便宜：全做最好，答案接近 2×10⁸
        emit([10**6] * n, [random.randint(0, 1000) for _ in range(m)], rand_need(n, m, 200))
