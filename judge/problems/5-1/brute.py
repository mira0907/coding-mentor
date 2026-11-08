# 暴力解：關卡 v 永遠無法通過 <=> 存在某個在環上的關卡 u（u 走一步以上能回到自己），
# 且 u == v 或 u 走得到 v。用每個點各做一次 DFS 求可達性。
import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
    # reach[u] = 從 u 走「至少一步」能到的點集合
    reach = []
    reach.append(set())
    for u in range(1, n + 1):
        seen = set()
        stack = list(adj[u])
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(adj[x])
        reach.append(seen)
    on_cycle = [u in reach[u] if u > 0 else False for u in range(n + 1)]
    stuck = []
    for v in range(1, n + 1):
        bad = False
        for u in range(1, n + 1):
            if on_cycle[u] and (u == v or v in reach[u]):
                bad = True
        if bad:
            stuck.append(v)
    print(len(stuck))
    if stuck:
        print(" ".join(map(str, stuck)))

main()
