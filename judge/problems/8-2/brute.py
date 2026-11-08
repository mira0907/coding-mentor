"""實作 8-2 的暴力解：從每個路口出發，窮舉所有「每條街道恰好走一次」的走法，取字典序最小的路口序列。"""
import sys

sys.setrecursionlimit(10000)


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    inc = [[] for _ in range(n + 1)]           # inc[u] = (走過去會到的路口, 街道編號)
    for i in range(m):
        u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        inc[u].append((v, i))
        if u != v:
            inc[v].append((u, i))
    best = None                                # 目前找到字典序最小的完整路線
    used = [False] * m                         # used[i] = 街道 i 是否已經走過
    seq = []                                   # 目前走過的路口序列

    def dfs(u, cnt):
        nonlocal best
        if cnt == m:
            t = tuple(seq)
            if best is None or t < best:
                best = t
            return
        for v, i in inc[u]:
            if not used[i]:
                used[i] = True
                seq.append(v)
                dfs(v, cnt + 1)
                seq.pop()
                used[i] = False

    for s in range(1, n + 1):
        seq.append(s)
        dfs(s, 0)
        seq.pop()
    print(-1 if best is None else " ".join(map(str, best)))


main()
