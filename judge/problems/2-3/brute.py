"""實作 2-3 停機檢修的暴力解：每筆詢問都把 x 拿掉，從 u 做一次 BFS 看能不能到 v。"""
import sys
from collections import deque

data = sys.stdin.read().split()
n, q = int(data[0]), int(data[1])
p = 2
adj = [[] for _ in range(n + 1)]                 # adj[a] = 和 a 相連的伺服器
for _ in range(n - 1):
    a, b = int(data[p]), int(data[p + 1])
    p += 2
    adj[a].append(b)
    adj[b].append(a)
out = []
for _ in range(q):
    x, u, v = int(data[p]), int(data[p + 1]), int(data[p + 2])
    p += 3
    if u == x or v == x:                         # 關機的伺服器本身不能通訊
        out.append("NO")
        continue
    seen = [False] * (n + 1)                     # x 先標記成走過，等於把它拿掉
    seen[x] = seen[u] = True
    dq = deque([u])
    while dq:
        a = dq.popleft()
        for b in adj[a]:
            if not seen[b]:
                seen[b] = True
                dq.append(b)
    out.append("YES" if seen[v] else "NO")
print("\n".join(out))
