"""範例 8-B 的暴力解：枚舉所有專案子集（2^n 種），買下用到的工具，取淨利最大者。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    p = [int(x) for x in data[2:2 + n]]        # p[i] = 專案 i + 1 的獲利
    c = [int(x) for x in data[2 + n:2 + n + m]]   # c[j] = 工具 j + 1 的價格
    pos = 2 + n + m
    need = []                                  # need[i] = 專案 i + 1 需要的工具（位元）
    for _ in range(n):
        k = int(data[pos])
        bits = 0
        for j in data[pos + 1:pos + 1 + k]:
            bits |= 1 << (int(j) - 1)
        need.append(bits)
        pos += 1 + k
    best = 0                                   # 什麼都不做的淨利是 0
    for mask in range(1 << n):
        tools, gain = 0, 0
        for i in range(n):
            if mask >> i & 1:
                tools |= need[i]
                gain += p[i]
        best = max(best, gain - sum(c[j] for j in range(m) if tools >> j & 1))
    print(best)


main()
