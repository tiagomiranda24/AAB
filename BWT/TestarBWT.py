import unittest
from BWT import BWT

seqs_para_bwts = {'' : '', 
             '$' : '$', 
             'TAGACAGAGA$' : 'AGGGTCAAAA$',
             'TAGACAGAGA' : 'AGGGTCAAAA$',
             'TAGACAGAGA$$' : 'A$GGGTCAAAA$',
             'ACTAGAGACA$' : 'ACG$GTAAAAC',
             'banana$' : 'annb$aa',
             'BANANA$' : 'ANNB$AA',
             'Banana$' : 'a$nnBaa',
             'a' : 'a$'
             }

bwts_para_seqs = {'' : '', 
             '$' : '$',
             'AGGGTCAAAA$' : 'TAGACAGAGA$',
             'A$GGGTCAAAA$' : '$TAGACAGAGA$',
             'ACG$GTAAAAC' : 'ACTAGAGACA$',
             'annb$aa' : 'banana$',
             'ANNB$AA' : 'BANANA$',
             'a$nnBaa' : 'Banana$',
             'a$' : 'a$'
             }

exemplos_padroes = [
    ('', 'AGA', []),
    ('$', 'AGA', []),
    ('AAA$', 'AGA', []),
    ('TAGACAGAGA$', 'AGA', [3, 4, 5]),
    ('ACTAGAGACA$', 'AGA', [4, 5])
    ]

exemplos_padroes_sa = [
    ('', 'AGA', []),
    ('$', 'AGA', []),
    ('AAA$', 'AGA', []),
    ('TAGACAGAGA$', 'AGA', [1, 5, 7]),
    ('ACTAGAGACA$', 'AGA', [3, 5])
    ]

class TestarBWT(unittest.TestCase):
    def testar_constr_bwt(self):
        for seq_teste, bwt_teste in seqs_para_bwts.items():
            bwt = BWT(seq_teste)
            self.assertEqual(bwt.bwt, bwt_teste)

    def testar_inverso_bwt(self):
        for bwt_teste, seq_teste in bwts_para_seqs.items():
            bwt = BWT('')
            bwt.definir_bwt(bwt_teste)
            self.assertEqual(bwt.inverso_bwt(), seq_teste)

    def testar_proc_padroes(self):
        for exemplo in exemplos_padroes:
            seq, padrao, indices = exemplo
        bwt = BWT(seq)
        bwt.bwt
        self.assertEqual(bwt.proc_padroes(padrao), indices)

    def testar_proc_padroes_sa(self):
        for exemplo in exemplos_padroes_sa:
            seq, padrao, indices = exemplo
        bwt = BWT(seq)
        bwt.bwt
        self.assertEqual(bwt.proc_padroes_sa(padrao), indices)

if __name__ == '__main__':
    unittest.main()