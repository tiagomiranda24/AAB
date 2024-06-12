"""
Código adaptado do professor Miguel Rocha
"""

import random

class Indiv:
    def __init__(self, size, genes=[], lb=0, ub=1):  # Método construtor da classe Indiv
        """
        Inicializa um objeto da classe Indiv.

        Parâmetros:
        size (int): Tamanho do vetor de genes.
        genes (list, opcional): Lista de genes. Se não fornecida, será inicializada aleatoriamente.
        lb (int, opcional): Limite inferior para os valores dos genes. Valor padrão é 0.
        ub (int, opcional): Limite superior para os valores dos genes. Valor padrão é 1.
        """
        self.lb = lb # Define o limite inferior para os genes
        self.ub = ub # Define o limite superior para os genes
        self.genes = genes if genes is not None else []# Lista de genes do indivíduo
        self.fitness = None # Aptidão do indivíduo, inicialmente indefinida
        if not self.genes:# Se não houver genes fornecidos
            self.initRandom(size) # Inicializa os genes aleatoriamente com base no tamanho fornecido

    def initRandom(self, size):  # Método para inicializar os genes de forma aleatória
       """
        Inicializa os genes de forma aleatória.

        Parâmetros:
        size (int): Tamanho do vetor de genes.
        """
       self.genes = [random.choice([0, 1]) for _ in range(size)]# Gera uma lista de genes com valores 0 ou 1

    def mutation(self): # Método para realizar a mutação de um gene aleatório
        """
        Realiza a mutação de um gene aleatório, invertendo seu valor.
        """
        pos = random.randint(0, len(self.genes) - 1) # Escolhe uma posição aleatória para mutação
        self.genes[pos] = 1 - self.genes[pos]# Inverte o valor do gene (0 -> 1 ou 1 -> 0)

    def crossover(self, indiv2): # Método para realizar o crossover com outro indivíduo
        """
        Realiza o crossover com outro indivíduo.

        Parâmetros:
        indiv2 (Indiv): Outro indivíduo para realizar o crossover.

        Retorna:
        tuple: Dois novos indivíduos resultantes do crossover.
        """
        return self.one_pt_crossover(indiv2) # Realiza o crossover de um ponto
    
    def one_pt_crossover(self, indiv2):# Método de crossover de um ponto
       """
        Realiza o crossover de um ponto com outro indivíduo.

        Parâmetros:
        indiv2 (Indiv): Outro indivíduo para realizar o crossover.

        Retorna:
        tuple: Dois novos indivíduos resultantes do crossover de um ponto.
        """
       offsp1 = self.genes[:] # Cria uma cópia dos genes do primeiro indivíduo
       offsp2 = indiv2.genes[:]# Cria uma cópia dos genes do segundo indivíduo
       pos = random.randint(0, len(self.genes) - 1)  # Escolhe um ponto de crossover aleatório
       offsp1[pos:], offsp2[pos:] = offsp2[pos:], offsp1[pos:]# Troca os genes após o ponto de crossover
       return Indiv(len(self.genes), offsp1, self.lb, self.ub), Indiv(len(self.genes), offsp2, self.lb, self.ub) # Retorna dois novos indivíduos resultantes do crossover

 
 
