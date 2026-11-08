#include <bits/stdc++.h>
using namespace std;
using ll = long long;

#ifdef LOCAL
#define dbg(x) cerr << #x << " = " << (x) << '\n'
#else
#define dbg(x)
#endif
int n,m;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin>>n>>m;
    vector<pair<int,int>> rel; 
    vector<int> out(n,0);
    int sel=0;
    int again=0;
    for(int i=0;i<m;i++){
        int a,b;
        cin>>a>>b;
        if (a==b){
            sel++;
            continue;
        }
        a--;
        b--;
        if (a>b) swap(a,b);
        rel.push_back({a,b});
    }
    sort(rel.begin(),rel.end());
    for(int i=0;i<(int)rel.size();i++){
        if (i>0 && rel[i]==rel[i-1]){
            again++;
        }
        else{
            out[rel[i].first]++;
            out[rel[i].second]++;
        }
    }
    cout << sel << " " << again << "\n";
    for(int i=0;i<n;i++){
        cout << out[i] << " ";
    }
    return 0;
}
