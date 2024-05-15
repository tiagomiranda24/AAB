# testes unitários para os algoritmos evolucionários
import unittest
import random

class Individual:
    def __init__(self, genome_length: int, fitness=None, upper_limit: int = 1, lower_limit: int = 0, genome=None):
        if genome is None:
            genome = []

        self.genome_length = genome_length
        self.genome = genome
        self.fitness = fitness
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if not self.genome:
            self.initialize_random_genome()

    def initialize_random_genome(self):
        self.genome = [random.uniform(self.lower_limit, self.upper_limit) for _ in range(self.genome_length)]

    def calculate_fitness(self):
        self.fitness = sum(self.genome)

    def mutate(self, mutation_rate: float):
        for i in range(self.genome_length):
            if random.random() < mutation_rate:
                self.genome[i] += random.uniform(-0.1, 0.1)


class Population:
    def __init__(self, population_size: int, individual_genome_length: int, individuals=None):
        self.population_size = population_size
        self.individual_genome_length = individual_genome_length

        if individuals:
            self.individuals = individuals
        else:
            self.initialize_random_population()

    def initialize_random_population(self):
        self.individuals = [Individual(self.individual_genome_length) for _ in range(self.population_size)]

    def evaluate_population(self):
        for individual in self.individuals:
            individual.calculate_fitness()

    def evolve_population(self, mutation_rate: float):
        for individual in self.individuals:
            individual.mutate(mutation_rate)


class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        self.population_size = 10
        self.genome_length = 5
        self.population = Population(self.population_size, self.genome_length)

    def test_individual_initialization(self):
        individual = Individual(self.genome_length)
        self.assertEqual(len(individual.genome), self.genome_length)

    def test_population_initialization(self):
        self.assertEqual(len(self.population.individuals), self.population_size)
        self.assertEqual(len(self.population.individuals[0].genome), self.genome_length)

    def test_fitness_calculation(self):
        individual = Individual(self.genome_length)
        individual.calculate_fitness()
        self.assertIsNotNone(individual.fitness)

    def test_mutation(self):
        individual = Individual(self.genome_length)
        original_genome = individual.genome[:]
        individual.mutate(0.5)
        self.assertNotEqual(individual.genome, original_genome)

if __name__ == '__main__':
    unittest.main()
