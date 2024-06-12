class BWT:
    """
    Classe que implementa a Transformada de Burrows-Wheeler (BWT), a recuperação da sequência da BWT 
    e a procura de padrões com a BWT (sem e com suffix array)
    ...
    """
    def __init__(self, seq : str = ''):
        """
        Descrição: Construtor da classe BWT
        Parâmetros:
            seq (str): Sequência a inserir com ou sem marcador ('$') no final 
                       Caso a sequência seja inserida sem marcador no final será automaticamente adicionado o marcador ('$') no final da sequência
                       Caso não seja inserida nenhuma sequência este parâmetro assume uma string vazia ('')
        """
        self.seq = seq
        if seq.endswith('$'):
            self.bwt = self.constr_bwt(seq)
        else: self.bwt = self.constr_bwt(seq + '$') if seq else ''
        self.suffix_array = self.constr_suffix_array(seq)
        self.primeira_col = sorted(self.bwt)
        self.c = self.constr_array_c()
        self.occ = self.constr_tabela_occ()

    def definir_bwt(self, bwt : str):
        """
        Descrição: Atualiza a BWT com a string passada como entrada
        Parâmetros:
            bwt (str): BWT a ser definida
        """
        self.bwt = bwt
        self.primeira_col = sorted(self.bwt)
        self.c = self.constr_array_c()
        self.occ = self.constr_tabela_occ()

    def constr_bwt(self, seq : str) -> str:
        """
        Descrição: Constrói a Transformada de Burrows-Wheeler (BWT)
        Parâmetros: 
            seq (str): Sequência fornecida para a contrução da BWT
        Retorna:
            str: Sequência da BWT
        """
        matriz = [seq[i:] + seq[:i] for i in range(len(seq))] # construir a matriz de Burrows-Wheeler
        matriz_ord = sorted(matriz) # ordenar a matriz de Burrows-Wheeler
        ultima_col = [linha[-1:] for linha in matriz_ord] # obter a última coluna da matriz de Burrows-Wheeler
        return ''.join(ultima_col) # retornar uma string com a BWT
    
    def inverso_bwt(self) -> str:
        """
        Descrição: Recupera a sequência original
        Parâmetros:
            seq (str): Sequência da BWT
        Retorna:
            str: Sequência original
        """
        # iniciar uma tabela vazia com número de strings vazias igual ao tamanho da seq
        tabela = [''] * len(self.bwt)
        for _ in range(len(self.bwt)):
            # Adicionar a sequência BWT como uma nova coluna em frente a cada string na tabela
            tabela = sorted([self.bwt[i] + tabela[i] for i in range(len(self.bwt))])
        # A linha correta termina com o marcador ('$')
        for linha in tabela:
            if linha.endswith('$'):
                return linha
        return ''

    def constr_array_c(self):
        """
        Descrição: Constrói o array de contagens (c) necessário para o Last-First (LF) mapping
        """
        c = {}
        sorted_bwt = sorted(self.bwt)
        for car in set(self.bwt):
            c[car] = sorted_bwt.index(car)
        return c

    def constr_tabela_occ(self):
        """
        Descrição: Constrói a tabela de ocurrências (occ) necessária para o Last-First (LF) mapping
        """
        occ = {}
        for car in set(self.bwt):
            occ[car] = [0] * (len(self.bwt) + 1)
        for i in range(1, len(self.bwt) + 1):
            car = self.bwt[i - 1]
            for key in occ:
                occ[key][i] = occ[key][i - 1]
            occ[car][i] += 1
        return occ

    def proc_padroes(self, padrao : str) -> list[int]:
        """
        Descrição: Procura o padrão usando o Last-First (LF) mapping, restringindo o intervalo 
        de linhas que podem conter o padrão e retorna os índices das linhas que contêm o padrão.
        Parâmetros:
            padrao (str): O padrão a procurar na BWT
        Returna:
            list[int]: Lista de índices das linhas que contêm o padrão a procurar
        """
        topo = 0
        fundo = len(self.bwt) - 1
        while topo <= fundo and padrao:
            simbolo = padrao[-1]
            padrao = padrao[:-1]
            if simbolo in self.bwt[topo:fundo + 1]:
                topo = self.c[simbolo] + self.occ[simbolo][topo]
                fundo = self.c[simbolo] + self.occ[simbolo][fundo + 1] - 1
            else:
                return []
        return list(range(topo, fundo + 1))
    
    def constr_suffix_array(self, seq : str) -> list[int]:
        """
        Descrição: Constrói o suffix array para a sequência fornecida
        Parâmetros:
            seq (str): Sequência fornecida
        Returns:
            list[int]: O suffix array da sequência fornecida
        """
        sufixos = sorted((seq[i:], i) for i in range(len(seq)))
        return [sufixo[1] for sufixo in sufixos]
    
    def proc_padroes_sa(self, padrao : str) -> list[int]:
        """
        Descrição: Procura o padrão usando o suffix array, realizando pesquisa binária 
        para encontrar o intervalo de sufixos que contém o padrão e retorna os índices 
        dos sufixos na sequência original.
        Parâmetros:
            padrao (str): O padrão a procurar
        Retorna:
            list[int]: Lista de índices dos sufixos que contêm o padrão a procurar
        """
        esq, dir = 0, len(self.suffix_array)
        while esq < dir:
            meio = (esq + dir) // 2
            if padrao > self.seq[self.suffix_array[meio]:]:
                esq = meio + 1
            else:
                dir = meio
        inicio = esq
        dir = len(self.suffix_array)
        while esq < dir:
            meio = (esq + dir) // 2
            if padrao < self.seq[self.suffix_array[meio]:self.suffix_array[meio] + len(padrao)]:
                dir = meio
            else:
                esq = meio + 1
        fim = dir
        return sorted(self.suffix_array[inicio:fim])