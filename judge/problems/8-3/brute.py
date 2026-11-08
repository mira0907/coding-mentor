"""實作 8-3 的暴力解：直接在騎士攻擊圖上求最大獨立集。
每次取編號最小的格子，分「不放」與「放（並刪掉它攻擊得到的格子）」兩種情況，用位元遮罩記憶化。"""
import sys
from functools import lru_cache


def main():
    data = sys.stdin.read().split()
    R, C = int(data[0]), int(data[1])
    b = data[2:2 + R]
    cells = [(r, c) for r in range(R) for c in range(C) if b[r][c] == '.']   # 所有好格子
    idx = {cell: i for i, cell in enumerate(cells)}
    nb = [0] * len(cells)                      # nb[i] = 格子 i 攻擊得到的好格子（位元）
    for i, (r, c) in enumerate(cells):
        for dr, dc in ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)):
            j = idx.get((r + dr, c + dc))
            if j is not None:
                nb[i] |= 1 << j

    @lru_cache(maxsize=None)
    def mis(mask):
        """mask 這些格子裡最多能放幾個互不攻擊的騎士"""
        if mask == 0:
            return 0
        v = (mask & -mask).bit_length() - 1    # v = 編號最小的格子
        rest = mask & ~(1 << v)
        if nb[v] & rest == 0:                  # v 打不到任何剩下的格子，放了一定不吃虧
            return 1 + mis(rest)
        return max(mis(rest), 1 + mis(rest & ~nb[v]))

    print(mis((1 << len(cells)) - 1))


main()
