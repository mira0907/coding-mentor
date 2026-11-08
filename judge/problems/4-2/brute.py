"""實作 4-2 的暴力解：每筆詢問各自只留下耐風等級 ≥ x 的道路，從 v 做一次 BFS 數走得到的鄉鎮。"""
import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n, m, q = int(data[0]), int(data[1]), int(data[2])
    p = 3
    E = []                                       # E = 所有道路 (u, v, w)
    for _ in range(m):
        E.append((int(data[p]), int(data[p + 1]), int(data[p + 2])))
        p += 3
    out = []
    for _ in range(q):
        v, x = int(data[p]), int(data[p + 1])
        p += 2
        adj = [[] for _ in range(n + 1)]         # 這次颱風還能走的道路
        for a, b, w in E:
            if w >= x:
                adj[a].append(b)
                adj[b].append(a)
        seen = [False] * (n + 1)
        seen[v] = True
        dq = deque([v])
        cnt = 0                                  # 走得到的鄉鎮數
        while dq:
            u = dq.popleft()
            cnt += 1
            for y in adj[u]:
                if not seen[y]:
                    seen[y] = True
                    dq.append(y)
        out.append(str(cnt))
    print("\n".join(out))


main()