class Popul:  
    def __init__(self, popsize, indsize, indivs=[]): # Método construtor da classe Popul
        """
        Inicializa um objeto da classe Popul.

        Parâmetros:
        popsize (int): Tamanho da população.
        indsize (int): Tamanho dos indivíduos.
        indivs (list, opcional): Lista de indivíduos. Se não fornecida, será inicializada aleatoriamente.
        """
        self.popsize = popsize  # Define o tamanho da população
        self.indsize = indsize # Define o tamanho dos indivíduos
        self.indivs = indivs if indivs is not None else []   # Lista de indivíduos na população

        if not self.indivs: #Se não houver indivíduos fornecidos
            self.initRandomPop() # Inicializa a população aleatoriamente

    def getIndiv(self, index):  # Método para obter um indivíduo pelo índice
        """
        Obtém um indivíduo pelo índice.

        Parâmetros:
        index (int): Índice do indivíduo na população.

        Retorna:
        Indiv: Indivíduo na posição especificada.
        """
        

        
        return self.indivs[index] # Retorna o indivíduo na posição especificada
    
    def initRandomPop(self):  # Método para inicializar a população com indivíduos aleatórios

        """
        Inicializa a população com indivíduos aleatórios.
        """
        self.indivs = [Indiv(self.indsize) for _ in range(self.popsize)]# Cria indivíduos aleatórios

    def getFitnesses(self, indivs=None):  # Método para obter a aptidão de todos os indivíduos

        """
        Obtém a aptidão de todos os indivíduos.

        Parâmetros:
        indivs (list, opcional): Lista de indivíduos. Se não fornecida, será utilizada a população atual.

        Retorna:
        list: Lista de aptidões de cada indivíduo.
        """
        if indivs is None:
            indivs = self.indivs # Se não forem fornecidos indivíduos, usa os da população
        return [indiv.fitness for indiv in indivs] # Retorna uma lista de aptidões de cada indivíduo
    def bestSolution(self):
        """
        Encontra o melhor indivíduo da população com base na soma dos genes iguais a 1.

        Retorna:
        Indiv: Melhor indivíduo da população.
        """
        # Método para encontrar o melhor indivíduo da população
        # O melhor indivíduo é aquele com a maior soma de genes igual a 1
        return max(self.indivs, key=lambda x: sum(1 for gene in x.genes if gene == 1))
    def bestFitness(self):
        # Método para encontrar o indivíduo com a melhor aptidão
        """
        Encontra o indivíduo com a melhor aptidão.

        Retorna:
        Indiv: Indivíduo com a melhor aptidão.
        """
        
        indv = self.bestSolution() # Chama o método bestSolution para obter o melhor indivíduo


    def selection(self, n, indivs=None):  # Método para selecionar n indivíduos com base na aptidão
        """
        Seleciona n indivíduos com base na aptidão.

        Parâmetros:
        n (int): Número de indivíduos a serem selecionados.
        indivs (list, opcional): Lista de indivíduos. Se não fornecida, será utilizada a população atual.

        Retorna:
        list: Lista de índices dos indivíduos selecionados.
        """
        
        
        fitnesses = self.getFitnesses(indivs)  # Obtém as aptidões dos indivíduos
        selected_indices = []
        for _ in range(n):
            selected_index = fitnesses.index(max(fitnesses)) # Encontra o índice do indivíduo com maior aptidão
            fitnesses[selected_index] = 0.0# Zera a aptidão do indivíduo selecionado para evitar seleção repetida
            selected_indices.append(selected_index)  # Adiciona o índice do indivíduo selecionado à lista
        return selected_indices # Retorna a lista de índices dos indivíduos selecionados
    def roulette(self, f): # Método para realizar a seleção via roleta
        
        """
        Realiza a seleção via roleta.

        Parâmetros:
        f (list): Lista de aptidões dos indivíduos.

        Retorna:
        int: Índice selecionado.
        """
        
        tot = sum(f) # Soma das aptidões
        val = random.random()# Valor aleatório para a roleta
        acum = 0.0 # Acumulador
        ind = 0 # Índice inicial
        while acum < val: 
            acum += (f[ind] / tot)# Incrementa o acumulador com a fração da aptidão
            ind += 1 # Incrementa o índice
        return ind-1 # Retorna o índice selecionado, ajustado para zero-based
    
    def linscaling(self, fitnesses):  # Método para realizar o escalonamento linear das aptidões
        
        """
        Realiza o escalonamento linear das aptidões.

        Parâmetros:
        fitnesses (list): Lista de aptidões dos indivíduos.

        Retorna:
        list: Lista de aptidões escalonadas.
        """
        
        mx = max(fitnesses) # Obtém a aptidão máxima
        mn = min(fitnesses)  # Obtém a aptidão mínima
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn) # Calcula o valor escalonado
            res.append(val)  # Adiciona o valor escalonado à lista
        return res  # Retorna a lista de aptidões escalonadas

    def recombination(self, parents, noffspring): # Método para realizar a recombinação e gerar descendentes
        """
        Realiza a recombinação e gera descendentes.

        Parâmetros:
        parents (list): Lista de índices dos pais.
        noffspring (int): Número de descendentes a serem gerados.

        Retorna:
        list: Lista de descendentes gerados.
        """
        
        
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
        
        """
        Reinserir os descendentes na população.

        Parâmetros:
        offspring (list): Lista de descendentes.
        """
        
        
        
        tokeep = self.selection(self.popsize-len(offspring)) # Seleciona os indivíduos a serem mantidos
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp] # Substitui o indivíduo da população pelo descendente
                ind_offsp += 1# Incrementa o índice dos descendentes

class EvolAlgorithm:

    
    def __init__(self, popsize, numits, noffspring, indsize):  # Método construtor da classe EvolAlgorithm
        """
        Inicializa um objeto da classe EvolAlgorithm.

        Parâmetros:
        popsize (int): Tamanho da população.
        numits (int): Número de iterações.
        noffspring (int): Número de descendentes por iteração.
        indsize (int): Tamanho dos indivíduos.
        """ 
        self.popsize = popsize # Define o tamanho da população
        self.numits = numits # Define o número de iterações
        self.noffspring = noffspring # Define o número de descendentes por iteração
        self.indsize = indsize # Define o tamanho dos indivíduos
        self.initPopul(self.indsize) # Inicializa a população

    
    def initPopul(self, indsize):

        """
        Inicializa a população.

        Parâmetros:
        indsize (int): Tamanho dos indivíduos.
        """
        # Método para inicializar a população
        self.popul = Popul(self.popsize, indsize)  # Cria uma nova população


    def evaluate(self, indivs):  # Método para avaliar a aptidão de cada indivíduo
        """
        Avalia a aptidão de cada indivíduo.

        Parâmetros:
        indivs (list): Lista de indivíduos a serem avaliados.
        """
        
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = sum(1 for gene in ind.genes if gene == 1) # Conta o número de genes iguais a 1
            ind.fitness = fit# Define a aptidão do indivíduo
    
    def iteration(self):  # Método para realizar uma iteração do algoritmo
        """
        Realiza uma iteração do algoritmo evolutivo.
        """
        
        self.evaluate(self.popul.indivs)  # Avalia a aptidão dos indivíduos
        parents = self.popul.selection(self.noffspring)  # Seleciona os pais
        offspring = self.popul.recombination(parents, self.noffspring) # Realiza a recombinação para gerar descendentes
        self.popul.reinsertion(offspring) # Reinsere os descendentes na população
    
    def run(self):   # Método para executar o algoritmo evolutivo
        
        """
        Executa o algoritmo evolutivo.
        """
        self.bestsol = self.popul.bestSolution()
        for i in range(self.numits):
            self.iteration()
            bs = self.popul.bestSolution()
            if bs > self.bestsol:
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol )
