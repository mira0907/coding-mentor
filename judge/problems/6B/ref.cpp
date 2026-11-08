#include <bits/stdc++.h>
using namespace std;
// N = 圖的點數（每個開關 2 個點，共 2n）；timer_ = 時間戳；sccCnt = SCC 個數
int N, timer_ = 0, sccCnt = 0;
vector<vector<int>> adj;               // adj[x] = 「x 成立」可以推出哪些點也成立
// dfn、low：Tarjan 用的時間戳；comp[x]：x 屬於第幾個 SCC；stk：還沒分進 SCC 的點
vector<int> dfn, low, comp, stk;
vector<bool> inStk;                    // inStk[x] = x 是否在 stk 裡
void tarjan(int u) {                   // u = 目前拜訪的點
    dfn[u] = low[u] = ++timer_;
    stk.push_back(u); inStk[u] = true;
    for (int v : adj[u]) {             // v = 從 u 推得出來的點
        if (!dfn[v]) { tarjan(v); low[u] = min(low[u], low[v]); }
        else if (inStk[v]) low[u] = min(low[u], dfn[v]);
    }
    if (low[u] == dfn[u]) {            // u 是一個 SCC 的根
        ++sccCnt;
        while (true) {
            int x = stk.back(); stk.pop_back();   // x = 屬於這個 SCC 的點
            inStk[x] = false; comp[x] = sccCnt;
            if (x == u) break;
        }
    }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                          // n = 開關數，m = 條件數
    cin >> n >> m;
    N = 2 * n;
    // 點 2i + 1 代表「開關 i 為 1」，點 2i 代表「開關 i 為 0」（i 從 0 起算）
    // id(i, val) = 「開關 i 為 val」這個點的編號
    auto id = [](int i, int val) { return 2 * i + val; };
    adj.assign(N, {});
    for (int k = 0; k < m; k++) {      // k = 第幾個條件
        int i, a, j, b;                // 條件：開關 i 為 a，或開關 j 為 b
        cin >> i >> a >> j >> b; i--; j--;
        // (i == a) 或 (j == b)：若 i != a 則 j == b；若 j != b 則 i == a
        adj[id(i, 1 - a)].push_back(id(j, b));
        adj[id(j, 1 - b)].push_back(id(i, a));
    }
    dfn.assign(N, 0); low.assign(N, 0); comp.assign(N, 0); inStk.assign(N, false);
    for (int v = 0; v < N; v++) if (!dfn[v]) tarjan(v);   // v = 每個還沒拜訪的點
    string ans(n, '0');                // ans[i] = 開關 i 的設定
    for (int i = 0; i < n; i++) {      // i = 第幾個開關
        if (comp[id(i, 0)] == comp[id(i, 1)]) { cout << "IMPOSSIBLE\n"; return 0; }   // 0 和 1 互相推得出 → 無解
        ans[i] = comp[id(i, 1)] < comp[id(i, 0)] ? '1' : '0';   // 拓撲序較後者為真
    }
    cout << ans << "\n";
}
