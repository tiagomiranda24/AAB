import random

class Individual:
    """
    Classe que representa um indivíduo em um algoritmo evolucionário.
    """
    def __init__(self, genome_length: int, fitness=None, upper_limit: int = 1, lower_limit: int = 0, genome=None):
        """
        Inicializa um novo objeto Individual.

        Parâmetros:
            genome_length (int): O tamanho do genoma do indivíduo.
            fitness (float): A aptidão do indivíduo.
            upper_limit (int): O limite superior do genoma do indivíduo.
            lower_limit (int): O limite inferior do genoma do indivíduo.
            genome (list): O genoma do indivíduo. Se não fornecido, inicializa com valores aleatórios.
        """
        if genome is None:
            genome = []

        self.genome_length = genome_length
        self.genome = genome
        self.fitness = fitness
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        # Inicializa o genoma com valores aleatórios, se não fornecido
        if not self.genome:
            self.initialize_random_genome()

    def initialize_random_genome(self):
        """
        Inicializa o genoma do indivíduo com valores aleatórios.
        """
        self.genome = [random.uniform(self.lower_limit, self.upper_limit) for _ in range(self.genome_length)]

    def calculate_fitness(self):
        """
        Calcula a aptidão do indivíduo.
        Aqui, poderia ser qualquer função de aptidão adequada para o problema em questão.
        """
        self.fitness = sum(self.genome)  # Exemplo simples: soma dos valores do genoma

    def mutate(self, mutation_rate: float):
        """
        Aplica uma mutação no genoma do indivíduo.

        Parâmetros:
            mutation_rate (float): A taxa de mutação, probabilidade de mutação para cada gene do genoma.
        """
        for i in range(self.genome_length):
            if random.random() < mutation_rate:
                # Mutação simples: adicionar um valor aleatório pequeno ao gene
                self.genome[i] += random.uniform(-0.1, 0.1)


class Population:
    """
    Classe que representa uma população em um algoritmo evolucionário.
    """
    def __init__(self, population_size: int, individual_genome_length: int, individuals=None):
        """
        Inicializa um novo objeto Population.

        Parâmetros:
            population_size (int): O número de indivíduos na população.
            individual_genome_length (int): O tamanho do genoma de cada indivíduo.
            individuals (list): A lista de indivíduos. Se não fornecido, inicializa com valores aleatórios.
        """

        self.population_size = population_size
        self.individual_genome_length = individual_genome_length

        # Inicializa a população com indivíduos aleatórios, se não fornecido
        if individuals:
            self.individuals = individuals
        else:
            self.initialize_random_population()

    def initialize_random_population(self):
        """
        Inicializa a população com indivíduos aleatórios.
        """
        self.individuals = [Individual(self.individual_genome_length) for _ in range(self.population_size)]

    def evaluate_population(self):
        """
        Avalia a aptidão de todos os indivíduos na população.
        """
        for individual in self.individuals:
            individual.calculate_fitness()

    def evolve_population(self, mutation_rate: float):
        """
        Evolui a população aplicando mutação nos indivíduos.

        Parâmetros:
            mutation_rate (float): A taxa de mutação para cada gene do genoma.
        """
        for individual in self.individuals:
            individual.mutate(mutation_rate)
