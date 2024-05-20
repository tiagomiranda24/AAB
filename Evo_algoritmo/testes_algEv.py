import random
import unittest

# Supondo a estrutura das classes Individual, Population e EvolAlgorithm
class Individual:
    def __init__(self, size, genes=None):
        self.size = size
        self.genes = genes if genes is not None else self.init_random(size)

    def init_random(self, size):
        mean = 0
        std_dev = 1
        return [int(random.gauss(mean, std_dev)) for _ in range(size)]  # Utiliza random.gauss para gerar uma distribuição normal

    def mutation(self):
        mutation_index = random.randint(0, self.size - 1)
        new_gene = int(random.gauss(0, 1))
        while self.genes[mutation_index] == new_gene:
            new_gene = int(random.gauss(0, 1))
        self.genes[mutation_index] = new_gene

    def crossover(self, other):
        crossover_point = random.randint(1, self.size - 1)
        child1_genes = self.genes[:crossover_point] + other.genes[crossover_point:]
        child2_genes = other.genes[:crossover_point] + self.genes[crossover_point:]
        return Individual(self.size, child1_genes), Individual(self.size, child2_genes)

class Population:
    def __init__(self, popsize, indsize):
        self.popsize = popsize
        self.indsize = indsize
        self.indivs = self.init_random_pop()

    def init_random_pop(self):
        return [Individual(self.indsize) for _ in range(self.popsize)]

    def get_fitnesses(self):
        # Supondo que a função de aptidão seja a soma dos genes
        return [sum(ind.genes) for ind in self.indivs]

    def best_solution(self):
        fitnesses = self.get_fitnesses()
        best_index = fitnesses.index(max(fitnesses))
        return self.indivs[best_index]

class EvolAlgorithm:
    def __init__(self, popsize, indsize, mutation_rate, crossover_rate):
        self.popsize = popsize
        self.indsize = indsize
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.popul = None

    def init_popul(self):
        self.popul = Population(self.popsize, self.indsize)

    def iteration(self):
        new_pop = []
        for _ in range(self.popsize // 2):
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            if random.random() < self.crossover_rate:
                offspring1, offspring2 = parent1.crossover(parent2)
            else:
                offspring1, offspring2 = parent1, parent2
            offspring1.mutation()
            offspring2.mutation()
            new_pop.extend([offspring1, offspring2])
        self.popul.indivs = new_pop

    def tournament_selection(self):
        tournament_size = 3
        selected = random.sample(self.popul.indivs, tournament_size)
        selected_fitnesses = [sum(ind.genes) for ind in selected]
        best_index = selected_fitnesses.index(max(selected_fitnesses))
        return selected[best_index]

class TestIndividual(unittest.TestCase):
    def test_init(self):
        ind = Individual(5)
        self.assertEqual(len(ind.genes), 5)
        self.assertTrue(all(isinstance(gene, int) for gene in ind.genes))

    def test_mutation(self):
        ind = Individual(5)
        original_genes = ind.genes[:]
        ind.mutation()
        self.assertNotEqual(ind.genes, original_genes)

    def test_crossover(self):
        ind1 = Individual(5)
        ind2 = Individual(5)
        offsp1, offsp2 = ind1.crossover(ind2)
        self.assertEqual(len(offsp1.genes), 5)
        self.assertEqual(len(offsp2.genes), 5)

class TestPopulation(unittest.TestCase):
    def test_init(self):
        pop = Population(10, 5)
        self.assertEqual(len(pop.indivs), 10)
        self.assertEqual(len(pop.get_fitnesses()), 10)

    def test_best_solution(self):
        pop = Population(10, 5)
        best_ind = pop.best_solution()
        self.assertIsInstance(best_ind, Individual)

class TestEvolAlgorithm(unittest.TestCase):
    def test_init_popul(self):
        algo = EvolAlgorithm(10, 5, 2, 5)
        self.assertIsNone(algo.popul)
        algo.init_popul()
        self.assertIsNotNone(algo.popul)

    def test_iteration(self):
        algo = EvolAlgorithm(10, 5, 2, 5)
        algo.init_popul()
        algo.iteration()
        self.assertEqual(len(algo.popul.indivs), 10)

if __name__ == '__main__':
    unittest.main()
