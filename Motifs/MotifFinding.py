from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size:int = 8, seqs:list = None)-> None:
        """
        Construtor com os atributos necessários para a class Motif_Finding
        Args:
            size: vê o tamanho do motif, em caso de não ser definido recebe o valor 8
        Returns:
            seqs: lista com as sequências, recebe None se não forem dadas sequências e teremos uma lista vazia
        """
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self) -> int:
        """
        Indica o número de elementos/sequências presentes na lista self.seqs
        Returns:
            int: número de elementos da lista
        """
        return len(self.seqs)
    
        
    def __getitem__(self, n) -> str:
        """
        Interface para a indexação []
        """
        return self.seqs[n]
    
    def seqSize (self, i: int) -> int:
        """
        Comprimento da sequência i que está presente na lista self.seqs
        """
        return len(self.seqs[i])
    
    def readFile(self, fic:str, t:str) -> None:
        """
        Função que lê ("r") um ficheiro, separa por espaços cada sequência (strip), e adiciona cada sequência à lista self.seqs
        Args:
            fic : ficheiro a ser lido
            t : tipo de sequência
        """
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes: list[int]) -> MyMotifs:
        """
        Cria uma matriz, a partir da definição da posição onde o motif começará a ser contado e onde termina, 
        identificando o seu tipo (t). Esta informação é adicionada à lista pseqs, que é uma lista de motifs.
        Args:
            indexes: lista de índices que indicam a posição inicial de cada sequência no conjunto de sequências.
        Returns:
            objeto MyMotifs com as sequências de motif.
        """
        pseqs = []
        for i, ind in enumerate(indexes):
            # Verifica se o índice é um inteiro válido
            if isinstance(ind, int):
                # Verifica se o índice está dentro dos limites da sequência
                if 0 <= ind <= len(self.seqs[i]) - self.motifSize:
                    pseqs.append(MySeq(self.seqs[i][ind:(ind + self.motifSize)], self.seqs[i].tipo))
                else:
                    # Se o índice estiver fora dos limites, emite um aviso
                    print(f"Índice inválido para a sequência {i}: {ind}")
            else:
                # Se o índice não for um inteiro válido, emite um aviso
                print(f"Índice inválido para a sequência {i}: {ind}")

        return MyMotifs(pseqs)

        
        
    # SCORES
          
    def score(self, s:int) -> list[int]:
        """
        Calcula o score do motif representado pelos índices 's', que indicam a posição inicial de cada sequência no 
        conjunto de sequências. O score é a soma das maiores contagens em cada coluna da matriz de contagem do motif.
        Args:
            s: Índices que indicam a posição inicial de cada sequência no conjunto de sequências.
        Returns:
            Lista com os scores para cada posição inicial.
        """
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts

        if mat:  # Verifica se mat não está vazio
            # Percorre cada coluna da matriz de contagem
            for j in range(len(mat[0])):
                maxcol = max(mat[i][j] for i in range(len(mat)))  # Encontra o valor máximo em cada coluna
                score += maxcol  # Adiciona o valor máximo da coluna ao score
        return score  # Retorna o score total

    
    def scoreMult(self, s:int)->float:
        """
        Calcula o score do motif representado pelos índices 's', que indicam a posição inicial de cada sequência no conjunto 
        de sequências. O score é o produto das probabilidades das bases do motif, calculadas a partir da matriz de frequência 
        do motif.
        Args:
            s: Índices que indicam a posição inicial de cada sequência no conjunto de sequências
        Returns:
            Score do motif representado pelos índices 's'
        """
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for col in zip(*mat):  # Transforma linhas em colunas
            maxcol = max(col)  # Encontra o valor máximo em cada coluna
            score *= maxcol  # Multiplica o score pelo valor máximo da coluna

        return score  # Retorna o score total 
             
        
    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s:list[int])->list[int]:
        """
        Encontra a próxima solução no espaço de procura para a posição do Motif. 
        Args:
            s:vetor de posições de Motif
        Returns:
            A próxima solução, ou None se não houver mais soluções
        
        """
        pos = len(s) - 1 # Inicia a verificação pela última posição do vetor de posições
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1 # Move para a posição anterior até encontrar uma posição que não atinja o limite
        if pos < 0:
            return None   

        nextS = s[:]  # Copia o vetor de posições atual para a próxima solução
        nextS[pos] += 1  # Incrementa a posição atual em 1 para encontrar a próxima solução válida
        for i in range(pos + 1, len(s)):
            nextS[i] = 0   # Reinicia todas as posições à direita da posição incrementada para 0

        return nextS  # Retorna a próxima solução válida
    
        
    def exhaustiveSearch(self)->list[int]:
        """
        Calcula o score de cada possível vetor de posições para o Motif e retorna a posição com o melhor score
        Returns:
            vetor de posições do Motif com o melhor score encontrado
        """
        melhorScore = -1    # Inicializa o melhor score como -1
        res = []    # Inicializa a lista de posições do Motif com o melhor score encontrado
        s = [0]* len(self.seqs) # Inicializa o vetor de posições do Motif com todas as sequências no início
        while (s!= None):   # Loop para encontrar a melhor solução
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s   # Atualiza as posições do Motif correspondentes ao melhor score
            s = self.nextSol(s)    # Obtém a próxima solução no espaço de busca
        return res
      
           
        
    # BRANCH AND BOUND     
     
    def nextVertex(self, s: list[int]) -> list[int]:
        """
        Dada uma solução parcial `s`, retorna a próxima solução candidata na árvore de procura.
        Args:
            s: Uma solução parcial.
        Returns:
            A próxima solução candidata na árvore de procura.
        """
        if len(s) < len(self.seqs):  # Verifica se é um nó interno (ainda há sequências para processar)
            return s + [0]  # Desce um nível na árvore de busca

        # Bypass
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1

        if pos < 0:  # Se todas as posições tiverem atingido o limite, retorna None, indicando que é a última solução
            return None  

        return s[:pos] + [s[pos] + 1]
    
    
    def bypass(self, s: list[int]) -> list[int]:
        """
        Dada uma solução parcial `s`, retorna a próxima solução candidata na árvore de procura saltando um nível.
        Args:
            s: Solução parcial.
        Returns:
            A próxima solução candidata na árvore de procura, ou None se não houver mais soluções possíveis.
        """
        pos = len(s) - 1  # Inicializa a posição como a última no vetor de posições
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:  # Encontra a posição onde ainda é possível aumentar
            pos -= 1

        if pos < 0: # Se todas as posições tiverem atingido o limite
            return None  

        return s[:pos] + [s[pos] + 1]
    
    
    def branchAndBound(self) -> list[int]:
        """
        Encontra o melhor vetor de posições do motivo usando o método Branch and Bound.
        Returns:
            O melhor vetor de posições do motivo encontrado, ou None se não houver soluções possíveis.
        """
        melhorScore = -1 # Inicializa a melhor pontuação como -1
        melhorMotif = None # Inicializa o melhor motivo como None
        size = len(self.seqs)  # Obtém o tamanho do conjunto de sequências
        s = [0] * size   # Inicializa o vetor de posições com zeros

        while s is not None:   # Enquanto houver soluções disponíveis
            if len(s) < size:
                optimScore = self.score(s) + (size - len(s)) * self.motifSize
                if optimScore < melhorScore:
                    s = self.bypass(s)
                else:
                    s = self.nextVertex(s) # Passa para a próxima solução
            else:   # Se o comprimento do vetor de posições for igual ao tamanho do conjunto de sequências
                sc = self.score(s)  # Calcula a pontuação da solução atual
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif = s
                s = self.nextVertex(s)

        return melhorMotif
    
   # Consensus (heuristic)
  
    def heuristicConsensus(self)->list[int]:
        """
        Considera apenas as duas primeiras sequências, escolhe as posições inicias que dão um melhor score, e isto dá o melhor score parcial. Depois itera para as restantes sequências e seleciona a posição que maximiza o score.
        Returns:
            vetor de posições que produz o melhor alinhamento do motif em todas as sequências
        """
        #Passo 1: Considerando apenas as duas primeiras sequências, escolher as posições iniciais s1 e s2 que dão um melhor score (melhor contribuição parcial para o score, i.e. considerando que existem apenas estas duas sequências).
        find = MotifFinding(self.motifSize, self.seqs[:2])
        es = find.exhaustiveSearch()

        #Passo 2: Para cada uma das sequências seguintes (i=3, …,t) , de forma iterativa, escolher a melhor posição inicial na sequência i, de forma a maximizar o score, considerando as posições anteriores fixas
        for p in range(2, len(self.seqs)):
            es.append(p)
            max_score = -1
            bestpos = 0
            for g in range (self.seqSize(p)-self.motifSize+1):
                es[p] = g   #vetor das posições
                score = self.score(es)
                if score > max_score:
                    max_score = score
                    bestpos = g
                es[p] = bestpos
        return es

    def heuristicStochastic (self)->list[str]:
        """
        Implementa a heurística estocástica para encontrar o melhor motif a partir das sequências fornecidas
        Returns: 
            Retorna a lista de posições dos motifs, ou None caso a busca não tenha obtido sucesso
        """
        from random import randint
        s = [0] * len(self.seqs)
        #Passo 1: Seleciona as posições iniciais de forma aleatória
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)  # como é random, pode escolher um otimo local mas não uma solução ótima
        #Passo 2: Cria um perfil P a partir das posições geradas no passo 1
        best_score = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
        #Passo 3: Descobrir o segmento mais provável em cada sequência usando P
            for i in range(len(self.seqs)):
                s[i] = motif.mostProbableSeq(self.seqs[i])
        #Passo 4: caclula um novo perfil P baseado nas posições calculadas em 3
            scr = self.score(s)
            if scr < best_score:
                best_score = scr
            else:
                improve = False
            return s
        return None


    # Gibbs sampling 
    def gibbs (self, iterations:int) -> list[int]:
        """
        Implementa o algoritmo de Gibbs Sampling
        Args:
            iterations : número inteiro de iterações 
        Returns:
            best_score: float do melhor score até ao fim da ultima iteração
            s: lista das posições inicias dos motifs nas sequências
        """
        from random import randint
        seqPos = []
        for i in range(0, len(self.seqs)):
            randPos = randint(0, self.seqSize(i)-self.motifSize-1)
            seqPos.append(randPos)
        best_score = self.scoreMult(seqPos) #calcula o score com base nas seqs da lista s

        x=0
        while x<iterations:
            x+=1

            randSeq = randint(0, (len(self.seqs)-1)) #Passo 2
           
            random = self.seqs[randSeq]
            seqNoRandom = self.seqs.pop(randSeq)  #remove-se a sequência escolhida aleatoriamente anteriormente
            aux_seq_list = seqPos.copy()          #lista auxiliar com todas as posições
            aux_seq_list.pop(randSeq) #remover a posição da sequência escolhida aleatoriamente na lista s com as posições iniciais
            pwm = self.createMotifFromIndexes(aux_seq_list)#criação do perfil sem a sequência removida
            pwm.createPWM() 

            probPos= pwm.probAllPositions(random) #Obter a melhor posição
            self.seqs.insert(randSeq,seqNoRandom) #Inserir a sequencia aleatoria 
            pos = self.roulette(probPos)
            aux_seq_list.insert(randSeq,pos)
            new_score = self.scoreMult(aux_seq_list)
               
            if  new_score > best_score: #Verifica se houve melhoria  
                best_score = new_score
                best_s = list(seqPos)
        return best_score, best_s

    def roulette(self, f: list[int]) -> int:
        """
        Seleciona um índice aleatório com base na probabilidade de cada elemento em f
        Args:
            f: Lista de valores de probabilidade
        Returns: 
            Índice aleatório selecionado com base nas probabilidades em f
        """
        from random import random  # Importa a função random do módulo random

        tot = 0.0  # Soma total das probabilidades
        for x in f:
            tot += (0.01 + x)  # Soma total, adicionando 0.01 a cada valor de probabilidade

        val = random() * tot  # Valor aleatório entre 0 e a soma total de probabilidades
        acum = 0.0  # Acumulação das probabilidades
        ind = 0  # Índice
        while acum < val:  # Enquanto a acumulação for menor que o valor aleatório gerado
            acum += (f[ind] + 0.01)  # Adiciona a probabilidade atual à acumulação, adicionando 0.01
            ind += 1  # Incrementa o índice
        return ind - 1  # Retorna o índice selecionado, subtraindo 1 para ajustar ao índice da lista



# tests

def test1():  
    sm = MotifFinding()
    sm.readFile(r"C:\Users\tiago\OneDrive\Ambiente de Trabalho\Motifs\exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile(r"C:\Users\tiago\OneDrive\Ambiente de Trabalho\Motifs\exemploMotifs.txt", "dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile(r"C:\Users\tiago\OneDrive\Ambiente de Trabalho\Motifs\exemploMotifs.txt", "dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    

if __name__ == "__main__":
    print("Test 1:")
    test1()
    print()
    print("-----------")
    print("Test 2:")
    test2()
    print()
    print("-----------")
    print("Test 3:")
    test3()
    print()
    print("-----------")
    print("Test 4:")
    test4()
    print()
    print("-----------")
    print("DONE")