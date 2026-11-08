"""範例 4-B 的暴力解：對每個 i，只用前 i 條紀錄重新建圖，用 BFS 替每個連通塊指定餘額，
看有沒有某條紀錄對不上；第一個對不上的 i 就是答案。只用在 m ≤ 8 的小測資。"""
import sys
from collections import deque


def consistent(n, recs):
    """recs 這些紀錄能不能同時成立"""
    adj = [[] for _ in range(n + 1)]             # adj[x] = (y, d)：值(y) − 值(x) = d
    for a, b, c in recs:
        adj[a].append((b, c))
        adj[b].append((a, -c))
    pot = [None] * (n + 1)                       # pot[x] = 指定給帳戶 x 的餘額
    for s in range(1, n + 1):
        if pot[s] is None:
            pot[s] = 0
            q = deque([s])
            while q:
                x = q.popleft()
                for y, d in adj[x]:
                    if pot[y] is None:
                        pot[y] = pot[x] + d
                        q.append(y)
    return all(pot[b] - pot[a] == c for a, b, c in recs)


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    recs = [(int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])) for i in range(m)]
    for i in range(1, m + 1):
        if not consistent(n, recs[:i]):
            print(i)
            return
    print(-1)


main()
