"""實作 2-3 停機檢修的測資產生器。
用法：python3 -I gen.py SEED SIZE，SIZE 是 small、mid 或 max。
small 給暴力解驗證用（n ≤ 10），max 用 n = q = 2×10⁵ 並依 seed 換不同形狀的樹。"""
import random
import sys

seed, size = int(sys.argv[1]), sys.argv[2]     # seed = 亂數種子，size = 測資規模
random.seed(seed * 1000 + {"small": 1, "mid": 2, "max": 3}[size])


def tree(n, mode):
    """產生 n 個點的樹，回傳 (父, 子) 清單：0 隨機、1 鏈、2 星形、3 毛毛蟲（父節點在前三個以內）"""
    edges = []
    for v in range(2, n + 1):
        if mode == 0:
            p = random.randint(1, v - 1)
        elif mode == 1:
            p = v - 1
        elif mode == 2:
            p = 1
        else:
            p = random.randint(max(1, v - 3), v - 1)
        edges.append((p, v))
    return edges


def relabel(n, edges):
    """把點的編號打亂，讓點 1 不一定是產生時的根"""
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    lab = [0] + perm
    return [(lab[a], lab[b]) for a, b in edges], lab


def emit(n, edges, queries):
    """印出一筆測資：邊的順序打亂、兩端隨機對調"""
    random.shuffle(edges)
    out = [f"{n} {len(queries)}"]
    out += [f"{a} {b}" if random.random() < 0.5 else f"{b} {a}" for a, b in edges]
    out += [f"{x} {u} {v}" for x, u, v in queries]
    print("\n".join(out))


def rand_query(n, hot=None):
    """隨機詢問；hot 不是 None 時關機的一律是 hot。約 10% u = v，約 10% u = x"""
    x = hot if hot is not None else random.randint(1, n)
    u = random.randint(1, n)
    v = u if random.random() < 0.1 else random.randint(1, n)
    if random.random() < 0.1:
        u = x
    return x, u, v


if size == "small":
    if seed == 1:                                # 只有一台：關掉自己，一定是 NO
        print("1 1\n1 1 1")
        sys.exit()
    n = random.randint(2, 10)
    q = random.randint(1, 15)
    edges, _ = relabel(n, tree(n, seed % 4))
    emit(n, edges, [rand_query(n) for _ in range(q)])
elif size == "mid":
    n = q = 2000
    edges, lab = relabel(n, tree(n, seed % 4))
    hot = lab[1] if seed % 4 == 2 else None      # 星形時多數詢問關掉中心
    emit(n, edges, [rand_query(n, hot if random.random() < 0.7 else None) for _ in range(q)])
else:
    n = q = 200000
    kind = seed % 5
    hot = None                                   # 大部分詢問要關掉的點
    if kind == 1:                                # 長鏈 1 − 2 − … − n，深度 2×10⁵
        edges = [(i, i + 1) for i in range(1, n)]
    elif kind == 2:                              # 星形，詢問都關掉中心 1：子節點很多，要二分搜尋
        edges = [(1, i) for i in range(2, n + 1)]
        hot = 1
    elif kind == 3:                              # 隨機樹
        edges = [(random.randint(1, i - 1), i) for i in range(2, n + 1)]
    elif kind == 4:                              # 掃帚：前半是鏈，尾端接一個大星形，一半詢問關掉接點
        h = n // 2
        edges = [(i, i + 1) for i in range(1, h)] + [(h, i) for i in range(h + 1, n + 1)]
        hot = h
    else:                                        # 鏈，但點 1 在正中間（從 1 出發往兩邊各 10⁵ 深）
        order = list(range(2, n + 1))
        random.shuffle(order)
        order.insert(n // 2, 1)
        edges = [(order[i], order[i + 1]) for i in range(n - 1)]
    queries = []
    for _ in range(q):
        queries.append(rand_query(n, hot if hot is not None and (kind == 2 or random.random() < 0.5) else None))
    emit(n, edges, queries)
