#include <bits/stdc++.h>
using namespace std;
using ll = long long;
vector<int> par;                         // par[x] = x 的父節點，par[x] == x 代表 x 是根
vector<ll> diff;                         // diff[x] = 值(x) − 值(par[x])
int find(int x) {                        // 回傳 x 的根，並把 diff[x] 更新成「值(x) − 值(根)」
    if (par[x] == x) return x;
    int r = find(par[x]);                // r = x 所在組的根
    diff[x] += diff[par[x]];             // 先把父節點壓縮到根，再累加
    par[x] = r;
    return r;
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;                            // n = 帳戶數，m = 紀錄數
    cin >> n >> m;
    par.resize(n + 1); iota(par.begin(), par.end(), 0);
    diff.assign(n + 1, 0);
    for (int i = 1; i <= m; i++) {       // i = 第幾條紀錄
        int a, b; ll c;                  // 這條紀錄說「帳戶 b 比帳戶 a 多 c」
        cin >> a >> b >> c;              // 值(b) − 值(a) = c
        int ra = find(a), rb = find(b);  // ra、rb = a、b 各自的根
        if (ra == rb) {                  // 已在同一組：用已知的差檢查是否矛盾
            if (diff[b] - diff[a] != c) { cout << i << "\n"; return 0; }
        } else {
            // 讓 rb 接到 ra 底下：值(rb) − 值(ra) = c + diff[a] − diff[b]
            par[rb] = ra;
            diff[rb] = c + diff[a] - diff[b];
        }
    }
    cout << -1 << "\n";
}
