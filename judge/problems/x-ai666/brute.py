"""x-ai666 的暴力解：每天試遍「不動、買、賣」三種動作，列舉所有合法的交易方式。只用在小測資。"""
import sys

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
p = [int(x) for x in data[2:2 + n]]
best = 0                                          # 目前找到的最大獲利


def go(i, holding, used, money):
    """i：第幾天；holding：手上的買價（None 表示沒貨）；used：已開始的交易數；money：已實現的獲利"""
    global best
    if i == n:
        if holding is None:
            best = max(best, money)
        return
    go(i + 1, holding, used, money)               # 今天不動
    if holding is None and used < k:
        go(i + 1, p[i], used + 1, money)          # 今天買
    if holding is not None:
        go(i + 1, None, used, money + p[i] - holding)   # 今天賣


go(0, None, 0, 0)
print(best)
