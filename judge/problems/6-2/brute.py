# 暴力解（n <= 5）：
# 問題一：由小到大枚舉要直接通知的學校集合，找最小的、能傳遍全部的集合。
# 問題二：已經強連通就是 0；否則 k = 1, 2, ... 枚舉所有「k 條新線路」的組合，
#         找最小的 k 使加完後整張圖強連通。完全不用 SCC 的理論。
import sys
from itertools import combinations

def closure(n, out, start_mask):
    # 從 start_mask 這些點出發走得到的點（位元遮罩，點 0..n-1）
    seen = start_mask
    frontier = start_mask
    while frontier:
        nxt = 0
        for v in range(n):
            if frontier >> v & 1:
                nxt |= out[v]
        nxt &= ~seen
        seen |= nxt
        frontier = nxt
    return seen

def strongly(n, out):
    full = (1 << n) - 1
    for v in range(n):
        if closure(n, out, 1 << v) != full:
            return False
    return True

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    out = [0] * n
    for i in range(m):
        u, v = int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]) - 1
        out[u] |= 1 << v
    full = (1 << n) - 1
    a1 = None
    for k in range(1, n + 1):
        for S in combinations(range(n), k):
            mask = 0
            for v in S:
                mask |= 1 << v
            if closure(n, out, mask) == full:
                a1 = k
                break
        if a1 is not None:
            break
    if strongly(n, out):
        a2 = 0
    else:
        pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
        a2 = None
        k = 1
        while a2 is None:
            for add in combinations(pairs, k):
                o2 = out[:]
                for u, v in add:
                    o2[u] |= 1 << v
                if strongly(n, o2):
                    a2 = k
                    break
            k += 1
    print(a1, a2)

main()
