"""
author: ruimendes
"""

import random

class Indiv:
    def __init__(self, size, genes=[], lb=0, ub=1):  # Método construtor da classe Indiv
        self.lb = lb # Define o limite inferior para os genes
        self.ub = ub # Define o limite superior para os genes
        self.genes = genes if genes is not None else []# Lista de genes do indivíduo
        self.fitness = None # Aptidão do indivíduo, inicialmente indefinida
        if not self.genes:# Se não houver genes fornecidos
            self.initRandom(size) # Inicializa os genes aleatoriamente com base no tamanho fornecido

    def initRandom(self, size):  # Método para inicializar os genes de forma aleatória
       self.genes = [random.choice([0, 1]) for _ in range(size)]# Gera uma lista de genes com valores 0 ou 1

    def mutation(self): # Método para realizar a mutação de um gene aleatório
        pos = random.randint(0, len(self.genes) - 1) # Escolhe uma posição aleatória para mutação
        self.genes[pos] = 1 - self.genes[pos]# Inverte o valor do gene (0 -> 1 ou 1 -> 0)

    def crossover(self, indiv2): # Método para realizar o crossover com outro indivíduo
       return self.one_pt_crossover(indiv2) # Realiza o crossover de um ponto
    
    def one_pt_crossover(self, indiv2):# Método de crossover de um ponto
       offsp1 = self.genes[:] # Cria uma cópia dos genes do primeiro indivíduo
       offsp2 = indiv2.genes[:]# Cria uma cópia dos genes do segundo indivíduo
       pos = random.randint(0, len(self.genes) - 1)  # Escolhe um ponto de crossover aleatório
       offsp1[pos:], offsp2[pos:] = offsp2[pos:], offsp1[pos:]# Troca os genes após o ponto de crossover
       return Indiv(len(self.genes), offsp1, self.lb, self.ub), Indiv(len(self.genes), offsp2, self.lb, self.ub) # Retorna dois novos indivíduos resultantes do crossover


class Popul:  
 
    def __init__(self, popsize, indsize,indivs=[]): # Método construtor da classe Popul
        self.popsize = popsize  # Define o tamanho da população
        self.indsize = indsize # Define o tamanho dos indivíduos
        self.indivs = indivs if indivs is not None else []   # Lista de indivíduos na população

        if not self.indivs: #Se não houver indivíduos fornecidos
            self.randomPopul() # Inicializa a população aleatoriamente

    def getIndiv(self, index):  # Método para obter um indivíduo pelo índice
        return self.indivs[index] # Retorna o indivíduo na posição especificada
    
    def initRandomPop(self):  # Método para inicializar a população com indivíduos aleatórios
        self.indivs = [Indiv(self.indsize) for _ in range(self.popsize)]# Cria indivíduos aleatórios

    def getFitnesses(self, indivs=None):  # Método para obter a aptidão de todos os indivíduos
        if indivs is None:
            indivs = self.indivs # Se não forem fornecidos indivíduos, usa os da população
        return [indiv.fitness for indiv in indivs] # Retorna uma lista de aptidões de cada indivíduo
    def bestSolution(self):
        # Método para encontrar o melhor indivíduo da população
        # O melhor indivíduo é aquele com a maior soma de genes igual a 1
        return max(self.indivs, key=lambda x: sum(1 for gene in x.genes if gene == 1))
    def bestFitness(self):
        # Método para encontrar o indivíduo com a melhor aptidão
        indv = self.bestSolution() # Chama o método bestSolution para obter o melhor indivíduo


    def selection(self, n, indivs=None):  # Método para selecionar n indivíduos com base na aptidão
        fitnesses = self.getFitnesses(indivs)  # Obtém as aptidões dos indivíduos
        selected_indices = []
        for _ in range(n):
            selected_index = fitnesses.index(max(fitnesses)) # Encontra o índice do indivíduo com maior aptidão
            fitnesses[selected_index] = 0.0# Zera a aptidão do indivíduo selecionado para evitar seleção repetida
            selected_indices.append(selected_index)  # Adiciona o índice do indivíduo selecionado à lista
        return selected_indices # Retorna a lista de índices dos indivíduos selecionados
    def roulette(self, f): # Método para realizar a seleção via roleta
        tot = sum(f) # Soma das aptidões
        val = random()# Valor aleatório para a roleta
        acum = 0.0 # Acumulador
        ind = 0 # Índice inicial
        while acum < val: 
            acum += (f[ind] / tot)# Incrementa o acumulador com a fração da aptidão
            ind += 1 # Incrementa o índice
        return ind-1 # Retorna o índice selecionado, ajustado para zero-based
    
    def linscaling(self, fitnesses):  # Método para realizar o escalonamento linear das aptidões
        mx = max(fitnesses) # Obtém a aptidão máxima
        mn = min(fitnesses)  # Obtém a aptidão mínima
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn) # Calcula o valor escalonado
            res.append(val)  # Adiciona o valor escalonado à lista
        return res  # Retorna a lista de aptidões escalonadas

    def recombination(self, parents, noffspring): # Método para realizar a recombinação e gerar descendentes
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]] # Seleciona o primeiro 
            parent2 = self.indivs[parents[new_inds+1]]  # Seleciona o segundo 
            offsp1, offsp2 = parent1.crossover(parent2) # Realiza o crossover
            offsp2.mutation()  # Realiza a mutação no primeiro descendente
            offspring.append(offsp1)  # Adiciona o primeiro descendente à lista de descendentes
            offspring.append(offsp2)  # Adiciona o segundo descendente à lista de descendentes
            new_inds += 2 # Incrementa o contador de novos indivíduos
        return offspring # Retorna a lista de descendentes
    
    def reinsertion(self, offspring): # Método para reinserir os descendentes na população
        tokeep = self.selection(self.popsize-len(offspring)) # Seleciona os indivíduos a serem mantidos
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp] # Substitui o indivíduo da população pelo descendente
                ind_offsp += 1# Incrementa o índice dos descendentes

