import unittest
from ProcuraMotifsAlgoEvol import Indiv, Popul, EvolAlgorithm

class TestIndiv(unittest.TestCase):
    def test_init(self):
        ind = Indiv(5)
        self.assertEqual(len(ind.genes), 5)
        self.assertTrue(all(isinstance(gene, int) for gene in ind.genes))

    def test_mutation(self):
        ind = Indiv(5)
        original_genes = ind.genes[:]
        ind.mutation()
        self.assertNotEqual(ind.genes, original_genes)

    def test_crossover(self):
        ind1 = Indiv(5)
        ind2 = Indiv(5)
        offsp1, offsp2 = ind1.crossover(ind2)
        self.assertEqual(len(offsp1.genes), 5)
        self.assertEqual(len(offsp2.genes), 5)

class TestPopul(unittest.TestCase):
    def test_init(self):
        pop = Popul(10, 5)
        pop.initRandomPop()  # Inicializa a população com indivíduos aleatórios
        self.assertEqual(len(pop.indivs), 10)
        self.assertEqual(len(pop.getFitnesses()), 10)

    def test_best_solution(self):
        pop = Popul(10, 5)
        pop.initRandomPop()  # Inicializa a população com indivíduos aleatórios
        best_ind = pop.bestSolution()
        self.assertIsInstance(best_ind, Indiv)

class TestEvolAlgorithm(unittest.TestCase):
    def test_init_popul(self):
        algo = EvolAlgorithm(10, 5, 2, 5)
        algo.initPopul(5)
        self.assertIsNotNone(algo.popul)

    def test_iteration(self):
        algo = EvolAlgorithm(10, 5, 2, 5)
        algo.initPopul(5)
        algo.iteration()
        self.assertEqual(len(algo.popul.indivs), 10)

if __name__ == '__main__':
    unittest.main()
