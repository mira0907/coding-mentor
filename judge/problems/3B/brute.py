"""範例 3-B 的暴力解：列舉城市 1 到 n 的所有簡單路徑，每條路徑把最貴的 K 段免費，取最小花費。
繞路只會多出航線，不會更便宜，所以只看簡單路徑就夠了。只用在 n ≤ 7 的小測資。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m, K = int(data[0]), int(data[1]), int(data[2])
    adj = [[] for _ in range(n + 1)]             # adj[u] = (v, w)
    for i in range(m):
        u, v, w = int(data[3 + 3 * i]), int(data[4 + 3 * i]), int(data[5 + 3 * i])
        adj[u].append((v, w))
        adj[v].append((u, w))
    best = [None]

    def dfs(u, vis, ws):
        if u == n:                               # 到達終點：最貴的 K 段用券
            cost = sum(sorted(ws)[:max(0, len(ws) - K)])
            if best[0] is None or cost < best[0]:
                best[0] = cost
            return
        for v, w in adj[u]:
            if not vis[v]:
                vis[v] = True
                ws.append(w)
                dfs(v, vis, ws)
                ws.pop()
                vis[v] = False

    vis = [False] * (n + 1)
    vis[1] = True
    dfs(1, vis, [])
    print(-1 if best[0] is None else best[0])


main()
