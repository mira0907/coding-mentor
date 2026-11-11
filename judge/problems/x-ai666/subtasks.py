"""讀入一筆測資，印出它符合哪些子題的限制（子題編號從 1 開始）。"""
import sys

data = sys.stdin.buffer.read().split(maxsplit=2)
n, k = int(data[0]), int(data[1])               # n：時間點數；k：交易次數上限
ok = []
if n <= 1000 and k == 1:
    ok.append(1)
if n <= 50000 and k <= 100:
    ok.append(2)
if n <= 200000 and k <= n:
    ok.append(3)
if n <= 2000000 and k <= n:
    ok.append(4)
print(*ok)
