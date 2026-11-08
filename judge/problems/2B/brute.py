"""範例 2-B 破牆迷宮的暴力解：列舉要拆掉哪幾面牆，拆掉後做普通 BFS，取最短。
最短路徑不會重複經過同一格，所以「打破 ≤ K 次」等於「事先拆掉 ≤ K 面牆」；
多拆不會變差，所以只列舉剛好 min(K, 牆數) 面。"""
import sys
from collections import deque
from itertools import combinations

data = sys.stdin.read().split()
R, C, K = int(data[0]), int(data[1]), int(data[2])
g = data[3:3 + R]
walls = [(x, y) for x in range(R) for y in range(C) if g[x][y] == '#']


def bfs(removed):
    """拆掉 removed 這些牆後，左上到右下的最短步數，到不了回傳 None"""
    dist = {(0, 0): 0}
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        if (x, y) == (R - 1, C - 1):
            return dist[(x, y)]
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < R and 0 <= ny < C and (nx, ny) not in dist:
                if g[nx][ny] == '#' and (nx, ny) not in removed:
                    continue
                dist[(nx, ny)] = dist[(x, y)] + 1
                q.append((nx, ny))
    return None


best = None
for sub in combinations(walls, min(K, len(walls))):
    d = bfs(set(sub))
    if d is not None and (best is None or d < best):
        best = d
print(-1 if best is None else best)
