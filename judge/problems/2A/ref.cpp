#include <bits/stdc++.h>
using namespace std;
int main() {
    int N, sx, sy, tx, ty;             // N = 棋盤邊長，(sx, sy) = 起點，(tx, ty) = 終點
    cin >> N >> sx >> sy >> tx >> ty;
    // (dx[d], dy[d]) = 騎士第 d 種走法的位移，共 8 種
    int dx[] = {1, 2, 2, 1, -1, -2, -2, -1};
    int dy[] = {2, 1, -1, -2, -2, -1, 1, 2};
    // dist[x][y] = 走到 (x, y) 的最少步數，-1 表示還沒走到
    vector<vector<int>> dist(N + 1, vector<int>(N + 1, -1));
    queue<pair<int,int>> q;            // 等待處理的格子 (x, y)
    dist[sx][sy] = 0; q.push({sx, sy});
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();         // (x, y) = 目前處理的格子
        for (int d = 0; d < 8; d++) {             // d = 第幾種走法
            int nx = x + dx[d], ny = y + dy[d];   // (nx, ny) = 走一步後的格子
            if (nx < 1 || nx > N || ny < 1 || ny > N || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
    cout << dist[tx][ty] << "\n";
}
