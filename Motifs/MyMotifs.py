"""
author: miguelrocha
"""

def createMatZeros(nl: int, nc: int) -> list[list[int]]:
    """
    Cria uma matriz de zeros com o número de linhas e colunas especificado.
    Args:
        nl (int): Número de linhas da matriz.
        nc (int): Número de colunas da matriz.
    Returns:
        list[list[int]]: Matriz de zeros com o número de linhas e colunas especificado.
    """
    return [[0] * nc for _ in range(nl)]


def printMat(mat: list[list[int]]) -> None:
    """
    Imprime a matriz.
    Args:
        mat (list[list[int]]): Matriz a ser impressa.
    Returns:
        None
    """
    for row in mat:
        print(row)


class MyMotifs:
    def __init__(self, seqs: list[str]) -> None:
        """
        Construtor da classe MyMotifs.
        Args:
            seqs (list[str]): Lista de sequências.
        """
        self.size = len(seqs[0])
        self.seqs = seqs
        self.alphabet = seqs[0].alfabeto()
        self.doCounts()
        self.createPWM()

        
    def __len__(self) -> int:
        """
        Retorna o tamanho do conjunto de sequências.
        Returns:
            int: Tamanho das sequências.
        """
        return self.size
        
        
    def doCounts(self) -> None:
        """
        Calcula a contagem de cada base por posição e guarda a matriz de contagem em 'self.counts'.
        """
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for seq in self.seqs:
            for i, base in enumerate(seq):
                lin = self.alphabet.index(base)
                self.counts[lin][i] += 1

                
    def createPWM(self) -> None:
        """
        Calcula e armazena a matriz PWM (Position Weight Matrix) do conjunto de sequências.
        Esta matriz é calculada a partir da matriz de contagem armazenada em 'self.counts'.
        """
        if self.counts is None:
            self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = self.counts[i][j] / len(self.seqs)

                
    def consensus(self) -> str:
        """
        Retorna a sequência de consenso para o conjunto de sequências.
        Returns: 
            Sequência de consenso.
        """
        res = ""
        for j in range(self.size):
            max_count = self.counts[0][j]
            max_base_index = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > max_count: 
                    max_count = self.counts[i][j]
                    max_base_index = i
            res += self.alphabet[max_base_index]
        return res


    def maskedConsensus(self) -> str:
        """
        Retorna a sequência de consenso para o conjunto de sequências de DNA,
        onde as posições com contagem abaixo de 50% da contagem total das sequências são substituídas por '-'.
        
        Returns: 
            Sequência de consenso com posições abaixo do limiar substituídas por '-'.
        """
        res = ""
        for j in range(self.size):
            max_count = self.counts[0][j]
            max_base_index = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > max_count: 
                    max_count = self.counts[i][j]
                    max_base_index = i
            if max_count > len(self.seqs) / 2:
                res += self.alphabet[max_base_index]        
            else:
                res += "-"
        return res


    def probabSeq(self, seq: str) -> float:
        """
        Calcula a probabilidade de uma sequência ser gerada pela matriz PWM.
        Args:
            Sequência de DNA a ser avaliada.
        Returns: 
            Probabilidade da sequência ser gerada pela matriz PWM.
        """
        res = 1.0
        for i, base in enumerate(seq):
            lin = self.alphabet.index(base)
            res *= self.pwm[lin][i]
        return res

    
    def probAllPositions(self, seq: str) -> list[float]:
        """
        Calcula a probabilidade do motivo aparecer em cada posição possível da sequência especificada.
        Args: 
            Sequência de DNA na qual procurar o motivo.
        Returns:
            Lista de probabilidades do motivo aparecer em cada posição possível.
        """
        res = []
        for k in range(len(seq) - self.size + 1):
            res.append(self.probabSeq(seq))
        return res


    def mostProbableSeq(self, seq: str) -> int:
        """
        Encontra a posição mais provável para o motivo na sequência especificada.
        Args: 
            Sequência de DNA na qual procurar o motivo.
        Returns: 
            Índice da posição mais provável para o motivo.
        """
        max_probability = -1.0
        max_index = -1
        for k in range(len(seq) - self.size):
            probability = self.probabSeq(seq[k:k + self.size])
            if probability > max_probability:
                max_probability = probability
                max_index = k
        return max_index


def test():
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat(motifs.counts)
    printMat(motifs.pwm)
    print(motifs.alphabet)
    
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()