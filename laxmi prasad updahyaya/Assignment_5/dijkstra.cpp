//Problem statement on leetcode
//https://leetcode.com/problems/network-delay-time/description/

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {


        //creating adjacency list
        vector<vector <pair <int,int>>> adj;
        for(int i = 0;i<n;i++){
            int u = times[i][0];
            int v = times[i][2];
            int w = times[i][3];

            adj[u].push_back(make_pair(v,w));
            adj[v].push_back(make_pair(u,w));

        }

        //code to find the minimum distance array to each node

        vector<int> dist;


        for(int i=0;i<n;i++){
            dist[i] = 11000;
        }

        
        queue<pair<int,int>>q;
        q.push(make_pair(k,0));
        dist[0] = 0;
        q.push(std::make_pair(0,0));
        int node=0;
        int distance=0;
        int new_node =0;
        int new_distance = 0;

        


        while(q.empty()){
            //fetch the element in first in queue
            int node = q.front().first;
            int distance = q.front().second;

            //poping the fetched node
            q.pop();

            //adding the neighbout node int queue
            for (const auto& p : adj[node]){
                new_node = p.first;
                new_distance = p.second;
                new_distance += distance;
               q.push(make_pair(new_node,new_distance));
            }

            if(dist[node]>distance){
                dist[node] = distance;
            }

        }



        //writing actual logic which find minimum network delay time using distance array
        int max=0;
        for (int i = 0;i < dist.size();i++){
            if(dist[i] >max){
                max = dist[i];
            }
        }

        if(max >=11000){
            return -1;
        }else{
            return max;
        }


    }
};
