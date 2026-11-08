"""實作 3-2 的暴力解：列舉點 1 到點 n 的所有簡單路徑（重邊分開走），記下最短長度與條數。
邊權都是正的，最短路一定是簡單路徑。只用在 n ≤ 7 的小測資。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]             # adj[u] = (v, w)，每條邊各存一次
    for i in range(m):
        u, v, w = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
        adj[u].append((v, w))
        adj[v].append((u, w))
    best = [None, 0]                             # [最短長度, 條數]

    def dfs(u, vis, d):
        if u == n:
            if best[0] is None or d < best[0]:
                best[0], best[1] = d, 1
            elif d == best[0]:
                best[1] += 1
            return
        for v, w in adj[u]:
            if not vis[v]:
                vis[v] = True
                dfs(v, vis, d + w)
                vis[v] = False

    vis = [False] * (n + 1)
    vis[1] = True
    dfs(1, vis, 0)
    print(-1 if best[0] is None else f"{best[0]} {best[1] % (10**9 + 7)}")


main()
