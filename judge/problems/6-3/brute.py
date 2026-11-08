"""實作 6-3 的暴力解：狀態 = (目前所在房間, 已經拿過寶石的房間集合)，
從 (1, {1}) 開始 BFS 走遍所有狀態，取集合寶石總和的最大值。"""
import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]          # a[i] = 房間 i+1 的寶石數
    adj = [[] for _ in range(n)]                 # adj[u] = u 可以走到的房間（從 0 起算）
    for k in range(m):
        u, v = int(data[2 + n + 2 * k]) - 1, int(data[3 + n + 2 * k]) - 1
        adj[u].append(v)
    start = (0, 1)                               # 在房間 1、拿過房間 1
    seen = {start}
    dq = deque([start])
    best = 0
    while dq:
        u, mask = dq.popleft()
        best = max(best, sum(a[i] for i in range(n) if mask >> i & 1))
        for v in adj[u]:
            s = (v, mask | 1 << v)
            if s not in seen:
                seen.add(s)
                dq.append(s)
    print(best)


main()
