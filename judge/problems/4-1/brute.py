"""實作 4-1 的暴力解：用 BFS 數連通塊，k 個連通塊至少要再修 k − 1 條路。"""
import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]             # adj[u] = u 的鄰居
    for i in range(m):
        u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * (n + 1)
    comps = 0                                    # 連通塊個數
    for s in range(1, n + 1):
        if not seen[s]:
            comps += 1
            seen[s] = True
            q = deque([s])
            while q:
                x = q.popleft()
                for y in adj[x]:
                    if not seen[y]:
                        seen[y] = True
                        q.append(y)
    print(comps - 1)


main()
