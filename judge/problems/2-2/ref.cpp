#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // R = 地圖的列數
    // C = 地圖的行數
    int R, C;
    cin >> R >> C;
    vector<string> g(R);                 // g[x][y] = 第 x 列第 y 行的格子
    for (auto& s : g) cin >> s;          // s = g 的每一列，用參考才能直接讀進 g
    const int INF = INT_MAX;             // 代表火永遠燒不到
    vector<int> fire(R * C, INF);        // fire[x * C + y] = 格子 (x, y) 開始著火的分鐘，INF 表示燒不到
    vector<int> dist(R * C, -1);         // dist[x * C + y] = 你最早幾分鐘到達 (x, y)，-1 表示還沒到過
    queue<int> q;                        // BFS 佇列，存格子編號 x * C + y
    // dx[d] = 第 d 個方向的列位移
    // dy[d] = 第 d 個方向的行位移
    int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};
    // 第一次 BFS：所有火源一起以時間 0 放進佇列（多源 BFS）
    for (int x = 0; x < R; x++)          // (x, y) = 掃描到的格子
        for (int y = 0; y < C; y++)
            if (g[x][y] == 'F') { fire[x * C + y] = 0; q.push(x * C + y); }
    while (!q.empty()) {
        int cur = q.front(); q.pop();    // cur = 目前展開的著火格子
        // x = cur 所在的列
        // y = cur 所在的行
        int x = cur / C, y = cur % C;
        for (int d = 0; d < 4; d++) {    // d = 第幾個方向
            // nx = 相鄰格子的列
            // ny = 相鄰格子的行
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= R || ny < 0 || ny >= C || g[nx][ny] == '#') continue;
            if (fire[nx * C + ny] != INF) continue;
            fire[nx * C + ny] = fire[cur] + 1;
            q.push(nx * C + ny);
        }
    }
    // 第二次 BFS：從你的位置出發，只走「到達時還沒著火」的格子
    for (int x = 0; x < R; x++)          // (x, y) = 掃描到的格子
        for (int y = 0; y < C; y++)
            if (g[x][y] == 'S') { dist[x * C + y] = 0; q.push(x * C + y); }
    while (!q.empty()) {
        int cur = q.front(); q.pop();    // cur = 目前展開的格子
        // x = cur 所在的列
        // y = cur 所在的行
        int x = cur / C, y = cur % C;
        if (x == 0 || x == R - 1 || y == 0 || y == C - 1) {   // 站在最外圈，再走一步就出去了
            cout << dist[cur] + 1 << "\n";
            return 0;
        }
        for (int d = 0; d < 4; d++) {    // d = 第幾個方向
            // nx = 相鄰格子的列（cur 不在最外圈，所以一定在地圖內）
            // ny = 相鄰格子的行
            int nx = x + dx[d], ny = y + dy[d];
            int nid = nx * C + ny;       // nid = 相鄰格子的編號
            if (g[nx][ny] == '#' || dist[nid] != -1) continue;
            if (dist[cur] + 1 >= fire[nid]) continue;     // 到達時已經著火（或同時著火），不能進去
            dist[nid] = dist[cur] + 1;
            q.push(nid);
        }
    }
    cout << -1 << "\n";
}
