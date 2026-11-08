"""實作 1-1 整理路網的暴力解：用計數鄰接矩陣記每對路口被記了幾次。"""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
cnt = [[0] * (n + 1) for _ in range(n + 1)]     # cnt[u][v] = u、v 之間被記了幾次（不含自環）
loops = 0                                        # 自環條數
for i in range(m):
    u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
    if u == v:
        loops += 1
    else:
        cnt[u][v] += 1
        cnt[v][u] += 1
# 每對路口記了 k 次，多出 k − 1 次
dup = sum(cnt[u][v] - 1 for u in range(1, n + 1) for v in range(u + 1, n + 1) if cnt[u][v] > 1)
# 整理後的度數 = 有被記過的鄰居個數
deg = [sum(1 for v in range(1, n + 1) if cnt[u][v] > 0) for u in range(1, n + 1)]
print(loops, dup)
print(" ".join(map(str, deg)))
