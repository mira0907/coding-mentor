"""實作 7-2 的暴力解：枚舉所有「哪些路口裝監視器」的組合（2^n 種），取能拍到每條道路的最便宜組合。"""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    c = [int(x) for x in data[1:1 + n]]        # c[i] = 路口 i + 1 的費用
    edges = []                                 # 道路，路口編號從 0 開始
    p = 1 + n
    for _ in range(n - 1):
        edges.append((int(data[p]) - 1, int(data[p + 1]) - 1))
        p += 2
    best = None
    for mask in range(1 << n):                 # mask 的第 i 位 = 路口 i + 1 有沒有裝
        if all(mask >> u & 1 or mask >> v & 1 for u, v in edges):
            cost = sum(c[i] for i in range(n) if mask >> i & 1)
            if best is None or cost < best:
                best = cost
    print(best)


main()
