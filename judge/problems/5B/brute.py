"""範例 5-B 的暴力解：從每個點各做一次 DFS，數到得了的點（含自己）。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]            # adj[a] = a 指向的點
    for i in range(m):
        adj[int(data[2 + 2 * i])].append(int(data[3 + 2 * i]))
    out = []
    for s in range(1, n + 1):                   # s = 出發點
        seen = {s}
        st = [s]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        out.append(len(seen))
    print(" ".join(map(str, out)))


main()
