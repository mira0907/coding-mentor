"""實作 4-3 的暴力解：列舉所有 n − 1 條光纖的組合，留下是生成樹的，
找出總成本最小的那些，再數每條光纖出現在幾棵最小生成樹裡。只用在 m ≤ 13 的小測資。"""
import sys
from itertools import combinations


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    E = [(int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])) for i in range(m)]

    def is_tree(ids):
        """ids 這 n − 1 條光纖有沒有形成環（沒有環就是生成樹）"""
        par = list(range(n + 1))

        def f(x):
            while par[x] != x:
                x = par[x]
            return x

        for i in ids:
            a, b = f(E[i][0]), f(E[i][1])
            if a == b:
                return False
            par[a] = b
        return True

    trees = []                                   # 所有生成樹的 (總成本, 光纖編號集合)
    for ids in combinations(range(m), n - 1):
        if is_tree(ids):
            trees.append((sum(E[i][2] for i in ids), set(ids)))
    best = min(w for w, _ in trees)
    msts = [s for w, s in trees if w == best]    # 所有最小生成樹
    res = []
    for i in range(m):
        c = sum(1 for s in msts if i in s)       # 第 i 條光纖在幾棵最小生成樹裡
        res.append("ALL" if c == len(msts) else ("SOME" if c > 0 else "NONE"))
    print("\n".join(res))


main()
