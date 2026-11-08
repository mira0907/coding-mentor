"""範例 5-A 的暴力解：照字典序枚舉 1..n 的所有排列，第一個符合全部先修關係的就是答案。"""
import itertools
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
    for p in itertools.permutations(range(1, n + 1)):   # permutations 依字典序產生
        pos = {v: i for i, v in enumerate(p)}           # pos[v] = 課 v 排在第幾個
        if all(pos[a] < pos[b] for a, b in edges):
            print(" ".join(map(str, p)))
            return
    print("IMPOSSIBLE")                                  # 沒有任何排列合法


main()
