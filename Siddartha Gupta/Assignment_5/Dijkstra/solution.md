Problem statement on leetcode
 <a href="https://leetcode.com/problems/network-delay-time/description/">Network-delay-time</a> 

Solution: Uisng dijkstra algorithm representing graph in Adjacency List.

```C++
class Solution {
private:
    int Nearnode(vector<int>& dis, vector<bool>& vis) {
        int n = dis.size(), idx;
        int Min = INT_MAX;
        for (int i = 0; i < n; i++) {
            if (!vis[i] && dis[i] < Min) {
                Min = dis[i];
                idx = i;
            }
        }
        if (Min == INT_MAX)
            return -1;
        return idx;
    }
    void dijkstra(vector<vector<pair<int, int>>>& adj, vector<int>& weight,
                  vector<bool>& vis, vector<int>& dis) {
        int idx = Nearnode(dis, vis);
        if (idx == -1)
            return;
        vis[idx] = true;

        for (int i = 0; i < adj[idx].size(); i++) {
            if (dis[idx] + adj[idx][i].second < dis[adj[idx][i].first]) {
                dis[adj[idx][i].first] = dis[idx] + adj[idx][i].second;
            }
        }

        dijkstra(adj, weight, vis, dis);
    }

public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int, int>>> al(n + 1);
        for (int s = 0; s < times.size(); s++) {
            al[times[s][0]].push_back(make_pair(times[s][1], times[s][2]));
        }
        vector<bool> vis(n + 1, false);
        vector<int> weight(n + 1,
                           INT_MAX); // Initialize weight vector with INT_MAX
        vector<int> dis(n + 1, INT_MAX);
        dis[k] = 0;
        dijkstra(al, weight, vis, dis);
        int ans = *max_element(dis.begin() + 1, dis.end());
        if (ans == INT_MAX)
            return -1;
        return ans;
    }
};
```

![]()