class EvolAlgorithm:
    def __init__(self, popsize, numits,noffspring, indsize):  # Método construtor da classe EvolAlgorithm
        self.popsize = popsize # Define o tamanho da população
        self.numits = numits # Define o número de iterações
        self.noffspring = noffspring # Define o número de descendentes por iteração
        self.indsize = indsize # Define o tamanho dos indivíduos
    def initPopul(self, indsize): # Método para inicializar a população
        self.popul = Popul(self.popsize, indsize)  # Cria uma nova população

    def evaluate(self, indivs):  # Método para avaliar a aptidão de cada indivíduo
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = sum(1 for gene in ind.genes if gene == 1) # Conta o número de genes iguais a 1
            ind.fitness = fit# Define a aptidão do indivíduo
    
    def iteration(self):  # Método para realizar uma iteração do algoritmo
        parents = self.popul.selection(self.noffspring)  # Seleciona os pais
        offspring = self.popul.recombination(parents, self.noffspring) # Realiza a recombinação para gerar descendentes
        self.evaluate(offspring) # Avalia os descendentes
        self.popul.reinsertion(offspring) # Reinsere os descendentes na população
    def run(self):   # Método para executar o algoritmo evolutivo
        self.initPopul(self.indsize) # Inicializa a população
        self.evaluate(self.popul.indivs)  # Avalia a população inicial
        self.bestsol = self.popul.bestSolution()
        for i in range(self.numits+1):
            self.iteration()
            bs = self.popul.bestSolution()
            if bs > self.bestsol:
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol )

class IndivInt (Indiv):  # Classe que herda da classe Indiv e representa indivíduos com genes inteiros
    def initRandom(self, size): # Método para inicializar aleatoriamente os genes do indivíduo
        self.genes = [] # Inicializa a lista de genes vazia
        for _ in range(size): # Para cada posição no tamanho especificado
            self.genes.append(randint(0, self.ub)) # Adiciona um valor inteiro aleatório entre 0 e o limite superior (ub)
    def mutation(self): # Método para realizar a mutação de um gene aleatório
        s = len(self.genes) # Obtém o tamanho da lista de genes
        pos = randint(0, s-1) # Escolhe uma posição aleatória para mutação
        self.genes[pos] = randint(0, self.ub)  # Substitui o gene nessa posição por um valor inteiro aleatório

class PopulInt(Popul):
    # Classe que herda da classe Popul e representa uma população de indivíduos com genes inteiros
    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub  # Define o limite superior para os genes
        Popul.__init__(self, popsize, indsize, indivs)  # Chama o construtor da classe base Popul
    
    def initRandomPop(self):
        # Método para inicializar a população com indivíduos aleatórios
        self.indivs = []  # Inicializa a lista de indivíduos vazia
        for _ in range(self.popsize):
            # Para cada posição no tamanho da população
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)  # Cria um novo indivíduo com genes inteiros
            self.indivs.append(indiv_i)  # Adiciona o novo indivíduo à população


class EAMotifsInt(EvolAlgorithm):
    # Classe que herda da classe EvolAlgorithm e implementa um algoritmo evolutivo para encontrar motivos em sequências de DNA
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()  # Inicializa um objeto de MotifFinding
        self.motifs.readFile(filename, "dna")  # Lê o arquivo com as sequências de DNA
        indsize = len(self.motifs)  # Define o tamanho dos indivíduos com base no tamanho dos motivos
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)  # Chama o construtor da classe base EvolAlgorithm
    
    def initPopul(self, indsize):
        # Método para inicializar a população
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize  # Calcula o valor máximo para os genes
        self.popul = PopulInt(self.popsize, indsize, maxvalue, [])  # Cria uma nova população de indivíduos com genes inteiros
    
    def evaluate(self, indivs):
        # Método para avaliar a aptidão de cada indivíduo
        for i in range(len(indivs)):
            ind = indivs[i]  # Obtém o indivíduo na posição i
            sol = ind.getGenes()  # Obtém os genes do indivíduo
            fit = self.motifs.score(sol)  # Calcula a aptidão do indivíduo com base na pontuação dos motivos
            ind.setFitness(fit)  # Define a aptidão do indivíduo






