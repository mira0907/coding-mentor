"""實作 7-1 的暴力解：真的把每一座變電所拿掉，數剩下各塊的大小。"""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]           # adj[u] = 和 u 相連的變電所
    for i in range(n - 1):
        u, v = int(data[1 + 2 * i]), int(data[2 + 2 * i])
        adj[u].append(v)
        adj[v].append(u)
    part = [0] * (n + 1)                       # part[x] = 拆掉 x 後最大那一塊的大小
    for x in range(1, n + 1):
        seen = [False] * (n + 1)
        seen[x] = True                         # 拆掉的點當作已走過
        for s in range(1, n + 1):              # 從每個還沒走過的點數一塊
            if seen[s]:
                continue
            seen[s] = True
            st, cnt = [s], 0
            while st:
                u = st.pop()
                cnt += 1
                for v in adj[u]:
                    if not seen[v]:
                        seen[v] = True
                        st.append(v)
            part[x] = max(part[x], cnt)
    best = min(part[1:])
    print(best)
    print(" ".join(str(x) for x in range(1, n + 1) if part[x] == best))


main()
