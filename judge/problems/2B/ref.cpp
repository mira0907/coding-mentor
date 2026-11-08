#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int R, C, K;                       // R、C = 迷宮的列數和行數，K = 最多能打破幾面牆
    cin >> R >> C >> K;
    vector<string> g(R);               // g[x][y] = 第 x 列第 y 行的格子，'.' 是通道、'#' 是牆
    for (auto& s : g) cin >> s;        // s = g 的每一列，用參考才能直接讀進 g
    // 狀態 (x, y, 已打破幾面牆)，攤平成一維陣列
    // id(x, y, k) = 狀態 (x, y, k) 在一維陣列裡的位置
    auto id = [&](int x, int y, int k) { return (x * C + y) * (K + 1) + k; };
    vector<int> dist(R * C * (K + 1), -1);   // dist[位置] = 走到這個狀態的最少步數，-1 表示還沒走到
    queue<array<int,3>> q;             // 等待處理的狀態 {x, y, k}
    dist[id(0, 0, 0)] = 0; q.push({0, 0, 0});
    int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};   // 上下左右四個方向的位移
    while (!q.empty()) {
        auto [x, y, k] = q.front(); q.pop();   // 目前在 (x, y)，已經打破 k 面牆
        if (x == R - 1 && y == C - 1) { cout << dist[id(x, y, k)] << "\n"; return 0; }
        for (int d = 0; d < 4; d++) {          // d = 第幾個方向
            int nx = x + dx[d], ny = y + dy[d];    // (nx, ny) = 下一格
            if (nx < 0 || nx >= R || ny < 0 || ny >= C) continue;
            int nk = k + (g[nx][ny] == '#');       // 走進牆就要打破一次
            if (nk > K || dist[id(nx, ny, nk)] != -1) continue;
            dist[id(nx, ny, nk)] = dist[id(x, y, k)] + 1;
            q.push({nx, ny, nk});
        }
    }
    cout << -1 << "\n";
}
