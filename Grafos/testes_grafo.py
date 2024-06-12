import unittest
from grafo import GrafoDirigido

class TestGrafoDirigido(unittest.TestCase):
    """
    Testa a funcionalidade da classe GrafoDirigido.
    """

    def setUp(self):
        """
        Configura um grafo vazio antes de cada teste.
        """
        self.grafo = GrafoDirigido()

    def test_adicionar_no(self):
        """
        Testa se um nó pode ser adicionado corretamente ao grafo.
        """
        self.grafo.adicionar_no('A')
        self.assertIn('A', self.grafo.estrutura)

    def test_adicionar_arestas(self):
        """
        Testa se as arestas podem ser adicionadas corretamente entre os nós.
        """
        self.grafo.adicionar_arestas('A->B,C')
        self.assertIn('A', self.grafo.estrutura)
        self.assertIn('B', self.grafo.estrutura['A'])
        self.assertIn('C', self.grafo.estrutura['A'])

    def test_remover_no(self):
        """
        Testa se um nó pode ser removido corretamente do grafo.
        """
        self.grafo.adicionar_no('A')
        self.grafo.remover_no('A')
        self.assertNotIn('A', self.grafo.estrutura)

    def test_remover_arestas(self):
        """
        Testa se as arestas podem ser removidas corretamente.
        """
        self.grafo.adicionar_arestas('A->B,C')
        self.grafo.remover_arestas('A->B')
        self.assertNotIn('B', self.grafo.estrutura['A'])
        self.assertIn('C', self.grafo.estrutura['A'])

    def test_obter_sucessores(self):
        """
        Testa se os sucessores de um nó são retornados corretamente.
        """
        self.grafo.adicionar_arestas('A->B,C')
        sucessores = self.grafo.obter_sucessores('A')
        self.assertEqual(sucessores, ['B', 'C'])

    def test_obter_predecessores(self):
        """
        Testa se os predecessores de um nó são retornados corretamente.
        """
        self.grafo.adicionar_arestas('A->B')
        self.grafo.adicionar_arestas('C->B')
        predecessores = self.grafo.obter_predecessores('B')
        self.assertEqual(set(predecessores), {'A', 'C'})

    def test_obter_adjacentes(self):
        """
        Testa se os nós adjacentes a um nó são retornados corretamente.
        """
        self.grafo.adicionar_arestas('A->B')
        self.grafo.adicionar_arestas('B->C')
        adjacentes = self.grafo.obter_adjacentes('B')
        self.assertEqual(set(adjacentes), {'A', 'C'})

    def test_matriz_adjacencia(self):
        """
        Testa se a matriz de adjacência é gerada corretamente.
        """
        self.grafo.adicionar_arestas('A->B')
        matriz = self.grafo.matriz_adjacencia()
        self.assertEqual(matriz.loc['A', 'B'], 1)
        self.assertEqual(matriz.loc['B', 'A'], 0)

    def test_busca_em_largura(self):
        """
        Testa se a busca em largura (BFS) é realizada corretamente.
        """
        self.grafo.adicionar_arestas('A->B')
        self.grafo.adicionar_arestas('B->C')
        resultado = self.grafo.busca_em_largura('A')
        self.assertEqual(resultado, ['A', 'B', 'C'])

class TestGrafoDirigido(unittest.TestCase):
    def setUp(self):
        # Criar instância de GrafoDirigido para uso nos testes
        self.grafo = GrafoDirigido({
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2), ('D', 5)],
            'C': [('D', 1)],
            'D': []
        })

    def test_dijkstra(self):
        # Verificar se as menores distâncias de A para todos os outros nós estão corretas
        distancias = self.grafo.dijkstra('A')
        self.assertEqual(distancias, {'A': 0, 'B': 1, 'C': 3, 'D': 4})

    def test_caminho_mais_curto(self):
        # Verificar se o caminho mais curto de A para D está correto
        caminho = self.grafo.caminho_mais_curto('A', 'D')
        self.assertEqual(caminho, ['A', 'B', 'C', 'D'])

    def test_dijkstra_com_caminho(self):
        # Verificar se as menores distâncias e os pais estão corretos para A
        distancias, pais = self.grafo.dijkstra_com_caminho('A')
        self.assertEqual(distancias, {'A': 0, 'B': 1, 'C': 3, 'D': 4})
        self.assertEqual(pais, {'A': None, 'B': 'A', 'C': 'B', 'D': 'C'})

if __name__ == '__main__':
    unittest.main()
