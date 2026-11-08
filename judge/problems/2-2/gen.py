"""實作 2-2 夜市火災的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（R, C ≤ 8），max 用 R = C = 1000 並依 seed 換不同形狀。
S 恰好一個，F 可以很多也可以沒有。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(g):
    """印出一筆測資：g 是字元的二維清單"""
    print(len(g), len(g[0]))
    print("\n".join("".join(r) for r in g))


def framed(R, C, pw, pf, holes):
    """外圈是牆、只開 holes 個缺口，內部隨機牆（機率 pw）與火（機率 pf），S 在內部"""
    g = [['#'] * C for _ in range(R)]
    for x in range(1, R - 1):
        for y in range(1, C - 1):
            r = random.random()
            g[x][y] = '#' if r < pw else ('F' if r < pw + pf else '.')
    border = [(x, y) for x in range(R) for y in range(C) if x in (0, R - 1) or y in (0, C - 1)]
    for x, y in random.sample(border, holes):
        g[x][y] = 'F' if random.random() < 0.15 else '.'
    g[random.randint(1, R - 2)][random.randint(1, C - 2)] = 'S'
    return g


if size == "small":
    if seed == 1:                                # 1 × 1，只有 S：一步就出去
        g = [['S']]
    elif seed == 2:                              # S 四周都是火，但 S 在外圈：還是一步就出去
        g = [list("FSF")]
    elif seed == 3:                              # S 被牆包住：-1
        g = [list("###"), list("#S#"), list("###")]
    elif seed == 4:                              # 你和火同時到達 S 上方那格：不能進去，-1
        g = [list("#.###"), list("#.F.#"), list("#S###"), list("#####")]
    elif seed == 5:                              # 同一張圖，但火晚一分鐘到：剛好來得及，答案 3
        g = [list("#.###"), list("#..F#"), list("#S###"), list("#####")]
    elif seed % 4 == 0:                          # 完全隨機（含 1 × C、R × 1，S 可能在外圈）
        R, C = random.randint(1, 6), random.randint(1, 6)
        pw = random.choice([0.0, 0.2, 0.35])
        pf = random.choice([0.0, 0.05, 0.15])
        g = [['#' if random.random() < pw else ('F' if random.random() < pf else '.') for _ in range(C)] for _ in range(R)]
        g[random.randrange(R)][random.randrange(C)] = 'S'
    else:                                        # 外圈是牆、開幾個缺口，S 在內部：答案通常大於 1
        R, C = random.randint(3, 8), random.randint(3, 8)
        g = framed(R, C, random.choice([0.1, 0.25, 0.35]), random.choice([0.0, 0.03, 0.08, 0.15]), random.randint(1, 3))
    emit(g)
elif size == "mid":
    R, C = random.randint(50, 150), random.randint(50, 150)
    if seed % 2 == 1:                            # 外圈是牆、開很多缺口，內部少量牆與 1～3 個火源
        g = framed(R, C, 0.15, 0.0, random.randint(20, 60))
    else:                                        # 沒有外牆，S 在中間附近，1～3 個火源
        g = [['#' if random.random() < 0.15 else '.' for _ in range(C)] for _ in range(R)]
        g[R // 2 + random.randint(-5, 5)][C // 2 + random.randint(-5, 5)] = 'S'
    for _ in range(random.randint(1, 3)):
        x, y = random.randrange(R), random.randrange(C)
        if g[x][y] != 'S':
            g[x][y] = 'F'
    emit(g)
else:
    R = C = 1000
    kind = seed % 6
    if kind == 1:                                # 空地、沒有火、S 在正中央：答案 500
        g = [['.'] * C for _ in range(R)]
        g[500][500] = 'S'
    elif kind == 2:                              # 蛇形走廊，火緊跟在 S 後面一格，出口在最遠的一端：答案 498003
        g = [['#'] * C for _ in range(R)]
        for x in range(1, R - 1, 2):
            for y in range(1, C - 1):
                g[x][y] = '.'
        for x in range(2, R - 1, 2):             # 連接相鄰兩條走廊的缺口，左右輪流
            g[x][C - 2 if (x // 2) % 2 == 1 else 1] = '.'
        g[1][1] = 'F'
        g[1][2] = 'S'
        last = max(range(1, R - 1, 2))           # 最後一條走廊，往下打通到地圖外圈
        g[last + 1][C // 2] = '.'
        g[R - 1][C // 2] = '.'
    elif kind == 3:                              # 外圈是牆、開 40 個缺口，內部 20% 牆、5 個火源
        g = framed(R, C, 0.2, 0.0, 40)
        for _ in range(5):
            x, y = random.randint(1, R - 2), random.randint(1, C - 2)
            if g[x][y] != 'S':
                g[x][y] = 'F'
    elif kind == 4:                              # 除了 S 全部著火：-1
        g = [['F'] * C for _ in range(R)]
        g[500][500] = 'S'
    elif kind == 5:                              # 空地上 3 個火源和 S 賽跑
        g = [['.'] * C for _ in range(R)]
        for _ in range(3):
            g[random.randrange(R)][random.randrange(C)] = 'F'
        g[random.randint(300, 700)][random.randint(300, 700)] = 'S'
    else:                                        # 只有一條走廊通往出口，火從側邊走廊和你「同時」到達岔路口：-1
        g = [['#'] * C for _ in range(R)]
        for y in range(1, C):                    # 第 500 列：從 S 往右通到右邊外圈
            g[500][y] = '.'
        for x in range(100, 500):                # 第 700 行：火走的側邊走廊
            g[x][700] = '.'
        g[500][300] = 'S'                        # S 走 400 步到 (500, 700)
        g[100][700] = 'F'                        # 火也走 400 步到 (500, 700)
    emit(g)
