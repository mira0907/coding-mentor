#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                                   // n = 路口數，m = 道路數
    cin >> n >> m;
    vector<vector<pair<int,int>>> g(n + 1);     // g[u] = (鄰居, 道路編號)
    for (int i = 1; i <= m; i++) {              // i = 道路編號
        int u, v; cin >> u >> v;                // 第 i 條道路連接 u、v
        g[u].push_back({v, i}); g[v].push_back({u, i});
    }
    // dfn[u]：u 被拜訪的順序，0 表示還沒拜訪
    // low[u]：u 的子樹最多經過一條非樹邊能回到的最小 dfn
    // pe[u]：走到 u 時用的那條道路編號，根為 0
    // it[u]：u 已經處理到第幾個鄰居
    vector<int> dfn(n + 1, 0), low(n + 1, 0), pe(n + 1, 0), it(n + 1, 0);
    vector<bool> isCut(n + 1, false);           // isCut[u] = u 是不是關鍵路口
    int timer_ = 0;                             // 時間戳計數器
    for (int s = 1; s <= n; s++) {              // s = 每個連通塊的起點，也就是 DFS 樹的根
        if (dfn[s]) continue;
        int rootChild = 0;                      // 根 s 在 DFS 樹上有幾個子節點
        vector<int> st = {s};                   // st = 目前的遞迴路徑，最上面是正在處理的點
        dfn[s] = low[s] = ++timer_;
        while (!st.empty()) {
            int u = st.back();                  // u = 正在處理的點
            if (it[u] < (int)g[u].size()) {
                auto [v, id] = g[u][it[u]++];   // v = 下一個鄰居，id = 那條道路的編號
                if (id == pe[u]) continue;      // 只跳過來時那條道路
                if (dfn[v]) low[u] = min(low[u], dfn[v]);   // 回邊：用 dfn 更新
                else {                          // 相當於遞迴呼叫 dfs(v)
                    pe[v] = id; dfn[v] = low[v] = ++timer_;
                    st.push_back(v);
                }
            } else {                            // u 的鄰居都處理完，相當於 return
                st.pop_back();
                if (st.empty()) continue;       // u 是根，沒有父節點可以回報
                int p = st.back();              // p = u 的父節點
                low[p] = min(low[p], low[u]);
                if (p == s) rootChild++;        // 根另外判斷，先數子節點
                else if (low[u] >= dfn[p]) isCut[p] = true;   // u 的子樹回不到 p 的上方
            }
        }
        if (rootChild >= 2) isCut[s] = true;   // 根有兩個以上子節點才是割點
    }
    vector<int> ans;                            // ans = 所有關鍵路口，由小到大
    for (int u = 1; u <= n; u++)                // u = 路口編號
        if (isCut[u]) ans.push_back(u);
    cout << ans.size() << "\n";
    for (size_t i = 0; i < ans.size(); i++)     // i = 第幾個關鍵路口
        cout << ans[i] << " \n"[i + 1 == ans.size()];
}
