import sys
def main():
    data = sys.stdin.read().split()
    n, m, t = int(data[0]), int(data[1]), int(data[2])
    INF = float('inf')
    d = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][i] = 0
    p = 3
    for _ in range(m):
        u, v, w = int(data[p]), int(data[p + 1]), int(data[p + 2]); p += 3
        if w < d[u][v]:
            d[u][v] = w
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    out = []
    for i in range(1, n + 1):
        a = d[i][t] + d[t][i]
        out.append(str(-1 if a == INF else a))
    print(" ".join(out))
main()
