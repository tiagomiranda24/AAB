import random


class Individual:
    def __init__(self, size, genes=None, lb=0, ub=1):
        self.lb = lb  # Limite inferior para os valores dos genes
        self.ub = ub  # Limite superior para os valores dos genes
        self.fitness = None  # Valor de aptidão do indivíduo
        self.genes = genes if genes is not None else self.init_random(size)  # Inicializa os genes utilizando uma distribuição normal se não forem fornecidos

    def init_random(self, size):
        # Inicialização dos genes utilizando uma distribuição normal
        mean = (self.lb + self.ub) / 2  # Calcula a média dos limites
        std_dev = (self.ub - self.lb) / 6  # Calcula o desvio padrão baseado na largura do intervalo
        return [int(np.random.normal(mean, std_dev)) for _ in range(size)]  # Gera genes aleatórios utilizando uma distribuição normal

    def mutation(self):
        # Mutação agressiva: muta até 20% dos genes
        num_mutations = max(1, int(0.2 * len(self.genes)))  # Calcula o número máximo de mutações
        positions = random.sample(range(len(self.genes)), num_mutations)  # Seleciona aleatoriamente as posições a serem mutadas
        for pos in positions:
            self.genes[pos] = 1 if self.genes[pos] == 0 else 0  # Inverte o valor do gene na posição escolhida

    def crossover(self, indiv2):
        return self.two_point_crossover(indiv2)

    def two_point_crossover(self, indiv2):
        # Crossover de dois pontos
        pos1 = random.randint(1, len(self.genes) - 2)  # Escolhe o primeiro ponto de corte
        pos2 = random.randint(pos1 + 1, len(self.genes) - 1)  # Escolhe o segundo ponto de corte
        offsp1 = self.genes[:pos1] + indiv2.genes[pos1:pos2] + self.genes[pos2:]  # Gera o primeiro descendente combinando partes dos genes dos pais
        offsp2 = indiv2.genes[:pos1] + self.genes[pos1:pos2] + indiv2.genes[pos2:]  # Gera o segundo descendente combinando partes dos genes dos pais
        return Individual(len(self.genes), offsp1, self.lb, self.ub), Individual(len(self.genes), offsp2, self.lb, self.ub)  # Retorna os descendentes como objetos Individual

    def get_fitness(self):
        return self.fitness  # Retorna a aptidão do indivíduo

    def set_fitness(self, fitness):
        self.fitness = fitness  # Define a aptidão do indivíduo

    def get_genes(self):
        return self.genes  # Retorna os genes do indivíduo
import random

class Population:
    def __init__(self, popsize, indsize, indivs=None):
        self.popsize = popsize  # Tamanho da população
        self.indsize = indsize  # Tamanho de cada indivíduo
        self.indivs = indivs if indivs is not None else []  # Lista de indivíduos, inicializada com uma lista vazia se não fornecida
        if not self.indivs:
            self.init_random_pop()  # Inicializa uma população aleatória se não houver indivíduos fornecidos

    def get_indiv(self, index):
        return self.indivs[index]  # Retorna o indivíduo na posição especificada

    def init_random_pop(self):
        self.indivs = [Individual(self.indsize) for _ in range(self.popsize)]  # Inicializa uma população aleatória de tamanho popsize

    def get_fitnesses(self, indivs=None):
        if indivs is None:
            indivs = self.indivs
        return [ind.get_fitness() for ind in indivs]  # Retorna uma lista de aptidões dos indivíduos fornecidos ou de toda a população

    def best_solution(self):
        return max(self.indivs, key=lambda ind: ind.get_fitness())  # Retorna o indivíduo com a maior aptidão na população

    def selection(self, n, indivs=None):
        if indivs is None:
            indivs = self.indivs
        fitnesses = self.get_fitnesses(indivs)
        selected = random.choices(range(len(indivs)), weights=fitnesses, k=n)  # Seleciona n indivíduos ponderados pelas aptidões
        return selected

    def recombination(self, parents, noffspring):
        offspring = []
        for _ in range(noffspring // 2):
            parent1 = self.indivs[random.choice(parents)]
            parent2 = self.indivs[random.choice(parents)]
            offsp1, offsp2 = parent1.crossover(parent2)  # Realiza o crossover entre dois pais selecionados aleatoriamente
            offsp1.mutation()  # Aplica mutação ao primeiro descendente
            offsp2.mutation()  # Aplica mutação ao segundo descendente
            offspring.extend([offsp1, offsp2])  # Adiciona os descendentes à lista de descendentes
        return offspring

    def reinsertion(self, offspring):
        fitnesses = self.get_fitnesses(self.indivs)
        sorted_inds = [ind for _, ind in sorted(zip(fitnesses, self.indivs), reverse=True)]  # Ordena os indivíduos por aptidão decrescente
        for i in range(len(offspring)):
            self.indivs[i] = offspring[i]  # Substitui os primeiros indivíduos da população pelos descendentes
        for i in range(len(offspring), len(self.indivs)):
            self.indivs[i] = sorted_inds[i - len(offspring)]  # Preenche os restantes com os indivíduos originais ordenados por aptidão
class EvolAlgorithm:
    def __init__(self, popsize, numits, noffspring, indsize):
        self.popsize = popsize  # Tamanho da população
        self.numits = numits  # Número de iterações
        self.noffspring = noffspring  # Número de descendentes gerados em cada iteração
        self.indsize = indsize  # Tamanho de cada indivíduo
        self.popul = None  # População inicialmente não definida
        self.bestsol = None  # Melhor solução inicialmente não definida

    def init_popul(self):
        self.popul = Population(self.popsize, self.indsize)  # Inicializa a população

    def evaluate(self, indivs):
        for ind in indivs:
            fitness = sum(ind.get_genes())  # Calcula a aptidão de cada indivíduo, que é a soma de seus genes
            ind.set_fitness(fitness)  # Define a aptidão do indivíduo

    def iteration(self):
        parents = self.popul.selection(self.noffspring)  # Seleciona os pais para a geração de descendentes
        offspring = self.popul.recombination(parents, self.noffspring)  # Realiza a recombinação para gerar descendentes
        self.evaluate(offspring)  # Avalia os descendentes
        self.popul.reinsertion(offspring)  # Reinserção dos descendentes na população

    def run(self):
        self.init_popul()  # Inicializa a população
        self.evaluate(self.popul.indivs)  # Avalia a população inicial
        self.bestsol = self.popul.best_solution()  # Define a melhor solução como a melhor solução atual da população
        for i in range(1, self.numits + 1):  # Executa as iterações do algoritmo
            self.iteration()  # Executa uma iteração do algoritmo genético
            current_best = self.popul.best_solution()  # Obtém a melhor solução após a iteração
            if current_best.get_fitness() > self.bestsol.get_fitness():  # Atualiza a melhor solução se uma solução melhor for encontrada
                self.bestsol = current_best
            # Exibe informações sobre a iteração atual
            print(f"Iteration: {i}, Best fitness: {self.bestsol.get_fitness()}, Best solution: {self.bestsol.get_genes()}")

