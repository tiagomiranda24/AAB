import graphviz
import io
from contextlib import redirect_stdout

class Digraph:
    """
    Implementação de um grafo direcionado (digrafo) em Python.
    """

    def __init__(self, g=None):
        """
        Inicializa um novo grafo direcionado.

        Args:
            g (dict, opcional): Um dicionário representando o grafo. As chaves são os nós e os valores são os vizinhos.
                Exemplo: {'A': {'B', 'C'}, 'B': {'C'}, 'C': {'A'}}
        """
        self.graph = g if g is not None else {}  # O dicionário que armazena o grafo
        self.GV = graphviz.Digraph()  # Objeto Graphviz para visualização do grafo

    def add_node(self, v):
        """
        Adiciona um novo nó ao grafo.

        Args:
            v: O nó a ser adicionado.
        """
        if v not in self.graph:
            self.graph[v] = {}  # O nó é representado como uma chave no dicionário
            self.GV.node(str(v))  # Adiciona o nó à visualização do grafo

    def add_edge(self, u, v):
        """
        Adiciona uma aresta direcionada ao grafo, conectando dois nós.

        Args:
            u: O nó de origem.
            v: O nó de destino.
        """
        self.add_node(u)  # Garante que os nós estejam presentes no grafo
        self.add_node(v)
        self.graph[u][v] = True  # Adiciona a aresta ao dicionário
        self.GV.edge(str(u), str(v))  # Adiciona a aresta à visualização do grafo

    def __repr__(self):
        """
        Representação do grafo para exibição.

        Retorna:
            str: Uma representação visual do grafo.
        """
        display(self.GV)  # Exibe o grafo utilizando Graphviz
        return ""

    def __str__(self):
        """
        Retorna uma representação textual do grafo.

        Retorna:
            str: Uma representação textual do grafo.
        """
        with io.StringIO() as F, redirect_stdout(F):
            for u in self.graph:
                print(u, [v for v in self.graph[u]], sep=" => ")
            return F.getvalue()

    def _get_neighbors(self, u, direction="successors"):
        """
        Obtém os vizinhos de um nó no grafo.

        Args:
            u: O nó de interesse.
            direction (str, opcional): A direção das arestas. Pode ser "successors" (sucessores) ou "predecessors" (predecessores).

        Retorna:
            set: Um conjunto dos vizinhos do nó.
        """
        return {v for v in self.graph[u]} if direction == "successors" else {u for u in self.graph if u in self.graph[v]}

    def indegree(self, u):
        """
        Calcula o grau de entrada de um nó.

        Args:
            u: O nó de interesse.

        Retorna:
            int: O grau de entrada do nó.
        """
        return len(self._get_neighbors(u, direction="predecessors"))

    def outdegree(self, u):
        """
        Calcula o grau de saída de um nó.

        Args:
            u: O nó de interesse.

        Retorna:
            int: O grau de saída do nó.
        """
        return len(self._get_neighbors(u))

    def degree(self, u):
        """
        Calcula o grau de um nó (entrada + saída).

        Args:
            u: O nó de interesse.

        Retorna:
            int: O grau do nó.
        """
        return self.indegree(u) + self.outdegree(u)

    def _traverse(self, u, visited=None, mode="dfs"):
        """
        Realiza uma travessia do grafo.

        Args:
            u: O nó de partida.
            visited (list, opcional): Lista dos nós visitados durante a travessia.
            mode (str, opcional): O modo de travessia. Pode ser "dfs" (busca em profundidade) ou "bfs" (busca em largura).

        Retorna:
            list: Lista dos nós visitados durante a travessia.
        """
        visited = [u] if visited is None else visited

        # Realiza a travessia de acordo com o modo especificado
        for v in self._get_neighbors(u) if mode == "dfs" else self._get_neighbors(u, direction="predecessors"):
            if v not in visited:
                visited.append(v)
                self._traverse(v, visited, mode)
        return visited

    def dfs(self, u):
        """
        Realiza uma busca em profundidade (DFS) a partir de um nó.

        Args:
            u: O nó de partida.

        Retorna:
            list: Lista dos nós visitados durante a busca em profundidade.
        """
        return self._traverse(u)

    def bfs(self, u):
        """
        Realiza uma busca em largura (BFS) a partir de um nó.

        Args:
            u: O nó de partida.

        Retorna:
            dict: Um dicionário que mapeia cada nó alcançável a partir do nó inicial ao seu caminho correspondente.
        """
        visited = {}
        assert u in self.graph, f"graph doesn't have a {u} vertex"
        queue = [(u, [])]

        while queue:
            U, P = queue[0]
            queue = queue[1:]
            if U not in visited:
                visited[U] = P
                for V in self._get_neighbors(U):
                    queue.append((V, P + [U]))
        return visited

    def _shortest_path(self, u, v):
        """
        Calcula o caminho mais curto entre dois nós usando BFS.

        Args:
            u: O nó de partida.
            v: O nó de destino.

        Retorna:
            list: O caminho mais curto entre os dois nós.
        """
        visited = self.bfs(u)
        return visited[v]

    def distance(self, u, v):
        """
        Calcula a distância entre dois nós, ou seja, o comprimento do caminho mais curto.

        Args:
            u: O nó de partida.
            v: O nó de destino.

        Retorna:
            int: A distância entre os dois nós.
        """
        return len(self._shortest_path(u, v))

    def shortest_path(self, u, v):
        """
        Calcula o caminho mais curto entre dois nós.

        Args:
            u: O nó de partida.
            v: O nó de destino.

        Retorna:
            list: O caminho mais curto entre os dois nós.
        """
        return self._shortest_path(u, v)

    def reachable_with_dist(self, u):
        """
        Calcula os nós alcançáveis a partir de um nó e suas distâncias correspondentes.

        Args:
            u: O nó de partida.

        Retorna:
            dict: Um dicionário que mapeia cada nó alcançável a partir do nó inicial à sua distância correspondente.
        """
        visited = self.bfs(u)
        return {u: len(visited[u]) for u in visited}

    def reachable_with_path(self, u):
        """
        Calcula os nós alcançáveis a partir de um nó e seus caminhos correspondentes.

        Args:
            u: O nó de partida.

        Retorna:
            dict: Um dicionário que mapeia cada nó alcançável a partir do nó inicial ao seu caminho correspondente.
        """
        return self.bfs(u)
