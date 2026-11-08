"""實作 2-1 島嶼探險的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（R, C ≤ 6），max 用 R = C = 1000 並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(g):
    """印出一筆測資：g 是字串清單"""
    print(len(g), len(g[0]))
    print("\n".join(g))


def rand_grid(R, C, p):
    """每格以機率 p 是陸地"""
    return ["".join('#' if random.random() < p else '.' for _ in range(C)) for _ in range(R)]


def checker(R, C):
    """西洋棋盤：陸地只有斜對角相鄰，每格都是一座島"""
    return ["".join('#' if (x + y) % 2 == 0 else '.' for y in range(C)) for x in range(R)]


def snake(R, C):
    """蛇形：偶數列整列是陸地，奇數列只在左右兩端輪流留一格陸地，整片是一條長路"""
    g = []
    for x in range(R):
        if x % 2 == 0:
            g.append('#' * C)
        else:
            row = ['.'] * C
            row[C - 1 if (x // 2) % 2 == 0 else 0] = '#'
            g.append("".join(row))
    return g


if size == "small":
    R, C = random.randint(1, 6), random.randint(1, 6)
    mode = seed % 6
    if seed == 1:                                # 1 × 1 的陸地
        g = ['#']
    elif mode == 0:                              # 全是海：輸出 0 0
        g = ['.' * C for _ in range(R)]
    elif mode == 1:                              # 全是陸地
        g = ['#' * C for _ in range(R)]
    elif mode == 2:                              # 西洋棋盤
        g = checker(R, C)
    elif mode == 3:                              # 蛇形
        g = snake(R, C)
    else:                                        # 隨機
        g = rand_grid(R, C, random.choice([0.3, 0.5, 0.7]))
    emit(g)
elif size == "mid":
    R, C = random.randint(50, 200), random.randint(50, 200)
    emit(rand_grid(R, C, random.choice([0.4, 0.55, 0.6])))
else:
    R = C = 1000
    kind = seed % 5
    if kind == 1:                                # 全是陸地：一座 10⁶ 格的島，遞迴 DFS 會很深
        g = ['#' * C for _ in range(R)]
    elif kind == 2:                              # 西洋棋盤：5×10⁵ 座單格島，斜對角不能算相連
        g = checker(R, C)
    elif kind == 3:                              # 蛇形長路：約 5×10⁵ 格連成一條
        g = snake(R, C)
    elif kind == 4:                              # 隨機 59% 陸地，接近連通的臨界，島的形狀很不規則
        g = rand_grid(R, C, 0.59)
    else:                                        # 全是海
        g = ['.' * C for _ in range(R)]
    emit(g)
