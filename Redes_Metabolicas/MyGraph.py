"""
autor: Miguel Rocha
"""

class MyGraph:

    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g

    ## get basic information about the graph

    def get_nodes(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
    
    def size(self):
        ''' Returns number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
    
    def print_graph(self):
        for v in self.graph.keys():
            print(v, " -> ", self.graph[v])

    def add_vertex(self, v):
        ''' Add a vertex to the graph
        Tests if vertex exists not adding if it does. '''
        if v not in self.graph.keys():
            self.graph[v] = []

    def add_edge(self, o, d):
        ''' Add edge to the graph.
        If vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)

    def get_successors(self, v):
        return list (self.graph[v]) # avoids list being overwritten
    
    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res
    
    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res

    def out_degree(self, v):
        return len(self.graph[v])

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v))

    def all_degrees( self , deg_type = "inout"):
        ''' Computes the degree for all nodes.
        deg_type can be "in", "out", or "inout"
        Returns a dictionary: node -> degree.'''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len (self.graph[v])
            else : degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs

    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len (l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.append(elem)
        return res
    
    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s=0
            for elem in self .graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res
    
    def distance(self, s, d):
        if s == d: return 0
        l = [(s,0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return dist + 1
                elif elem not in visited:
                    l.append((elem,dist+1))
                    visited.append(elem)
        return None

    def shortest_path(self, s, d):
        if s == d: return 0
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return preds+[node,elem]
                elif elem not in visited:
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None

    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not MyGraph.is_in_tuple_list(l,elem) and not MyGraph.is_in_tuple_list(res,elem):
                    l.append((elem,dist+1))
        return res

    def is_in_tuple_list(tl, val):
        res = False
        for (x,y) in tl:
            if val == x: return True
        return res
    
    def is_connected(self):
        total = len (self.graph.keys()) - 1
        for v in self.graph.keys():
            reachable_v = self.reachable_bfs(v)
            if (len(reachable_v) < total): return False
        return True
    
    def node_has_cycle(self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res