"""範例 2-A 騎士巡邏的暴力解：反覆鬆弛每一格的步數，直到不再變小（不用佇列）。"""
import sys

N, sx, sy, tx, ty = map(int, sys.stdin.read().split())
INF = float("inf")
d = {(x, y): INF for x in range(1, N + 1) for y in range(1, N + 1)}   # d[格子] = 目前已知最少步數
d[(sx, sy)] = 0
moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
changed = True
while changed:                                   # 一輪掃過所有格子，有變小就再掃一輪
    changed = False
    for (x, y), k in d.items():
        if k == INF:
            continue
        for dx, dy in moves:
            p = (x + dx, y + dy)
            if p in d and d[p] > k + 1:
                d[p] = k + 1
                changed = True
print(-1 if d[(tx, ty)] == INF else d[(tx, ty)])
