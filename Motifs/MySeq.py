class MySeq:

    def __init__(self, seq, tipo="dna"):
        """
        Inicializa um objeto MySeq com uma sequência e um tipo (default é "dna").
        """
        self.seq = seq.upper()
        self.tipo = tipo

    def __len__(self):
        """
        Retorna o comprimento da sequência.
        """
        return len(self.seq)
    
    def __getitem__(self, n):
        """
        Retorna o elemento na posição n da sequência.
        """
        return self.seq[n]

    def __getslice__(self, i, j):
        """
        Retorna uma fatia da sequência, do índice i ao j.
        """
        return self.seq[i:j]

    def __str__(self):
        """
        Retorna uma representação em string do objeto MySeq.
        """
        return self.tipo + ":" + self.seq

    def printseq(self):
        """
        Imprime a sequência.
        """
        print(self.seq)
    
    def alfabeto(self):
        """
        Retorna o alfabeto correspondente ao tipo de sequência.
        """
        if (self.tipo=="dna"): return "ACGT"
        elif (self.tipo=="rna"): return "ACGU"
        elif (self.tipo=="protein"): return "ACDEFGHIKLMNPQRSTVWY"
        else: return None
    
    def valida(self):
        """
        Valida se a sequência contém apenas elementos do alfabeto correspondente ao tipo.
        """
        alf = self.alfabeto()
        res = True
        i = 0
        while i < len(self.seq) and res:
            if self.seq[i] not in alf: 
                res = False
            else: i += 1
        return res 
    
    def validaER(self):
        """
        Valida a sequência usando expressões regulares.
        """
        import re
        if (self.tipo=="dna"):
            if re.search("[^ACTGactg]", self.seq) != None: return False
            else: return True 
        elif (self.tipo=="rna"):
            if re.search("[^ACUGacug]", self.seq) != None:  return False
            else: return True
        elif (self.tipo=="protein"):
            if re.search("[^ACDEFGHIKLMNPQRSTVWY_acdefghiklmnpqrstvwy]", self.seq) != None:
                return False
            else: return True
        else: return False    
    
    def transcricao (self):
        """
        Transcreve uma sequência de DNA para RNA.
        """
        if (self.tipo == "dna"):
            return MySeq(self.seq.replace("T","U"), "rna")
        else:
            return None
        
    def compInverso(self):
        """
        Retorna o complemento inverso de uma sequência de DNA.
        """
        if (self.tipo != "dna"): return None
        comp = ""
        for c in self.seq:
            if (c == 'A'):
                comp = "T" + comp 
            elif (c == "T"): 
                comp = "A" + comp 
            elif (c == "G"): 
                comp = "C" + comp
            elif (c== "C"): 
                comp = "G" + comp
        return MySeq(comp)

    def traduzSeq (self, iniPos= 0):
        """
        Traduz uma sequência de DNA em uma sequência de proteína.
        """
        if (self.tipo != "dna"): return None
        seqM = self.seq
        seqAA = ""
        for pos in range(iniPos,len(seqM)-2,3):
            cod = seqM[pos:pos+3]
            seqAA += self.traduzCodao(cod)
        return MySeq(seqAA, "protein")

    def orfs (self):
        """
        Encontra os ORFs (Open Reading Frames) em uma sequência de DNA.
        """
        if (self.tipo != "dna"): return None
        res = []
        res.append(self.traduzSeq(0))
        res.append(self.traduzSeq(1))
        res.append(self.traduzSeq(2))
        compinv = self.compInverso()
        res.append(compinv.traduzSeq(0))
        res.append(compinv.traduzSeq(1))
        res.append(compinv.traduzSeq(2))    
        return res

    def traduzCodao (self, cod):
        """
        Traduz um codão de DNA em um aminoácido.
        """
        tc = {"GCT":"A", "GCC":"A", "GCA":"A", "GCC":"A", "TGT":"C", "TGC":"C",
      "GAT":"D", "GAC":"D","GAA":"E", "GAG":"E", "TTT":"F", "TTC":"F",
      "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G","CAT":"H", "CAC":"H",
      "ATA":"I", "ATT":"I", "ATC":"I",
      "AAA":"K", "AAG":"K",
      "TTA":"L", "TTG":"L", "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L",
      "ATG":"M", "AAT":"N", "AAC":"N",
      "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P",
      "CAA":"Q", "CAG":"Q",
      "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R", "AGA":"R", "AGG":"R",
      "TCT":"S", "TCC":"S", "TCA":"S", "TCG":"S", "AGT":"S", "AGC":"S",
      "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T",
      "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V",
      "TGG":"W",
      "TAT":"Y", "TAC":"Y",
      "TAA":"_", "TAG":"_", "TGA":"_"}
        if cod in tc:
            aa = tc[cod]
        else: aa = "X" # marca os erros com X
        return aa

    def maiorProteina (self):
        """
        Retorna a maior proteína encontrada em uma sequência de proteínas.
        """
        if (self.tipo != "protein"):
            return None
        seqAA = self.seq
        protAtual = ""
        maiorprot = ""
        for aa in seqAA:
            if aa == "_":
                if len(protAtual) > len(maiorprot):
                    maiorprot = protAtual
                protAtual = ""
            else:
                if len(protAtual) > 0 or aa == "M":
                    protAtual += aa
        return MySeq(maiorprot, "protein")        

    
    def maiorProteinaER (self):
        """
        Retorna a maior proteína encontrada em uma sequência de proteínas usando expressões regulares.
        """
        import re
        if (self.tipo != "protein"): return None
        mos = re.finditer("M[^_]*_", self.seq)
        sizem = 0
        lprot = ""
        for x in mos:
            ini = x.span()[0]
            fin = x.span()[1]
            s = fin - ini + 1
            if s > sizem:
                lprot = x.group()
                sizem = s
        return MySeq(lprot, "protein")    
    
    def todasProteinas(self):
        """
        Retorna uma lista com todas as proteínas encontradas em uma sequência de proteínas.
        """
        if (self.tipo != "protein"):
            return None
        seqAA = self.seq
        protsAtuais = []
        proteinas = []
        for aa in seqAA:
            if aa == "_":
                if protsAtuais:
                    for p in protsAtuais:
                        proteinas.append(MySeq(p, "protein"))
                    protsAtuais = []
            else:
                if aa == "M":
                    protsAtuais.append("")
                for i in range(len(protsAtuais)):
                    protsAtuais[i] += aa

        return proteinas

    
    def maiorProteinaORFs (self):
        """
        Retorna a maior proteína encontrada nas ORFs (Open Reading Frames) de uma sequência de DNA.
        """
        if (self.tipo != "dna"):
            return None
        larg = MySeq("","protein")
        for orf in self.orfs():
            prot = orf.maiorProteinaER()
            if len(prot.seq)>len(larg.seq):
                larg = prot
        return larg



# teste
def teste():
    seq_dna = input("Sequencia:")
    s1 = MySeq(seq_dna)
    s1.printseq()

    if s1.validaER():
        print("Sequencia valida")
        print("Transcricao: ")
        s1.transcricao().printseq()
        print("Complemento inverso:") 
        s1.compInverso().printseq()
        print("Traducao: ") 
        s1.traduzSeq().printseq()
        print("ORFs:")
        for orf in s1.orfs(): orf.printseq()
        print("Maior proteina nas ORFs:")
        s1.maiorProteinaORFs().printseq()  
    else:
        print("Sequencia invalida")

if __name__ == "__main__": 
    teste()