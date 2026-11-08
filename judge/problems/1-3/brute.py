"""實作 1-3 停駛的渡輪的暴力解：直接建出補圖（還在開的航線），再用並查集合併。"""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
stopped = [[False] * (n + 1) for _ in range(n + 1)]   # stopped[u][v] = u–v 是否停駛
for i in range(m):
    u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
    stopped[u][v] = stopped[v][u] = True
par = list(range(n + 1))                              # 並查集的父節點


def find(x):
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x


# 每對沒停駛的島合併成同一圈
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        if not stopped[u][v]:
            par[find(u)] = find(v)
cnt = {}                                              # 每個代表元底下的島數
for u in range(1, n + 1):
    r = find(u)
    cnt[r] = cnt.get(r, 0) + 1
sizes = sorted(cnt.values())
print(len(sizes))
print(" ".join(map(str, sizes)))
