"""範例 2-B 破牆迷宮的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（R, C ≤ 5），max 用 R = C = 500 並依 seed 換不同形狀。
起點（左上）與終點（右下）一定是 '.'。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(K, g):
    """印出一筆測資：g 是字元的二維清單，起點終點強制設成 '.'"""
    R, C = len(g), len(g[0])
    g[0][0] = '.'
    g[R - 1][C - 1] = '.'
    print(R, C, K)
    print("\n".join("".join(row) for row in g))


def rand_grid(R, C, p):
    """每格以機率 p 是牆"""
    return [['#' if random.random() < p else '.' for _ in range(C)] for _ in range(R)]


def snake(R, C):
    """蛇形迷宮：奇數列整列是牆，只在左右兩端輪流留一個缺口"""
    g = [['.'] * C for _ in range(R)]
    for x in range(1, R, 2):
        g[x] = ['#'] * C
        g[x][C - 1 if (x // 2) % 2 == 0 else 0] = '.'
    return g


# 手工挑過的小陷阱 (K, 地圖)：狀態沒有記「已打破幾面牆」的 BFS，不論方向順序都會答錯
TRAPS = [
    (1, ["..##", "#..#", "#..#", ".##."]),
    (1, ["..##", "#..#", "...#", ".###", "##.."]),
    (2, ["..##", "#.#.", ".#.#", ".##."]),
    (1, ["..#.#", "#...#", "...#."]),
]

if size == "small":
    if seed == 1:                                # 1 × 1：起點就是終點，答案 0
        R, C, g = 1, 1, [['.']]
        K = 0
    elif seed == 2:                              # 除了起點終點全是牆，K 小時到不了
        R, C = random.randint(2, 4), random.randint(2, 4)
        g = [['#'] * C for _ in range(R)]
        K = random.randint(0, 2)
    elif seed == 3:                              # 蛇形，K = 0 只能繞路
        R, C = 5, random.randint(2, 5)
        g, K = snake(R, C), 0
    elif seed == 4:                              # 蛇形，可以打破牆抄近路
        R, C = 5, random.randint(3, 5)
        g, K = snake(R, C), random.randint(1, 2)
    elif seed <= 8:                              # 陷阱：先打牆到某格比較快，但之後還得再打牆；每格只記一次會答錯
        K, rows = TRAPS[seed - 5]
        g = [list(r) for r in rows]
    else:                                        # 隨機地圖（含 1 × C、R × 1）
        R, C = random.randint(1, 5), random.randint(1, 5)
        g = rand_grid(R, C, random.choice([0.2, 0.35, 0.5, 0.65]))
        walls = sum(row.count('#') for row in g)
        K = random.randint(0, 3)
        if walls <= 12 and random.random() < 0.3:   # 牆少時偶爾給大 K（暴力解仍跑得動）
            K = random.randint(walls, 10)
    emit(K, g)
elif size == "mid":
    R, C = random.randint(40, 100), random.randint(40, 100)
    if seed % 2 == 0:                            # 蛇形，缺口位置隨機：不打牆也到得了，打牆可以抄近路
        g = snake(R, C)
        for x in range(1, R, 2):
            g[x] = ['#'] * C
            g[x][random.randrange(C)] = '.'
    else:                                        # 隨機地圖
        g = rand_grid(R, C, random.choice([0.25, 0.3, 0.35]))
    emit(random.randint(2, 10), g)
else:
    R = C = 500
    kind = seed % 5
    if kind == 1:                                # 隨機 40% 牆、K = 10：幾乎每個 (格子, k) 狀態都會走到
        g, K = rand_grid(R, C, 0.4), 10
    elif kind == 2:                              # 蛇形迷宮、K = 10：不打牆要走約 1.25×10⁵ 步
        g, K = snake(R, C), 10
    elif kind == 3:                              # 隨機 30% 牆、K 很小
        g, K = rand_grid(R, C, 0.3), random.randint(0, 2)
    elif kind == 4:                              # 中間有 11 列厚的整面牆、K = 10：到不了，但上半部狀態全被走過
        g = rand_grid(R, C, 0.2)
        for x in range(240, 251):
            g[x] = ['#'] * C
        K = 10
    else:                                        # 完全沒有牆、K = 10，答案 998
        g, K = [['.'] * C for _ in range(R)], 10
    emit(K, g)
