"""
Script para implementação das Redes Metabólicas na classe MetabolicNetwork 
onde foram implementados de raíz os métodos:
- reacoes_ativas
- metabolitos_produzidos
- metabolitos_finais
O restante código da classe é da autoria do professor Miguel Rocha
"""

from MyGraph import MyGraph

class MetabolicNetwork(MyGraph):
    def __init__(self, network_type="metabolite-reaction", split_rev=False):
        MyGraph.__init__( self , {})
        self.net_type = network_type
        self.node_types = {}
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []
            self.node_types["reaction"] = []
        self.split_rev = split_rev

    def add_vertex_type(self, v, nodetype):
        self.add_vertex(v)
        self.node_types[nodetype].append(v)

    def get_nodes_type(self, node_type):
        if node_type in self.node_types:
            return self.node_types[node_type]
        else: return None

    def load_from_file(self, filename):
        with open(filename) as rf:
            gmr = MetabolicNetwork("metabolite-reaction")
            for line in rf:
                if ":" in line:
                    tokens = line.split(":")
                    reac_id = tokens[0].strip()
                    gmr.add_vertex_type(reac_id, "reaction")
                    rline = tokens[1]
                else: raise Exception("Invalid line:")
                if "<=>" in rline:
                    left, right = rline.split("<=>")
                    mets_left = left.split("+")
                    for met in mets_left:
                        met_id = met.strip()
                        if met_id not in gmr.graph:
                            gmr.add_vertex_type(met_id, "metabolite")
                        if self.split_rev:
                            gmr.add_vertex_type(reac_id + "_b", "reaction")
                            gmr.add_edge(met_id, reac_id)
                            gmr.add_edge(reac_id + "_b", met_id)
                        else:
                            gmr.add_edge(met_id, reac_id)
                            gmr.add_edge(reac_id, met_id)
                    mets_right = right.split("+")
                    for met in mets_right:
                        met_id = met.strip()
                        if met_id not in gmr.graph:
                            gmr.add_vertex_type(met_id, "metabolite")
                        if self.split_rev:
                            gmr.add_edge(met_id, reac_id + "_b")
                            gmr.add_edge(reac_id, met_id)
                        else:
                            gmr.add_edge(met_id, reac_id)
                            gmr.add_edge(reac_id, met_id)
                elif "=>" in rline:
                    left, right = rline.split("=>")
                    mets_left = left.split("+")
                    for met in mets_left:
                        met_id = met.strip()
                        if met_id not in gmr.graph:
                            gmr.add_vertex_type(met_id, "metabolite")
                        gmr.add_edge(met_id, reac_id)
                    mets_right = right.split("+")
                    for met in mets_right:
                        met_id = met.strip()
                        if met_id not in gmr.graph:
                            gmr.add_vertex_type(met_id, "metabolite")
                        gmr.add_edge(reac_id, met_id)
                else: raise Exception("Invalid line:")

            if self.net_type == "metabolite-reaction":
                self.graph = gmr.graph
                self.node_types = gmr.node_types
            elif self.net_type == "metabolite-metabolite":
                self.convert_metabolite_net(gmr)
            elif self.net_type == "reaction-reaction":
                self.convert_reaction_graph(gmr)
            else: self.graph = {}

    def convert_metabolite_net(self, gmr):
        for m in gmr.node_types["metabolite"]:
            self.add_vertex(m)
            sucs = gmr.get_successors(m)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if m != s2:
                        self.add_edge(m, s2)

    def convert_reaction_graph(self, gmr):
        for r in gmr.node_types["reaction"]:
            self.add_vertex(r)
            sucs = gmr.get_successors(r)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if r != s2:
                        self.add_edge(r, s2)

    def reacoes_ativas(self, metabolitos : list[str]) -> list[str]:
        """
        Descrição: Determina todas as reações ativas dado uma lista de metabolitos existentes
        Parâmetros:
            metabolitos (list[str]): Lista de metabolitos existentes
        Retorna:
            (list[str]): Lista ordenada com todas as reações ativas dado uma lista de 
            metabolitos existentes
        """
        if self.net_type != "metabolite-reaction" or not self.split_rev:
            return None
        reacoes_ativas = []
        for reacao in self.node_types["reaction"]:
            substratos = [node for node in self.get_predecessors(reacao) if node in self.node_types["metabolite"]]
            if all(substrato in metabolitos for substrato in substratos):
                reacoes_ativas.append(reacao)
        reacoes_ativas = set(reacoes_ativas)
        return sorted(list(reacoes_ativas))

    def metabolitos_produzidos(self, reacoes : list[str]) -> list[str]:
        """
        Descrição: Determina todos os metabolitos que podem ser produzidos dada uma lista de reações ativas 
        Parâmetros:
            reacoes (list[str]): Lista de reações ativas
        Retorna:
            (list[str]): Lista ordenada com todos os metabolitos que podem ser produzidos 
            dada uma lista de reações ativas
        """
        if self.net_type != "metabolite-reaction" or not self.split_rev:
            return None
        metabolitos_produzidos = set()
        for reacao in reacoes:
            produtos = [node for node in self.get_successors(reacao) if node in self.node_types["metabolite"]]
            metabolitos_produzidos.update(produtos)
        return sorted(list(metabolitos_produzidos))

    def metabolitos_finais(self, metabolitos_iniciais : list[str]) -> list[str]:
        """
        Descrição: Calcula todos os metabolitos “finais” que poderão ser produzidos, 
                   dada uma lista de metabolitos iniciais
        Parâmetros:
            metabolitos_iniciais (list[str]): Lista de metabolitos iniciais
        Retorna:
            (list[str]): Lista ordenada de todos os metabolitos “finais” que poderão ser produzidos
        """
        metabolitos_atuais = set(metabolitos_iniciais)
        metabolitos_anteriores = set()

        while metabolitos_atuais != metabolitos_anteriores:
            metabolitos_anteriores = metabolitos_atuais.copy()
            reacoes_ativas = self.reacoes_ativas(list(metabolitos_atuais))
            metabolitos_produzidos = self.metabolitos_produzidos(reacoes_ativas)
            metabolitos_atuais.update(metabolitos_produzidos)

        return sorted(list(metabolitos_atuais))