# 暴力解：用大整數算「長度恰為 L 的 1 → n 走法數」，L = 0 .. 2n。
# 若存在長度在 [n, 2n] 的走法，代表走法中有重複的點，可以繞圈 → INFINITE。
# 否則每條走法都是簡單路徑（長度 <= n - 1），答案是 L = 0 .. n-1 的總和取餘數。
import sys

MOD = 10**9 + 7

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
    cur = [0] * (n + 1)
    cur[1] = 1
    by_len = [cur[n]]
    for L in range(1, 2 * n + 1):
        nxt = [0] * (n + 1)
        for u, v in edges:
            nxt[v] += cur[u]
        cur = nxt
        by_len.append(cur[n])
    if any(by_len[L] > 0 for L in range(n, 2 * n + 1)):
        print("INFINITE")
    else:
        print(sum(by_len[:n]) % MOD)

main()
