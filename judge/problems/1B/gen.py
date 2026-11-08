"""範例 1-B 三角形計數的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 8），max 用題目上限並依 seed 換不同形狀。
題目保證是簡單圖，所以每種形狀都不產生重邊與自環。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def emit(n, edges):
    """印出一筆測資：邊的順序打亂、兩端隨機對調"""
    edges = list(edges)
    random.shuffle(edges)
    print(n, len(edges))
    if edges:
        print("\n".join(f"{u} {v}" if random.random() < 0.5 else f"{v} {u}" for u, v in edges))


def add_random(n, es, m):
    """在集合 es 裡補隨機邊，直到有 m 條（存成小編號在前）"""
    while len(es) < m:
        u, v = random.sample(range(1, n + 1), 2)
        es.add((min(u, v), max(u, v)))
    return es


if size == "small":
    n = 1 if seed == 1 else random.randint(2, 8)
    pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    mode = seed % 4
    if mode == 0:                                # 完全圖或幾乎完全圖
        es = [p for p in pairs if random.random() < 0.9]
    elif mode == 1:                              # 沒有邊（seed = 1 時 n = 1）
        es = []
    elif mode == 2:                              # 稀疏
        es = [p for p in pairs if random.random() < 0.3]
    else:                                        # 中等密度
        es = [p for p in pairs if random.random() < 0.6]
    emit(n, es)
elif size == "mid":
    n = 2000
    es = set()
    k = random.randint(30, 60)                   # 一團幾乎完全的點，製造很多三角形
    for u in range(1, k + 1):
        for v in range(u + 1, k + 1):
            if random.random() < 0.8:
                es.add((u, v))
    emit(n, add_random(n, es, len(es) + 8000))
else:
    n, m = 100000, 200000
    kind = seed % 4
    es = set()
    if kind == 1:                                # 稠密核心：632 點的完全圖約 2×10⁵ 條邊，三角形約 4×10⁷ 個
        core = 632
        for u in range(1, core + 1):
            for v in range(u + 1, core + 1):
                if len(es) < m - 1000:
                    es.add((u, v))
        add_random(n, es, m)
    elif kind == 2:                              # 兩個超級中心（編號在 n/3、2n/3）連到所有人，且彼此相連
        h1, h2 = n // 3, 2 * n // 3              # 只按編號定向的寫法，中心的出入度都很大，會很慢
        es.add((h1, h2))
        for v in range(1, n + 1):
            if v != h1 and v != h2:
                es.add((min(h1, v), max(h1, v)))
                es.add((min(h2, v), max(h2, v)))
    elif kind == 3:                              # 隨機圖
        add_random(n, es, m)
    else:                                        # 第 1 點連到所有人，再加隨機邊
        for v in range(2, n + 1):
            es.add((1, v))
        add_random(n, es, m)
    emit(n, es)
