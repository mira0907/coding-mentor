"""範例 7-A 的暴力解：從每個村莊出發走遍整棵樹，取所有距離的最大值。"""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]           # adj[u] = (v, w) 的清單
    for i in range(n - 1):
        u, v, w = int(data[1 + 3 * i]), int(data[2 + 3 * i]), int(data[3 + 3 * i])
        adj[u].append((v, w))
        adj[v].append((u, w))
    best = 0                                   # 目前看過的最遠距離
    for s in range(1, n + 1):                  # 以每個村莊為起點
        dist = {s: 0}
        st = [s]
        while st:
            u = st.pop()
            for v, w in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + w
                    st.append(v)
        best = max(best, max(dist.values()))
    print(best)


main()
