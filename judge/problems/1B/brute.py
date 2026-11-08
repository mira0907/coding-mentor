"""範例 1-B 三角形計數的暴力解：用鄰接矩陣列舉所有三點組。"""
import sys
from itertools import combinations

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
adj = [[False] * (n + 1) for _ in range(n + 1)]     # adj[u][v] = u、v 是否相鄰
for i in range(m):
    u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
    adj[u][v] = adj[v][u] = True
# 每個三點組 a < b < c 檢查三條邊是否都在
print(sum(1 for a, b, c in combinations(range(1, n + 1), 3) if adj[a][b] and adj[b][c] and adj[a][c]))
