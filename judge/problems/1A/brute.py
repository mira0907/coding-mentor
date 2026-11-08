"""範例 1-A 握手統計的暴力解：對每個人掃過所有握手，數他出現幾次。"""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
# 每個人逐一數：這次握手有他就加一
deg = [sum((u == i) + (v == i) for u, v in edges) for i in range(1, n + 1)]
print(" ".join(map(str, deg)))
print(sum(1 for d in deg if d % 2 == 1))
