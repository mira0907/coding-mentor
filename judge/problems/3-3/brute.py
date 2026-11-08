"""實作 3-3 的暴力解：列舉 s 到 t 的所有簡單路徑（重複道路分開算），
找出長度最短的那些路線，再數每條道路出現在幾條最短路線上。只用在 n ≤ 7、m ≤ 14 的小測資。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m, s, t = map(int, data[:4])
    E = [(int(data[4 + 3 * i]), int(data[5 + 3 * i]), int(data[6 + 3 * i])) for i in range(m)]
    out = [[] for _ in range(n + 1)]             # out[u] = 從 u 出發的道路編號
    for i, (u, v, w) in enumerate(E):
        out[u].append(i)
    paths = []                                   # 每條簡單路線的 (長度, 經過的道路編號)
    vis = [False] * (n + 1)

    def dfs(u, length, used):
        if u == t:
            paths.append((length, list(used)))
            return
        for i in out[u]:
            v = E[i][1]
            if vis[v]:
                continue
            vis[v] = True
            used.append(i)
            dfs(v, length + E[i][2], used)
            used.pop()
            vis[v] = False

    vis[s] = True
    dfs(s, 0, [])
    res = ["NONE"] * m
    if paths:
        D = min(l for l, _ in paths)
        best = [set(ids) for l, ids in paths if l == D]   # 所有最短路線
        for i in range(m):
            c = sum(1 for b in best if i in b)            # 第 i 條道路在幾條最短路線上
            if c == len(best):
                res[i] = "ALL"
            elif c > 0:
                res[i] = "SOME"
    print("\n".join(res))


main()
