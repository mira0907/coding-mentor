"""範例 8-A 的暴力解：依序替每位員工決定「不做」或「做某項還沒人做的工作」，窮舉所有分法取最多。"""
import sys
from functools import lru_cache


def main():
    data = sys.stdin.read().split()
    nL, nR, E = int(data[0]), int(data[1]), int(data[2])
    can = [[] for _ in range(nL + 1)]          # can[u] = 員工 u 會做的工作
    for i in range(E):
        can[int(data[3 + 2 * i])].append(int(data[4 + 2 * i]))

    @lru_cache(maxsize=None)
    def best(u, used):
        """員工 u..nL 還沒安排、used 是已被做的工作（位元）時，最多還能完成幾項"""
        if u > nL:
            return 0
        r = best(u + 1, used)                  # 員工 u 不做
        for v in can[u]:
            if not used >> v & 1:
                r = max(r, 1 + best(u + 1, used | 1 << v))
        return r

    print(best(1, 0))


main()
