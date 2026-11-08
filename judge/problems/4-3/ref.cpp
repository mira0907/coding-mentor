#include <bits/stdc++.h>
using namespace std;
struct DSU {
    // p[x]：x 的父節點，p[x] == x 代表 x 是這一組的根
    // sz[x]：以 x 為根的這一組有幾個元素，只有根的值有意義
    vector<int> p, sz;
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }   // n = 元素個數；一開始每個元素自成一組
    // 回傳 x 所在組的根，並路徑壓縮
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    // 合併 a、b 所在的組；已經同組時回傳 false
    bool unite(int a, int b) {
        a = find(a); b = find(b);             // 之後 a、b 代表兩組各自的根
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);        // 小的接到大的下面
        p[b] = a; sz[a] += sz[b];
        return true;
    }
    // 把 x 還原成自成一組（只對這一輪用過的點呼叫）
    void reset(int x) { p[x] = x; sz[x] = 1; }
};

vector<int> jp;                               // jp[x] = x 往上跳的目標；x 到父節點的樹邊被標記後才會指向父節點
// 回傳從 x 出發、沿著已標記的樹邊一路往上能到的最高點（非遞迴，並把路上的點直接指向它）
int jfind(int x) {
    int r = x;                                // r = 最後找到的最高點
    while (jp[r] != r) r = jp[r];
    while (jp[x] != r) {                      // 第二趟：路徑壓縮
        int nx = jp[x];                       // nx = x 原本要跳去的點
        jp[x] = r;
        x = nx;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    // n = 機房數
    // m = 光纖數
    int n, m;
    cin >> n >> m;
    // eu[i] = 第 i 條光纖的一端
    // ev[i] = 第 i 條光纖的另一端
    // ew[i] = 第 i 條光纖的成本
    vector<int> eu(m), ev(m), ew(m);
    for (int i = 0; i < m; i++) cin >> eu[i] >> ev[i] >> ew[i];   // i = 光纖編號（從 0 開始）
    vector<int> ord(m);                       // ord = 依成本由小到大排好的光纖編號
    iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int a, int b) { return ew[a] < ew[b]; });

    DSU all(n);                               // 成本比目前這組小的光纖，把機房連成的連通塊
    DSU tmp(n);                               // 只在一組內使用：這組光纖在「縮點後的圖」上選出的森林
    jp.resize(n + 1); iota(jp.begin(), jp.end(), 0);
    vector<vector<pair<int,int>>> fadj(n + 1);   // fadj[a] = 森林上 a 的鄰居 (b, 光纖編號)
    // par[x] = 森林上 x 的父節點
    // pe[x] = x 連到父節點的那條光纖編號
    // dep[x] = x 在森林上的深度，根是 0
    vector<int> par(n + 1), pe(n + 1), dep(n + 1);
    vector<char> seen(n + 1, 0);              // seen[x] = 這一組的 BFS 是否已經走到 x
    // ra[i] = 第 i 條光纖一端所在的連通塊（縮點後的點）
    // rb[i] = 第 i 條光纖另一端所在的連通塊
    vector<int> ra(m), rb(m);
    vector<int> type(m, 0);                   // type[i] = 第 i 條光纖的答案：0 = NONE，1 = SOME，2 = ALL

    for (int i = 0; i < m; ) {                // i = 這一組在 ord 裡的開頭
        int j = i;                            // j = 這一組的結尾（不含）
        while (j < m && ew[ord[j]] == ew[ord[i]]) j++;
        vector<int> nodes;                    // nodes = 這一組用到的縮點後的點，結束時要還原
        vector<int> extra;                    // extra = 這一組裡不在森林上、但兩端不同塊的光纖
        // 第一步：縮點，並用 tmp 選出一個生成森林
        for (int k = i; k < j; k++) {         // k = 這一組的第幾條
            int id = ord[k];                  // id = 光纖編號
            ra[id] = all.find(eu[id]);
            rb[id] = all.find(ev[id]);
            if (ra[id] == rb[id]) continue;   // 兩端早已連通：NONE
            nodes.push_back(ra[id]); nodes.push_back(rb[id]);
            if (tmp.unite(ra[id], rb[id])) {  // 森林邊，先假設是 ALL
                type[id] = 2;
                fadj[ra[id]].push_back({rb[id], id});
                fadj[rb[id]].push_back({ra[id], id});
            } else {                          // 會和森林形成環：一定是 SOME
                type[id] = 1;
                extra.push_back(id);
            }
        }
        // 第二步：BFS 求森林上每個點的父節點與深度
        for (int r : nodes) {                 // r = 還沒走過的點就當作一棵樹的根
            if (seen[r]) continue;
            seen[r] = 1; par[r] = r; pe[r] = -1; dep[r] = 0;
            queue<int> q;                     // BFS 佇列
            q.push(r);
            while (!q.empty()) {
                int x = q.front(); q.pop();   // x = 正在展開的點
                for (auto [y, id] : fadj[x]) {   // 森林邊 x–y，光纖編號 id
                    if (seen[y]) continue;
                    seen[y] = 1; par[y] = x; pe[y] = id; dep[y] = dep[x] + 1;
                    q.push(y);
                }
            }
        }
        // 第三步：每條非森林邊 (a, b) 和森林上 a 到 b 的路徑形成環，把路徑上的森林邊改成 SOME
        for (int id : extra) {                // id = 非森林邊的光纖編號
            int x = jfind(ra[id]);            // x = 從一端往上跳過已標記邊後的位置
            int y = jfind(rb[id]);            // y = 從另一端往上跳過已標記邊後的位置
            while (x != y) {
                if (dep[x] < dep[y]) swap(x, y);   // 每次讓比較深的那一邊往上走一步
                type[pe[x]] = 1;              // x 到父節點的森林邊在環上
                jp[x] = par[x];               // 標記後，之後可以直接跳過這條邊
                x = jfind(x);
            }
        }
        // 第四步：整組加入 all，並還原這一組動過的陣列
        for (int k = i; k < j; k++) all.unite(eu[ord[k]], ev[ord[k]]);   // k = 這一組的第幾條
        for (int x : nodes) {                 // x = 這一組用過的點
            tmp.reset(x); jp[x] = x; fadj[x].clear(); seen[x] = 0;
        }
        i = j;
    }
    const char* name[3] = {"NONE", "SOME", "ALL"};   // name[x] = type 為 x 時要輸出的字
    for (int i = 0; i < m; i++) cout << name[type[i]] << "\n";   // i = 光纖編號（從 0 開始）
}
