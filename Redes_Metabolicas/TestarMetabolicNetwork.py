"""
unittesting dos métodos 'reacoes_ativas', 'metabolitos_produzidos', 'metabolitos_finais' 
da classe MetabolicNetwork
"""

import unittest
from MetabolicNetwork import MetabolicNetwork

parametros_errados = {
    'metabolite-metabolite' : True,
    'reaction-reaction' : True,
    'metabolite-reaction' : False,
    'metabolite-reaction' : False
}

class TestarMetabolicNetwork(unittest.TestCase):
    # testar inserir parâmetros errados na classe
    def testar_reacoes_ativas_param_errados(self):
        for net_type, split_rev in parametros_errados.items():
            mrsn = MetabolicNetwork(net_type, split_rev)
            mrsn.load_from_file('example-net.txt')
            self.assertEqual(mrsn.reacoes_ativas(['M1','M2']), None)

    def testar_metabolitos_produzidos_param_errados(self):
        for net_type, split_rev in parametros_errados.items():
            mrsn = MetabolicNetwork(net_type, split_rev)
            mrsn.load_from_file('example-net.txt')
            self.assertEqual(mrsn.metabolitos_produzidos(['R1']), None)

    # testar reacoes_ativas
    def testar_reacoes_ativas_example1(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.reacoes_ativas(['M1','M2']), ['R1'])

    def testar_reacoes_ativas_example2(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.reacoes_ativas(['M4','M6']), ['R2', 'R3_b'])

    def testar_reacoes_ativas_example3(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.reacoes_ativas(['M4','M5','M6']), ['R2', 'R3', 'R3_b'])
    
    # testar metabolitos_produzidos
    def testar_metabolitos_produzidos_example1(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.metabolitos_produzidos(['R1']), ['M3', 'M4'])

    def testar_metabolitos_produzidos_example2(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.metabolitos_produzidos(['R2']), ['M3'])

    def testar_metabolitos_produzidos_example3(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.metabolitos_produzidos(['R3']), ['M6'])

    # testar metabolitos_finais
    def testar_metabolitos_finais_example1(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.metabolitos_finais(['M1','M2']), ['M1', 'M2', 'M3', 'M4'])

    def testar_metabolitos_finais_example2(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.metabolitos_finais(['M1','M2','M6']), ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'])

    def testar_metabolitos_finais_example3(self):
        mrsn = MetabolicNetwork('metabolite-reaction', True)
        mrsn.load_from_file('example-net.txt')
        self.assertEqual(mrsn.metabolitos_finais(['M1', 'M2', 'M3', 'M4', 'M5', 'M6']), ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'])

if __name__ == '__main__':
    unittest.main()