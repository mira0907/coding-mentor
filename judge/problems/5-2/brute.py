"""實作 5-2 的暴力解：先用三色 DFS 找環（有環輸出 -1），
再用記憶化遞迴求「從 u 開工到後續全部做完」的最長天數，取最大值。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    t = [0] + [int(x) for x in data[2:2 + n]]   # t[i] = 工作 i 的天數
    adj = [[] for _ in range(n + 1)]            # adj[a] = 要等 a 的工作
    p = 2 + n
    for _ in range(m):
        adj[int(data[p])].append(int(data[p + 1]))
        p += 2
    sys.setrecursionlimit(10000)
    color = [0] * (n + 1)                       # 0 = 沒走過、1 = 在遞迴中、2 = 做完
    cyc = [False]

    def dfs(u):
        color[u] = 1
        for v in adj[u]:
            if color[v] == 1:
                cyc[0] = True                   # 走回遞迴中的點 → 有環
            elif color[v] == 0:
                dfs(v)
        color[u] = 2

    for i in range(1, n + 1):
        if color[i] == 0:
            dfs(i)
    if cyc[0]:
        print(-1)
        return
    memo = {}

    def longest(u):                             # 從 u 開工，到 u 之後的工作全做完要幾天
        if u not in memo:
            memo[u] = t[u] + max([longest(v) for v in adj[u]], default=0)
        return memo[u]

    print(max(longest(i) for i in range(1, n + 1)))


main()
