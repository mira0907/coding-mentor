#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct Dinic {
    struct Ed { int to; ll cap; };             // 一條邊：指向 to，剩餘容量 cap
    // e：所有的邊（第 i 條和第 i ^ 1 條互為反向邊）；g[u]：u 出發的邊編號
    // lvl[u]：分層後的層數；it[u]：當前弧，下一條要試的邊
    vector<Ed> e; vector<vector<int>> g; vector<int> lvl, it;
    Dinic(int n) : g(n + 1), lvl(n + 1), it(n + 1) {}   // n = 最大的點編號
    void addEdge(int u, int v, ll c) {         // 加入 u → v 容量 c，和容量 0 的反向邊
        g[u].push_back(e.size()); e.push_back({v, c});
        g[v].push_back(e.size()); e.push_back({u, 0});
    }
    bool bfs(int s, int t) {                   // 分層，回傳 t 是否走得到
        fill(lvl.begin(), lvl.end(), -1);
        queue<int> q; lvl[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int id : g[u])
                if (e[id].cap > 0 && lvl[e[id].to] < 0) { lvl[e[id].to] = lvl[u] + 1; q.push(e[id].to); }
        }
        return lvl[t] >= 0;
    }
    ll dfs(int u, int t, ll f) {               // 從 u 往 t 送流，最多送 f，回傳實際送出的量
        if (u == t) return f;
        for (int& i = it[u]; i < (int)g[u].size(); i++) {   // i 綁在 it[u] 上：當前弧優化
            int id = g[u][i], v = e[id].to;    // id = 嘗試的邊，v = 終點
            if (e[id].cap > 0 && lvl[v] == lvl[u] + 1) {
                ll d = dfs(v, t, min(f, e[id].cap));   // d = 經由 v 送到 t 的量
                if (d > 0) { e[id].cap -= d; e[id ^ 1].cap += d; return d; }
            }
        }
        return 0;
    }
    ll maxflow(int s, int t) {                 // 回傳 s 到 t 的最大流
        ll flow = 0, f;                        // flow = 總流量，f = 這次送出的量
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while ((f = dfs(s, t, LLONG_MAX)) > 0) flow += f;
        }
        return flow;
    }
};
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                                  // n = 專案數，m = 工具數
    cin >> n >> m;
    // 點編號：S = 0，專案 1..n，工具 n+1..n+m，T = n+m+1
    int S = 0, T = n + m + 1;                  // S = 源點，T = 匯點
    Dinic din(T);
    const ll INF = LLONG_MAX / 4;              // 代表「不能切」的無限容量
    ll totalProfit = 0;                        // 所有專案的獲利總和
    for (int i = 1; i <= n; i++) {             // i = 專案編號
        ll p; cin >> p; totalProfit += p;      // p = 專案 i 的獲利
        din.addEdge(S, i, p);                  // 切掉這條邊 = 放棄專案 i
    }
    for (int j = 1; j <= m; j++) {             // j = 工具編號
        ll c; cin >> c;                        // c = 工具 j 的價格
        din.addEdge(n + j, T, c);              // 切掉這條邊 = 買下工具 j
    }
    for (int i = 1; i <= n; i++) {
        int k; cin >> k;                       // k = 專案 i 需要幾種工具
        while (k--) { int j; cin >> j; din.addEdge(i, n + j, INF); }   // 做專案 i 就一定要買工具 j
    }
    cout << totalProfit - din.maxflow(S, T) << "\n";   // 最大淨利 = 總獲利 − 最小割
}
