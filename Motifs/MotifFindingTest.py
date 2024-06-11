import unittest
from MotifFinding import MotifFinding 
from MySeq import MySeq  

class MotifFinding_test(unittest.TestCase):

    def setUp(self):
        self.seq1 = MySeq("ATAGAGCTGA", "dna")
        self.seq2 = MySeq("ACGTAGATGA", "dna")
        self.seq3 = MySeq("AAGATAGGGG", "dna")

    def test_exhaustiveSearch(self):
        # Cria uma instância de MotifFinding com um comprimento de motif 3 e as sequências definidas anteriormente
        mf = MotifFinding(3, [self.seq1, self.seq2, self.seq3])
        # Realiza a pesquisa exaustiva para encontrar os melhores motifs
        x = mf.exhaustiveSearch()
        # Verifica se o resultado é igual a [1, 3, 4]
        self.assertEqual(str(x), "[1, 3, 4]")

    def test_score(self):
        mf = MotifFinding(3, [self.seq1, self.seq2, self.seq3])
        # Define a solução esperada
        sol = [1, 3, 4]
        # Calcula o score da solução
        x = mf.score(sol)
        # Verifica se o score calculado é igual a 9
        self.assertEqual(str(x), "9")

    def test_consensus(self):
        mf = MotifFinding(3, [self.seq1, self.seq2, self.seq3])
        sol = [1, 3, 4]
        # Cria um motif a partir dos índices fornecidos e calcula o consenso
        x = mf.createMotifFromIndexes(sol).consensus()
        # Verifica se o consenso calculado é igual a "TAG"
        self.assertEqual(str(x), "TAG")

    def test_heuristicConsensus(self):
        mf = MotifFinding(3, [self.seq1, self.seq2, self.seq3])
        # Executa a função para encontrar um consenso
        sol = mf.heuristicConsensus()
        x = mf.score(sol)
        # Verifica se o score calculado é igual a 9
        self.assertEqual(str(x), "9")

if __name__ == '__main__':
    unittest.main()