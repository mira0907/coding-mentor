"""實作 8-3 騎士共存的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（R·C ≤ 24），max 用 200 × 200 並依 seed 換不同形狀。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(rows):
    """印出一筆測資；rows 是每列的字串"""
    print(f"{len(rows)} {len(rows[0])}")
    print("\n".join(rows))


def rand_board(R, C, p):
    """每格以機率 p 壞掉的隨機棋盤"""
    return ["".join('#' if random.random() < p else '.' for _ in range(C)) for _ in range(R)]


if size == "small":
    if seed == 1:                              # 最小：1 × 1 的好格子
        emit(["."])
    elif seed == 2:                            # 全部壞掉，答案 0
        R, C = random.randint(1, 4), random.randint(1, 4)
        emit(["#" * C] * R)
    elif seed == 3:                            # 單一列：騎士互相打不到
        emit(rand_board(1, random.randint(2, 20), 0.1))
    elif seed == 4:                            # 2 × C：只有隔兩行的格子會互相攻擊
        emit(rand_board(2, random.randint(3, 12), 0.0))
    else:
        while True:
            R, C = random.randint(1, 6), random.randint(1, 6)
            if R * C <= 24:
                break
        emit(rand_board(R, C, random.choice([0.0, 0.1, 0.25, 0.4, 0.7])))
elif size == "mid":
    emit(rand_board(random.randint(40, 60), random.randint(40, 60), random.choice([0.0, 0.1, 0.3])))
else:
    R = C = 200
    kind = (seed - 1) % 5
    if kind == 0:                              # 全部是好格子：答案 20000，最大匹配最大
        emit(["." * C] * R)
    elif kind == 1:                            # 一成格子壞掉：最大流要繞路
        emit(rand_board(R, C, 0.1))
    elif kind == 2:                            # 每隔兩行一條壞掉的直線
        emit(["".join('#' if c % 3 == 2 else '.' for c in range(C)) for _ in range(R)])
    elif kind == 3:                            # 只剩同色格：沒有任何攻擊，答案 = 好格子數
        emit(["".join('.' if (r + c) % 2 == 0 else '#' for c in range(C)) for r in range(R)])
    else:                                      # 一半格子壞掉
        emit(rand_board(R, C, 0.5))
