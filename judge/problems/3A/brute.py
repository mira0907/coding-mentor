"""範例 3-A 的暴力解：列舉所有簡單環找可達負環，再列舉所有簡單路徑求最短距離。只用在 n ≤ 6 的小測資。"""
import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    out = [[] for _ in range(n + 1)]             # out[u] = u 的出邊 (v, w)
    for i in range(m):
        u, v, w = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
        out[u].append((v, w))

    # 從點 1 走得到哪些點
    reach = [False] * (n + 1)
    reach[1] = True
    stack = [1]
    while stack:
        u = stack.pop()
        for v, _ in out[u]:
            if not reach[v]:
                reach[v] = True
                stack.append(v)

    # 列舉每個從 s 出發又回到 s 的簡單環，s 走得到且總和為負就是可達負環
    neg = [False]

    def cyc(s, u, total, vis):
        for v, w in out[u]:
            if v == s and total + w < 0:
                neg[0] = True
            elif v != s and not vis[v]:
                vis[v] = True
                cyc(s, v, total + w, vis)
                vis[v] = False

    for s in range(1, n + 1):
        if reach[s]:
            vis = [False] * (n + 1)
            vis[s] = True
            cyc(s, s, 0, vis)
    if neg[0]:
        print("NEGATIVE CYCLE")
        return

    # 沒有可達負環時，最短路一定是簡單路徑：列舉全部取最小
    best = [None] * (n + 1)

    def path(u, total, vis):
        if best[u] is None or total < best[u]:
            best[u] = total
        for v, w in out[u]:
            if not vis[v]:
                vis[v] = True
                path(v, total + w, vis)
                vis[v] = False

    vis = [False] * (n + 1)
    vis[1] = True
    path(1, 0, vis)
    print(" ".join("INF" if b is None else str(b) for b in best[1:]))


main()
