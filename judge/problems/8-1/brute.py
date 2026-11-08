"""實作 8-1 的暴力解：依字典序列舉所有 2^n 種分法，第一個讓每組都不同隊的就是答案。"""
import sys
from itertools import product


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
    for t in product([1, 2], repeat=n):        # product 依字典序產生 (1,…,1)、(1,…,2)、…
        if all(t[u - 1] != t[v - 1] for u, v in edges):
            print("YES")
            print(" ".join(map(str, t)))
            return
    print("NO")


main()
