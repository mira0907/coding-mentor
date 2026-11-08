"""範例 6-B 的暴力解：枚舉全部 2^n 種設定（字典序由小到大），輸出第一組滿足所有條件的；
都不滿足就輸出 IMPOSSIBLE。"""
import itertools
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    cl = [tuple(int(v) for v in data[2 + 4 * k: 6 + 4 * k]) for k in range(m)]   # (i, a, j, b)
    for x in itertools.product((0, 1), repeat=n):
        if all(x[i - 1] == a or x[j - 1] == b for i, a, j, b in cl):
            print("".join(map(str, x)))
            return
    print("IMPOSSIBLE")


main()
