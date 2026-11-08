"""實作 7-3 的暴力解：每筆配送都從 u 走遍整棵樹找出到 v 的路徑，路徑上每個站點加 1。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]           # adj[u] = 和 u 相鄰的站點
    p = 2
    for _ in range(n - 1):
        u, v = int(data[p]), int(data[p + 1])
        p += 2
        adj[u].append(v)
        adj[v].append(u)
    cnt = [0] * (n + 1)                        # cnt[x] = 站點 x 的工作量
    for _ in range(q):
        u, v = int(data[p]), int(data[p + 1])
        p += 2
        par = {u: None}                        # 以 u 為根的父節點
        st = [u]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in par:
                    par[y] = x
                    st.append(y)
        x = v
        while x is not None:                   # 從 v 沿父節點走回 u，路上每站加 1
            cnt[x] += 1
            x = par[x]
    print(max(cnt[1:]))


main()
