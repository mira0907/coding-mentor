"""範例 7-B 的暴力解：從每個村莊出發走遍整棵樹，把到所有村莊的距離加起來。"""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]           # adj[u] = (v, w) 的清單
    for i in range(n - 1):
        u, v, w = int(data[1 + 3 * i]), int(data[2 + 3 * i]), int(data[3 + 3 * i])
        adj[u].append((v, w))
        adj[v].append((u, w))
    ans = []                                   # ans[i] = 村莊 i + 1 的距離總和
    for s in range(1, n + 1):                  # 以每個村莊為起點
        dist = {s: 0}
        st = [s]
        while st:
            u = st.pop()
            for v, w in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + w
                    st.append(v)
        ans.append(sum(dist.values()))
    print(" ".join(map(str, ans)))


main()
