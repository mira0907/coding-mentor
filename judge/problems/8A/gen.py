"""範例 8-A 工作分配的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（nL、nR ≤ 7），max 用題目上限並依 seed 換不同形狀。
同一組 (u, v) 不會重複出現。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(nL, nR, pairs):
    """印出一筆測資；pairs 是 (員工, 工作) 的清單，會打亂順序"""
    pairs = list(pairs)
    random.shuffle(pairs)
    print("\n".join([f"{nL} {nR} {len(pairs)}"] + [f"{u} {v}" for u, v in pairs]))


def rand_pairs(nL, nR, E):
    """隨機取 E 組不重複的 (u, v)"""
    S = set()
    while len(S) < E:
        S.add((random.randint(1, nL), random.randint(1, nR)))
    return S


if size == "small":
    nL, nR = random.randint(1, 7), random.randint(1, 7)
    if seed == 1:                              # 最小：1 位員工、1 項工作、沒有關係
        nL = nR = 1
        emit(1, 1, [])
    elif seed % 5 == 0:                        # 完全二分圖，答案 = min(nL, nR)
        emit(nL, nR, [(u, v) for u in range(1, nL + 1) for v in range(1, nR + 1)])
    elif seed % 5 == 1:                        # 階梯：員工 i 會做 i、i+1，只會做一項的放最後，要換很多次人
        k = min(nL, nR)
        S = {(i, i) for i in range(1, k + 1)} | {(i, i + 1) for i in range(1, k)}
        emit(nL, nR, S)
    else:                                      # 隨機稀疏或稠密
        E = random.randint(0, min(nL * nR, 14))
        emit(nL, nR, rand_pairs(nL, nR, E))
elif size == "mid":
    nL, nR = random.randint(80, 120), random.randint(80, 120)
    emit(nL, nR, rand_pairs(nL, nR, 2000))
else:
    kind = (seed - 1) % 4
    if kind == 0:                              # 隨機：500 × 500、2×10⁴ 組
        emit(500, 500, rand_pairs(500, 500, 20000))
    elif kind == 1:                            # 稠密區塊：141 × 141 完全二分圖，大量平手，其餘人沒得做
        emit(500, 500, [(u, v) for u in range(1, 142) for v in range(1, 142)][:20000])
    elif kind == 2:                            # 階梯加下三角：員工 i 只會做 i、i+1 與編號較小的工作，增廣路很長
        S = {(i, i) for i in range(1, 501)} | {(i, i + 1) for i in range(1, 500)}
        while len(S) < 20000:
            u = random.randint(2, 500)
            S.add((u, random.randint(1, u - 1)))
        emit(500, 500, S)
    else:                                      # 一邊很少：500 位員工只搶 3 項工作
        emit(500, 3, [(u, v) for u in range(1, 501) for v in range(1, 4)])
