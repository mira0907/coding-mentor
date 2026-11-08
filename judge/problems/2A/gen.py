"""範例 2-A 騎士巡邏的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（N ≤ 8），max 用 N = 1000 並依 seed 換不同的起終點。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def cell(N):
    """隨機一格"""
    return random.randint(1, N), random.randint(1, N)


if size == "small":
    if seed == 1:                                # 1 × 1 棋盤，起點就是終點
        N, s, t = 1, (1, 1), (1, 1)
    elif seed == 2:                              # 2 × 2 棋盤：騎士一步都走不了
        N, s, t = 2, cell(2), cell(2)
        if s == t:
            t = (3 - s[0], s[1])
    elif seed == 3:                              # 3 × 3 棋盤：中心格到不了
        N, s, t = 3, (1, 1), (2, 2)
    elif seed == 4:                              # 3 × 3 棋盤的角落走到中心以外的格子
        N, s, t = 3, (1, 1), cell(3)
        if t == (2, 2):
            t = (3, 3)
    else:
        N = random.randint(3, 8)
        s = cell(N)
        t = s if seed % 7 == 0 else cell(N)      # 偶爾起點等於終點
    print(N, s[0], s[1], t[0], t[1])
elif size == "mid":
    N = random.randint(100, 500)
    s, t = cell(N), cell(N)
    print(N, s[0], s[1], t[0], t[1])
else:
    N = 1000
    kind = seed % 4
    if kind == 1:                                # 左上角到右下角，步數最多
        s, t = (1, 1), (N, N)
    elif kind == 2:                              # 角落走到斜對角的鄰格：無限大棋盤只要 2 步，這裡要 4 步
        s, t = (1, 1), (2, 2)
    elif kind == 3:                              # 右上角到左下角旁邊，換一個方向
        s, t = (1, N), (N, 2)
    else:                                        # 隨機起終點
        s, t = cell(N), cell(N)
    print(N, s[0], s[1], t[0], t[1])
