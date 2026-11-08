"""實作 2-1 島嶼探險的暴力解：用並查集把上下左右相鄰的陸地合併，再數每組的大小。"""
import sys

data = sys.stdin.read().split()
R, C = int(data[0]), int(data[1])
g = data[2:2 + R]
par = list(range(R * C))                         # 並查集，格子 (x, y) 的編號是 x * C + y


def find(a):
    while par[a] != a:
        par[a] = par[par[a]]
        a = par[a]
    return a


# 每格陸地和右邊、下面的陸地合併
for x in range(R):
    for y in range(C):
        if g[x][y] != '#':
            continue
        if y + 1 < C and g[x][y + 1] == '#':
            par[find(x * C + y)] = find(x * C + y + 1)
        if x + 1 < R and g[x + 1][y] == '#':
            par[find(x * C + y)] = find((x + 1) * C + y)
size = {}                                        # 每個代表元底下的陸地格數
for x in range(R):
    for y in range(C):
        if g[x][y] == '#':
            r = find(x * C + y)
            size[r] = size.get(r, 0) + 1
print(len(size), max(size.values(), default=0))
