"""實作 2-2 夜市火災的暴力解：一分鐘一分鐘模擬火的範圍，以及你在這一分鐘可能站的所有位置。"""
import sys

data = sys.stdin.read().split()
R, C = int(data[0]), int(data[1])
g = data[2:2 + R]
fire = set()                                     # 目前著火的格子
S = None                                         # 你的起點
for x in range(R):
    for y in range(C):
        if g[x][y] == 'F':
            fire.add((x, y))
        if g[x][y] == 'S':
            S = (x, y)


def nbrs(x, y):
    """(x, y) 上下左右、在地圖內且不是牆的格子"""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < R and 0 <= ny < C and g[nx][ny] != '#':
            yield (nx, ny)


P = {S}                                          # 第 t 分鐘你可能站的位置
ans = -1
for t in range(R * C + 5):
    if any(x == 0 or x == R - 1 or y == 0 or y == C - 1 for (x, y) in P):
        ans = t + 1                              # 站在外圈，再一分鐘就出去
        break
    newfire = set(fire)                          # 這一分鐘火蔓延後的範圍
    for (x, y) in fire:
        newfire.update(nbrs(x, y))
    # 你同時移動一格，不能走進這一分鐘（含）以前著火的格子
    P = {q for (x, y) in P for q in nbrs(x, y) if q not in newfire}
    fire = newfire
    if not P:
        break
print(ans)
