from __future__ import print_function

from collections import defaultdict
from copy import copy


class Graph(object):
    INIT_DEGREE_DIC = [('in', 0), ('out', 0)]

    def __init__(self, **kwargs):
        if 'graph_obj' in kwargs:
            self.__graph_dic__ = copy(kwargs['graph_obj'].__graph_dic__)
            self.degree_dic = copy(kwargs['graph_obj'].degree_dic)
        else:
            self.__graph_dic__ = defaultdict(dict)
            self.degree_dic = defaultdict(lambda: defaultdict(int))
            self.__compute_degree__()

    def to_csv(self, name="graph.csv"):
        with open(name, 'w') as f:
            for src in self.__graph_dic__:
                for dst in self.__graph_dic__[src]:
                    f.write('{},{}\n'.format(src, dst))

    def vertices(self):
        return self.__graph_dic__.keys()

    # partially match
    def find_vertex(self, word):
        v = []
        for vertex in self.vertices():
            if vertex.find(word) != -1:
                v.append(vertex)
        return v

    def add_edge(self, edge, value=None):
        (vertex, neighbour) = tuple(edge)
        if neighbour not in self.__graph_dic__[vertex]:
            self.__graph_dic__[vertex][neighbour] = value if value else 1
            if neighbour not in self.__graph_dic__:
                self.__graph_dic__[neighbour] = {}
            self.degree_dic[neighbour]['in'] += 1
            self.degree_dic[vertex]['out'] += 1

    def get_neighbour(self, vertex=None):
        if vertex is not None:
            return self.__graph_dic__[vertex]
        else:
            return self.__graph_dic__

    def __compute_degree__(self):
        for vertex in self.__graph_dic__:
            self.degree_dic[vertex] = {'in': 0, 'out': 0}
        for vertex in self.__graph_dic__:
            if not self.__graph_dic__[vertex]:
                continue
            for neighbour in self.__graph_dic__[vertex]:
                self.degree_dic[vertex]['out'] += 1
                self.degree_dic[neighbour]['in'] += 1

    def get_degree(self, vertex):
        return self.degree_dic[vertex]

    def get_parent(self, vertex):
        parent = set()
        for v in self.__graph_dic__:
            if vertex in self.__graph_dic__[v]:
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

    # distance function. return value if edge exist, else return inf
    def distance(self, a, b):
        if b in self.__graph_dic__[a]:
            return self.__graph_dic__[a][b]
        else:
            return float('inf')

    # Dijkstra algorithm
    def path_between(self, src, dst):
        if src is dst:
            return [src]

        # selected points list
        S = {src}
        # path point dictionary
        P = {}
        # distance dictionary
        D = {}
        for v in self.vertices():
            D[v] = self.distance(src, v)
            if v in self.__graph_dic__[src]:
                P[v] = src
        P[src] = None

        while dst not in P and P.keys() != S:
            unselected_p = [p for p in P if p not in S]
            select_p = unselected_p[0]
            # select the closest unselected point
            for p in unselected_p:
                if D[p] < D[select_p]:
                    select_p = p
            S.add(select_p)

            for neighbour in self.get_neighbour(select_p):
                if D[select_p] + self.distance(select_p, neighbour) < D[neighbour]:
                    D[neighbour] = D[select_p] + self.distance(select_p, neighbour)
                    P[neighbour] = select_p

        if P.keys() == S:
            return None
        path = [dst]
        p = dst
        while P[p] is not None:
            path.append(P[p])
            p = P[p]
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
    g = Graph()
    g.add_edge(['a', 'b'])
    g.add_edge(['a','b'])
    g.add_edge(['b', 'c'])
    g.add_edge(['a', 'c'])
    g.add_edge(['d', 'a'])
    print(g.get_neighbour())
    print(g.vertices())
    for vertex in g.get_neighbour():
        print(vertex + ':')
        print(g.get_degree(vertex))

    print("c's parent:")
    print(g.get_parent('c'))
    print("path d to c:")
    print(g.path_between('d', 'c'))
    g.to_csv()
