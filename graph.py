class Graph(object):
    INIT_DEGREE_DIC = [('in', 0), ('out', 0)]

    def __init__(self, graph_obj=None, graph_dic=None):
        if graph_dic is None:
            graph_dic = {}
        if graph_obj is not None:
            self.__graph_dic = graph_obj.__graph_dic
            self.degree_dic = graph_obj.degree_dic
        else:
            self.__graph_dic = dict(graph_dic)
            self.degree_dic = {}
            self.__complete_vertices()
            self.__compute_degree()

    def __complete_vertices(self):
        add_list = set()

        for vertex in self.__graph_dic:
            for neighbour in self.__graph_dic[vertex]:
                # for dictionary's length can not be change during iteration,we use list to store the unexist vertex
                if neighbour not in self.__graph_dic:
                    add_list.add(neighbour)
        for not_exist_vertex in add_list:
            self.add_vertices(not_exist_vertex)

    def vertices(self):
        return self.__graph_dic.keys()

    def add_vertices(self, v):
        if v not in self.__graph_dic:
            self.__graph_dic[v] = []
            self.degree_dic[v] = dict(Graph.INIT_DEGREE_DIC)

    # partially match
    def find_vertex(self, word):
        v = []
        for vertex in self.vertices():
            if vertex.find(word) != -1:
                v.append(vertex)
        return v

    def add_edge(self, edge):
        (vertex, neighbour) = tuple(edge)
        if vertex in self.__graph_dic:
            if neighbour not in self.__graph_dic[vertex]:
                self.__graph_dic[vertex].append(neighbour)
                if neighbour not in self.__graph_dic:
                    self.add_vertices(neighbour)
                self.degree_dic[neighbour]['in'] += 1
                self.degree_dic[vertex]['out'] += 1
        else:
            self.add_vertices(vertex)
            self.__graph_dic[vertex].append(neighbour)
            self.degree_dic[vertex]['out'] += 1
            if neighbour not in self.__graph_dic:
                self.add_vertices(neighbour)
            self.degree_dic[neighbour]['in'] += 1

    def get_neighbour(self, vertex=None):
        if vertex is not None:
            return self.__graph_dic[vertex]
        else:
            return self.__graph_dic

    def __compute_degree(self):
        for vertex in self.__graph_dic:
            self.degree_dic[vertex] = {'in': 0, 'out': 0}
        for vertex in self.__graph_dic:
            if not self.__graph_dic[vertex]:
                continue
            for neighbour in self.__graph_dic[vertex]:
                self.degree_dic[vertex]['out'] += 1
                self.degree_dic[neighbour]['in'] += 1

    def get_degree(self, vertex):
        return self.degree_dic[vertex]

    def get_parent(self, vertex):
        parent = set()
        for v in self.__graph_dic:
            if vertex in self.__graph_dic[v]:
                parent.add(v)
        return parent

    def merge(self, graph):
        if isinstance(graph, Graph):
            graph_dic = graph.get_neighbour()
            for v in graph_dic:
                for neighbour in graph_dic[v]:
                    self.add_edge((v, neighbour))
        else:
            raise TypeError

    # distance function.Must be fix when we are using a graph with som distance between vertices
    @staticmethod
    def distance(a, b):
        return 1

    # dijstra algorithm
    def path_between(self, src, dst):
        if src is dst:
            return [src]

        # selected points list
        S = []
        # path point dictionary
        P = {}
        # distance dictionary
        D = {}
        # define -1 as inf here
        for v in self.vertices():
            if v in self.get_neighbour(src):
                D[v] = self.distance(src, v)
                P[v] = src
            else:
                D[v] = -1
        P[src] = None
        S.append(src)

        while dst not in P and P.keys() != S:
            unselected_p = [p for p in P if p not in S]
            select_p = unselected_p[0]
            # select the closest unselected point
            for p in unselected_p:
                if D[p] < D[select_p]:
                    select_p = p
            S.append(select_p)

            for neighbour in self.get_neighbour(select_p):
                if D[select_p] + self.distance(select_p,neighbour) < D[neighbour] or D[neighbour] is -1:
                    D[neighbour] = D[select_p] + self.distance(select_p, neighbour)
                    P[neighbour] = select_p

        if P.keys() is S:
            return None
        path = [dst]
        p = dst
        while P[p] is not src:
            path.append(P[p])
            p = P[p]
        path.append(src)
        return path

    # My shortest distance algorithm for no-rule-directed-graph
    def my_shortest(self, src, dst):
        if src == dst:
            return [src]
        visit = {}
        tmp_graph_dic = {}

        for v in self.vertices():
            visit[v] = False
        visit[src] = True

        V = [src]
        while True:
            next_V = []
            for v in V:
                tmp_V = self.get_neighbour(v)
                for next_v in tmp_V:
                    # This algorithm reach dst
                    if next_v == dst:
                        path = [dst, v]
                        next_v = v
                        while next_v != src:
                            next_v = tmp_graph_dic[next_v]
                            path.append(next_v)
                        return path

                    if visit[next_v] is False:
                        visit[next_v] = True
                        tmp_graph_dic[next_v] = v
                next_V += tmp_V
            V = next_V

    def all_path_between(self, src, dst, path=None):
        success_path = []
        if path is None:
            path = src
        if src is dst:
            return [path]

        for neighbour in self.get_neighbour(src):
            success_path += self.all_path_between(neighbour, dst, path+'->'+neighbour)

        return success_path


if __name__ == '__main__':
    g = Graph({'a':['b']})
    g.add_vertices('a')
    g.add_edge(['a', 'b'])
    g.add_edge(['a','b'])
    g.add_edge(['b', 'c'])
    g.add_edge(['a', 'c'])
    g.add_edge(['d', 'a'])
    print g.get_neighbour()
    print g.vertices()
    for vertex in g.get_neighbour():
        print vertex + ':',
        print g.get_degree(vertex)

    print "c's parent:",
    print g.get_parent('c')
    print "path d to c:",
    print g.path_between('d', 'c')
