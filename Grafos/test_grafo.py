# test_grafo.py
import unittest
from typing import Dict, List
from grafo import GrafoDirigido


import unittest
from grafo import GrafoDirigido

class TestGrafoDirigido(unittest.TestCase):
    def setUp(self):
        self.grafo = GrafoDirigido()

    def test_adicionar_no(self):
        self.grafo.adicionar_no('A')
        self.assertIn('A', self.grafo.estrutura)
        self.grafo.adicionar_no(1)
        self.assertIn('1', self.grafo.estrutura)

    def test_adicionar_arestas(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        self.assertIn('B', self.grafo.estrutura['A'])
        self.grafo.adicionar_arestas(['A->C', 'B->D'])
        self.assertIn('C', self.grafo.estrutura['A'])
        self.assertIn('D', self.grafo.estrutura['B'])

    def test_remover_no(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        self.grafo.remover_no('A')
        self.assertNotIn('A', self.grafo.estrutura)
        self.assertNotIn('A', self.grafo.estrutura['B'])

    def test_remover_arestas(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        self.grafo.remover_arestas('A->B')
        self.assertNotIn('B', self.grafo.estrutura['A'])

    def test_obter_sucessores(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        self.assertEqual(self.grafo.obter_sucessores('A'), ['B'])

    def test_obter_predecessores(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        self.assertEqual(self.grafo.obter_predecessores('B'), ['A'])

    def test_obter_adjacentes(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        self.assertEqual(self.grafo.obter_adjacentes('A'), ['B'])
        self.assertEqual(self.grafo.obter_adjacentes('B'), ['A'])

    def test_matriz_adjacencia(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_arestas('A->B')
        matriz = self.grafo.matriz_adjacencia()
        self.assertEqual(matriz.loc['A', 'B'], 1)
        self.assertEqual(matriz.loc['B', 'A'], 0)

    def test_busca_em_largura(self):
        self.grafo.adicionar_no('A')
        self.grafo.adicionar_no('B')
        self.grafo.adicionar_no('C')
        self.grafo.adicionar_arestas('A->B')
        self.grafo.adicionar_arestas('B->C')
        self.assertEqual(self.grafo.busca_em_largura('A'), ['A', 'B', 'C'])

if __name__ == '__main__':
    unittest.main()
