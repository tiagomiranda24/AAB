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
        
        
    def createMotifFromIndexes(self, indexes:int) -> list[int]:
        """
        Crição de uma matriz, a partir da definição da posição onde o motif começará a ser contado e onde termina, 
        identificando o seu tipo (t). Esta info é adicionada à lista pseqs, que é uma lista de motifs
        Args:
            indexes : indica a posição pela qual vamos começar a contar o motif
        Returns:
            objeto MyMotifs com as sequências de motif
        """
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s:int) -> list[int]:
        """
        Calcula o escore do motif representado pelos índices 's', que indicam a posição inicial de cada sequência no 
        conjunto de sequências. O score é a soma das maiores contagens em cada coluna da matriz de contagem do motif
        Args:
            s: Índices que indicam a posição inicial de cada sequência no conjunto de sequências
        Returns:
            lista com os scores para cada posição inicial
        """
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):   #colunas da matriz
            maxcol = mat[0][j]          #a cada ronda, define que aquela coluna é maxima e a primeira linha
            for  i in range(1, len(mat)):   
                if mat[i][j] > maxcol:   #se houver outra linha da coluna máxima que seja maior que a definida antes, admitimos nova maxcol
                    maxcol = mat[i][j]
            score += maxcol             #adiciona o valor de cada coluna ao score
        return score                    #lista das várias colunas com valores maiores das linhas = score
   
    def scoreMult(self, s:int)->float:
        """
        Calcula o escore do motif representado pelos índices 's', que indicam a posição inicial de cada sequência no conjunto 
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
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s:list[int])->list[int]:
        """
        Encontra a próxima solução no espaço de procura para a posição do Motif. 
        Args:
            s:vetor de posições de Motif
        Returns:
            A próxima solução, ou None se não houver mais soluções
        
        """
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1;
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self)->list[int]:
        """
        Calcula o score de cada possível vetor de posições para o Motif e retorna a posição com o melhor score
        Returns:
            vetor de posições do Motif com o melhor score encontrado
        """
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while (s!= None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s:list[int])->list[int]:
        """
        Dada uma solução parcial `s`, retorna a próxima solução candidata na árvore de procura
        Args:
            s: Uma solução parcial
        Returns:
            A próxima solução candidata na árvore de procura
        """
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s:list[int])->list[int]:
        """
        Dada uma solução parcial `s`, retorna a próxima solução candidata na árvore de procura saltando um nível.
        Args:
            s: solução parcial.
        Returns:
            A próxima solução candidata na árvore de procura, ou None se não houver mais soluções possíveis.
        """
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound (self)->list[int]:
        """
        Encontra o melhor vetor de posições do motivo usando o método Branch and Bound
        Returns:
            O melhor vetor de posições do motivo encontrado, ou None se não houver soluções possíveis
        """
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
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
            s[i] = randint(0, self.seqSize(i) - self.motifSize)  #como é random, pode escolher um otimo local mas não uma solução ótima
        #Passo 2: Cria um oerfuk P a partir das posições geradas no passo 1
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
            aux_seq_list = seqPos.copy()  #lista auxiliar com todas as posições
            aux_seq_list.pop(randSeq)  #remover a posição da sequência escolhida aleatoriamente na lista s com as posições iniciais
            pwm = self.createMotifFromIndexes(aux_seq_list)#criação do perfil sem a sequência removida
            pwm.createPWM() 

            probPos= pwm.probAllPositions(random) #Obter a melhor posição
            self.seqs.insert(randSeq,seqNoRandom)#Inserir a sequencia aleatoria 
            pos = self.roulette(probPos)
            aux_seq_list.insert(randSeq,pos)
            new_score = self.scoreMult(aux_seq_list)
               
            if  new_score > best_score: #Verifica se houve melhoria  
                best_score = new_score
                best_s = list(seqPos)
        return best_score, best_s

    def roulette(self, f:list[int])->int:
        """
        Seleciona um índice aleatório com base na probabilidade de cada elemento em f
        Args:
            f: Lista de valores de probabilidade
        Returns: 
            Índice aleatório selecionado com base nas probabilidades em f
        """
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

#EX com pseudo contagens

    def scoreEX(self, m): #responsável por calcular a contagem com as pseudo contagens
            score = 0
            motif = self.createMotifFromIndexes(m)
            motif.doCounts() #cria a matriz de contagens
            mat = [] #lista vazia qeu vai servir como matriz depois
            for i in range(len(motif.counts)): #vai correr as linhas da matriz com as counts
                linha = []
                for j in range(len(motif.counts[i])):
                    linha.append(motif.counts[i][j] + 1) #não permite que haja 0 possibilitando as pseudo contagens
                mat.append(linha)
            for k in range(len(mat[0])): #vai correr as colunas da matriz
                maxcol = mat[0][k] #vai dizer que o maxcolun vai ser igual ao primeiro elemento da coluna
                for f in range(1, len(mat)): #vai começar no segundo elemento da coluna e vai comparar com todos os elementos da coluna para ver qual é o maior
                    if mat[f][k] > maxcol:
                        maxcol = mat[f][k]
                score += maxcol #vai adionar esse valor a coluna
            return score #vai dar o score da consenso

    def probabSeqEX (self, seq, pwm): #vai calcular a probabilidade de a seq fazer parte deste quadro sendo que todos os elementos do quadro nao tem valores negativos
        res = 1.0
        for i in range(self.motifSize):
            lin = self.alphabet.index(seq[i])
            res *= pwm[lin][i] #damos a pwm e nao usamso o self.pwm por causa de termos substituido os 0
        return res #da a probabilidade de cada seq ocorrer

    def mostProbableSeqEX(self, seq, pwm): #vai ver qual a posição inicial da subseq de uma seq de comprimento indefenido encaixa melhor no quandro de motifs das seqs
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.motifSize):
            p = self.probabSeqEX(seq[k:k+ self.motifSize], pwm)
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind

    def probAllPositionsEX(self, seq, pwm): #este em vez de calcular a probabilidade de acontecer devolve uma lista com as probabilidades de acontecer em cada letra da seq
        res = []
        for k in range(len(seq)-self.motifSize+1):
            res.append(self.probabSeqEX(seq, pwm))
        return res

    def heuristicStochastic_EX(self):
        from random import randint
        s = [0] * len(self.seqs) #gera um vetor aleatório com o mesmo tamanho do nº de seqs qeu existem
        #passo 1
        for i in range(len(self.seqs)): #indica todas as posições com valores aleatórios
            s[i] = randint(0, self.seqSize(i) - self.motifSize) #como é random pode escolher um otimo local mas não a solução otima
        #Passo 2
        melhorscore = self.scoreEX(s) #vai fazer o score consoante o novo score2 que não vai conter valores 0 já com as pseudos contagens
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s) #constroi o perfil com base nas posições iniciais s
            motif.createPWM() #vai criar a matriz PWM
            newPWM = [] #vai construir a matriz PWM sem nenhum numero negativo já com as pseudo contagens
            for k in range(len(motif.pwm)):
                linhas = []
                for t in range(len(motif.pwm[0])):
                    linhas.append(motif.pwm[k][t] + 0.1) #quando ao probabilidade seri a0 passa a ser 0.1
                newPWM.append(linhas)
            #Passo 3
            for i in range(len(self.seqs)): #avalia a melhor posicao inicial para cada seq
                s[i] = self.mostProbableSeqEX(self.seqs[i], newPWM) #vai ver em cada seq de self.seqs, qual é a subseq nelas que é mais provável de acontecer no quandro PWM
            # passo 4
            # verifica se houve melhoria
            scr = self.scoreEX(s) #vai calcular o score
            if scr > melhorscore: #se o score melhorou volta a repetir o processo se não acaba e devolve as melhores posições das subseqs
                melhorscore = scr
            else:
                improve = False
        return s

    def gibbsEX (self, iterations = 1000):
        # vai tentar aproximar da solução otima em vez dos otimos locais
        from random import randint
        s = [] #cria a lsiat s de posições iniciais
        # passo 1 indica todas as posições com valores aleatórios(vetor inicializado de forma aleatória)
        for i in range(len(self.seqs)):
             s.append(randint(0, len(self.seqs[i]) - self.motifSize -1)) #escolher um numero random de start para cada sequência
        melhorscore = self.scoreEX(s) #calcular o score de s
        bests = list(s)
        for it in range(iterations):
            # passo 2: esolher uma das seqs aleatoriamente
            seq_idx = randint(0, len(self.seqs) - 1) #retira uma seq aleatória
            # passo 3: cria o perfil sem a seq escolhida aleatoriamente
            seq = self.seqs[seq_idx]
            s.pop(seq_idx)
            removed = self.seqs.pop(seq_idx) #vai dar pop da seq na lista e guardar no removed
            motif = self.createMotifFromIndexes(s) #Cria o perfil sem a sequência removida
            motif.createPWM()
            newPWM = [] #vai contruir a matriz PWM sem nenhum numero negativo já com as pseudo contagens
            for k in range(len(motif.pwm)):
                linhas = []
                for t in range(len(motif.pwm[0])):
                    linhas.append(motif.pwm[k][t] + 0.1) #substitiu as probabilidade de 0 por 0.1
                newPWM.append(linhas)
            self.seqs.insert(seq_idx, removed) #vai voltar a adicionar a seq removida a lista de seqs na posição seq_idx
            r = self.probAllPositionsEX(seq, newPWM) #vai calcular a probabilidade de todas as subseqs possiveis na seq removida
            pos = self.roulette(r) #vai fazer o roulette da lista e escolher um dos valores com valores maior que 0, devolvendo a posição onde se iniciou o motif
            s.insert(seq_idx, pos) #vai adicionar o valor da pos do motif ao s na posição seq_idx
            score = self.scoreEX(s) #vai calcular o score do novo s
            if score > melhorscore: #vai ver se este é maior que o melhor scor se for, o melhorscore passa a ser o score e a bests passa a ser a s
                melhorscore = score
                bests = list(s)
        return bests #vai dar return do s    

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
    
    sol2 = mf.gibbs(1000)
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))


if __name__ == "__main__":
    print("Test 1:")
    test1()
    print()
    print("Test 2:")
    test2()
    print()
    print("Test 3:")
    test3()
    print()
    print("Test 4:")
    test4()
    print("DONE")