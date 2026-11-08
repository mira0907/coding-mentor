#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct Dinic {
    struct E { int to; ll cap; };              // 一條邊：指向 to，剩餘容量 cap
    // e：所有的邊，第 i 條和第 i ^ 1 條互為反向邊
    // g[u]：從 u 出發的邊在 e 裡的編號
    // lvl[u]：BFS 分層後 u 的層數（離 s 幾步），-1 表示走不到
    // it[u]：當前弧，u 下一條要嘗試的邊是 g[u] 的第幾條
    vector<E> e; vector<vector<int>> g; vector<int> lvl, it;
    Dinic(int n) : g(n + 1), lvl(n + 1), it(n + 1) {}   // n = 最大的點編號
    void addEdge(int u, int v, ll c) {          // 加入 u → v 容量 c，和容量 0 的反向邊
        g[u].push_back(e.size()); e.push_back({v, c});
        g[v].push_back(e.size()); e.push_back({u, 0});
    }
    bool bfs(int s, int t) {                    // 從 s 分層；回傳 t 是否還走得到
        fill(lvl.begin(), lvl.end(), -1);
        queue<int> q; lvl[s] = 0; q.push(s);    // q = BFS 佇列
        while (!q.empty()) {
            int u = q.front(); q.pop();         // u = 目前處理的點
            for (int id : g[u])                 // id = u 出發的一條邊的編號
                if (e[id].cap > 0 && lvl[e[id].to] < 0) {
                    lvl[e[id].to] = lvl[u] + 1; q.push(e[id].to);
                }
        }
        return lvl[t] >= 0;
    }
    // 從 u 往 t 送流，f = 這條路到目前為止最多還能送多少；回傳實際送出的量
    ll dfs(int u, int t, ll f) {
        if (u == t) return f;
        for (int& i = it[u]; i < (int)g[u].size(); i++) {   // i 綁在 it[u] 上：當前弧優化
            int id = g[u][i];                   // id = 嘗試的邊
            int v = e[id].to;                   // v = 這條邊的終點
            if (e[id].cap > 0 && lvl[v] == lvl[u] + 1) {    // 只走往下一層、還有容量的邊
                ll d = dfs(v, t, min(f, e[id].cap));        // d = 經由 v 實際送到 t 的量
                if (d > 0) { e[id].cap -= d; e[id ^ 1].cap += d; return d; }
            }
        }
        return 0;
    }
    ll maxflow(int s, int t) {                  // 回傳 s 到 t 的最大流；s = 源點，t = 匯點
        ll flow = 0;                            // flow = 目前的總流量
        ll f;                                   // f = 這次增廣送出的量
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while ((f = dfs(s, t, LLONG_MAX)) > 0) flow += f;
        }
        return flow;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // R = 棋盤列數
    // C = 棋盤行數
    int R, C;
    cin >> R >> C;
    vector<string> b(R);                        // b[r][c] = '.' 可以放、'#' 是壞掉的格子
    for (auto& row : b) cin >> row;             // row = b 的每一列，用參考才能直接讀進 b
    // 點編號：S = 0，格子 (r, c) 是 r * C + c + 1，T = R * C + 1
    int S = 0;                                  // S = 源點，連到每個黑格
    int T = R * C + 1;                          // T = 匯點，每個白格連到它
    Dinic din(T);
    // 騎士的 8 種走法：(dr[k], dc[k]) = 列、行的位移
    int dr[8] = {1, 1, -1, -1, 2, 2, -2, -2};
    int dc[8] = {2, -2, 2, -2, 1, -1, 1, -1};
    int freeCells = 0;                          // freeCells = 可以放騎士的格子數
    for (int r = 0; r < R; r++)                 // (r, c) = 目前的格子
        for (int c = 0; c < C; c++) {
            if (b[r][c] != '.') continue;
            freeCells++;
            int id = r * C + c + 1;             // id = 格子 (r, c) 的點編號
            if ((r + c) % 2 == 1) { din.addEdge(id, T, 1); continue; }   // 白格：連到匯點
            din.addEdge(S, id, 1);              // 黑格：從源點連進來
            for (int k = 0; k < 8; k++) {       // k = 第幾種走法
                int nr = r + dr[k];             // nr = 走到的列
                int nc = c + dc[k];             // nc = 走到的行
                if (nr < 0 || nr >= R || nc < 0 || nc >= C || b[nr][nc] != '.') continue;
                din.addEdge(id, nr * C + nc + 1, 1);   // 騎士一步一定走到白格：黑 → 白
            }
        }
    cout << freeCells - din.maxflow(S, T) << "\n";   // 最大獨立集 = 點數 − 最大匹配
}
