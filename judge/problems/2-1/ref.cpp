#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int R, C;                        // R、C = 地圖的列數和行數
    cin >> R >> C;
    vector<string> g(R);             // g[i][j] = 第 i 列第 j 行，'#' 是陸地、'.' 是海
    for (auto& s : g) cin >> s;      // s = g 的每一列，用參考才能直接讀進 g
    vector<vector<bool>> vis(R, vector<bool>(C, false));   // vis[i][j] = 這格陸地是否已經算進某座島
    int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};      // 上下左右四個方向的位移
    int islands = 0, best = 0;       // islands = 島的數量，best = 最大的島有幾格
    for (int i = 0; i < R; i++)          // (i, j) = 掃描到的格子
        for (int j = 0; j < C; j++) {
            if (g[i][j] != '#' || vis[i][j]) continue;   // 不是陸地，或已經屬於某座島
            islands++;                   // 找到一座新的島
            int area = 0;                // 這座島目前算到的格數
            queue<pair<int,int>> q;      // BFS 佇列，存還沒展開的格子
            q.push({i, j}); vis[i][j] = true;
            while (!q.empty()) {
                auto [x, y] = q.front(); q.pop();   // (x, y) = 目前展開的格子
                area++;
                for (int d = 0; d < 4; d++) {       // d = 第幾個方向
                    int nx = x + dx[d], ny = y + dy[d];   // (nx, ny) = 相鄰的格子
                    if (nx < 0 || nx >= R || ny < 0 || ny >= C) continue;
                    if (g[nx][ny] != '#' || vis[nx][ny]) continue;
                    vis[nx][ny] = true;
                    q.push({nx, ny});
                }
            }
            best = max(best, area);
        }
    cout << islands << " " << best << "\n";
}
