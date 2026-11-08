"""範例 4-A 村莊供電的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 6、m ≤ 8），max 用題目上限並依 seed 換不同形狀。
題目沒說可以有自環或重複電線，所以一律產生簡單無向圖。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])
W = 10**9                                      # 花費上限


def emit(c, edges):
    """印出一筆測資：c[i] 是村莊 i+1 蓋發電廠的花費，edges 是 (u, v, w) 的清單（順序與方向打亂）"""
    random.shuffle(edges)
    print(len(c), len(edges))
    print(" ".join(map(str, c)))
    print("\n".join(f"{u} {v} {w}" if random.random() < 0.5 else f"{v} {u} {w}" for u, v, w in edges))


def pairs(n, m, sample=None):
    """隨機挑至多 m 條不重複、不是自環的無向邊 (u, v)，u < v；sample() 可指定怎麼抽一個點對"""
    if n * (n - 1) // 2 <= 2 * m:                # 小圖：從所有點對裡抽
        cand = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
        random.shuffle(cand)
        return cand[:m]
    used, res = set(), []
    while len(res) < m:
        u, v = sample() if sample else (random.randint(1, n), random.randint(1, n))
        u, v = min(u, v), max(u, v)
        if u != v and (u, v) not in used:
            used.add((u, v))
            res.append((u, v))
    return res


if size == "small":
    style = seed % 5
    n = random.randint(2, 6)
    full = n * (n - 1) // 2                      # 簡單無向圖最多幾條邊
    m = random.randint(min(full, n - 1), min(8, full))
    if style == 0:                               # 沒有電線：每個村莊都要自己蓋；seed 5 是 n = 1
        emit([random.randint(1, 10) for _ in range(1 if seed == 5 else n)], [])
    elif style == 1:                             # 電線便宜、發電廠貴：只蓋一座
        emit([random.randint(5, 10) for _ in range(n)], [(u, v, random.randint(1, 4)) for u, v in pairs(n, m)])
    elif style == 2:                             # 電線貴、發電廠便宜：多蓋幾座比較划算
        emit([random.randint(1, 4) for _ in range(n)], [(u, v, random.randint(2, 8)) for u, v in pairs(n, m)])
    elif style == 3:                             # 花費都接近 10⁹，總和超過 int
        emit([random.randint(W - 3, W) for _ in range(n)], [(u, v, random.randint(W - 3, W)) for u, v in pairs(n, m)])
    else:                                        # 小範圍隨機，很多平手
        emit([random.randint(1, 3) for _ in range(n)], [(u, v, random.randint(1, 3)) for u, v in pairs(n, m)])
elif size == "mid":
    n, m = 2000, 6000
    k = [1, 5, 50][seed % 3]                     # 電線花費約是發電廠的 1/k
    emit([random.randint(1, W) for _ in range(n)], [(u, v, random.randint(1, W // k)) for u, v in pairs(n, m)])
else:
    n, m = 100000, 200000
    style = (seed - 1) % 5
    if style == 0:                               # 隨機圖，花費隨機到 10⁹
        emit([random.randint(1, W) for _ in range(n)], [(u, v, random.randint(1, W)) for u, v in pairs(n, m)])
    elif style == 1:                             # 長鏈 1–2–…–n 加相近村莊的電線，花費全是 10⁹：答案 10¹⁴，int 會溢位
        chain = [(i, i + 1) for i in range(1, n)]
        local = lambda: (lambda u: (u, u + random.randint(2, 5)))(random.randint(1, n - 5))
        extra = pairs(n, m - len(chain), local)   # 相距 2..5，不會和鏈重複
        emit([W] * n, [(u, v, W) for u, v in chain + extra])
    elif style == 2:                             # 星狀：中心發電廠便宜，葉子之間也有電線
        c = [1] + [random.randint(1, W) for _ in range(n - 1)]
        star = [(1, v, random.randint(1, W)) for v in range(2, n + 1)]
        leaf = lambda: (random.randint(2, n), random.randint(2, n))
        extra = [(u, v, random.randint(1, W)) for u, v in pairs(n, m - len(star), leaf)]
        emit(c, star + extra)
    elif style == 3:                             # 花費全部相同：大量平手
        emit([7] * n, [(u, v, 7) for u, v in pairs(n, m)])
    else:                                        # 很多連通塊（每塊 10 個村莊），每塊都要自己的發電廠
        blk = lambda: (lambda b: (b * 10 + random.randint(1, 10), b * 10 + random.randint(1, 10)))(random.randrange(n // 10))
        emit([random.randint(W // 2, W) for _ in range(n)], [(u, v, random.randint(1, W // 1000)) for u, v in pairs(n, 20 * (n // 10), blk)])
