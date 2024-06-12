"""
author: miguelrocha
"""

from typing import Union, List, Dict  # Importa tipos de dados da biblioteca typing para uso nas anotações de tipo
import graphviz  # Importa a biblioteca graphviz para visualização de grafos
import pandas as pd  # Importa a biblioteca pandas para manipulação de dados

class GrafoDirigido:  # Define uma classe para representar um grafo dirigido
    def __init__(self, estrutura_grafo: Dict[str, List[str]] = None):  # Inicializa o grafo dirigido com uma estrutura opcional
        # Define a estrutura do grafo, usando um dicionário fornecido ou um dicionário vazio
        self.estrutura = estrutura_grafo if estrutura_grafo is not None else {}
    def adicionar_no(self, no: Union[str, int]) -> None: #Adiciona um nó ao grafo.
        # Verifica se o nó não é uma string
        if not isinstance(no, str):
            # Verifica se o nó é uma lista 
            if isinstance(no, list):
                raise TypeError('O nó deve ser uma string ou um número.')
            # Converte o nó para string
            no = str(no)
        # Adiciona o nó à estrutura do grafo se ele não existir
        self.estrutura.setdefault(no, [])

    def adicionar_arestas(self, arestas: Union[str, List[str]]) -> None: #Adiciona arestas ao grafo.
        # Converte arestas para uma lista se for uma string
        if isinstance(arestas, str):
            arestas = [arestas]
        # Itera sobre cada aresta na lista
        for aresta in arestas:
            # Remove espaços em branco e divide a aresta em origem e destinos
            aresta = aresta.replace(' ', '')
            origem, destinos = aresta.split('->')
            # Adiciona o nó de origem se ele não existir
            self.adicionar_no(origem)
            # Itera sobre cada destino na lista de destinos
            for destino in destinos.split(','):
                # Verifica se o destino não está vazio e não está na lista de adjacência da origem
                if destino.strip() and destino not in self.estrutura[origem]:
                    # Adiciona o nó de destino se ele não existir
                    self.adicionar_no(destino)
                    # Adiciona o destino à lista de adjacência da origem
                    self.estrutura[origem].append(destino)

    def mostrar(self, txt: bool = False, gviz: bool = True) -> graphviz.Digraph: #Exibe o grafo.
        # Se txt for True, imprime a estrutura do grafo
        if txt:
            # Itera sobre cada chave e valor no dicionário da estrutura do grafo
            for chave, valor in self.estrutura.items():
                # Imprime a chave e a lista de adjacência correspondente
                print(f'{chave} ==> {valor}')
        # Se gviz for True, exibe o grafo usando Graphviz
        if gviz:
            # Retorna o objeto Graphviz gerado pelo método auxiliar _exibir
            return self._exibir()

    def _exibir(self) -> graphviz.Digraph: #exibir o grafo usando Graphviz
        # Cria um novo objeto Graphviz
        dot = graphviz.Digraph()
        # Itera sobre cada chave (nó) e valor (lista de adjacência) no dicionário da estrutura do grafo
        for chave, valor in self.estrutura.items():
            # Adiciona o nó ao gráfico
            dot.node(str(chave))
            # Itera sobre cada nó de destino na lista de adjacência
            for dest in valor:
                # Adiciona uma aresta entre a origem (chave) e o destino
                dot.edge(str(chave), str(dest))
        # Retorna o objeto Graphviz
        return dot

    def remover_no(self, no: Union[str, int]) -> None: # Remove um nó do grafo
        # Verifica se o nó existe no grafo
        if no in self.estrutura:
            # Itera sobre cada lista de adjacência no grafo
            for aresta in self.estrutura.values():
                # Remove o nó da lista de adjacência se estiver presente
                if no in aresta:
                    aresta.remove(no)
            # Remove o nó do grafo
            del self.estrutura[no]
        else:
            # Informa que o nó não existe
            print('O nó não existe.')

    def remover_arestas(self, arestas: Union[str, List[str]]) -> None: #Remove arestas do grafo.
        # Converte arestas para uma lista se for uma string
        if isinstance(arestas, str):
            arestas = [arestas]
        # Itera sobre cada aresta na lista
        for aresta in arestas:
            # Remove espaços em branco e divide a aresta em origem e destinos
            aresta = aresta.replace(' ', '')
            origem, destinos = aresta.split('->')
            # Itera sobre cada destino na lista de destinos
            for destino in destinos.split(','):
                # Verifica se o destino está na lista de adjacência da origem e o remove
                if destino in self.estrutura[origem]:
                    self.estrutura[origem].remove(destino)

   
    def obter_sucessores(self, no: str) -> List[str]: #Obtém os sucessores de um nó.
        # Retorna a lista de sucessores do nó, ou uma lista vazia se o nó não existir
        return self.estrutura.get(no, [])

    def obter_predecessores(self, no: str) -> List[str]: #Obtém os predecessores de um nó.
        # Inicializa a lista de predecessores
        predecessores = []
        # Itera sobre cada chave (nó) e valor (lista de adjacência) no dicionário da estrutura do grafo
        for chave, valor in self.estrutura.items():
            # Se o nó está na lista de adjacência de outro nó
            if no in valor:
                # Adiciona o nó à lista de predecessores
                predecessores.append(chave)
        # Retorna a lista de predecessores
        return predecessores

    def obter_adjacentes(self, no: str) -> List[str]: #Obtém os nós adjacentes de um dado nó.
        # Obtém os predecessores e sucessores do nó
        predecessores = self.obter_predecessores(no)
        sucessores = self.obter_sucessores(no)
        # Retorna a lista de nós adjacentes (predecessores e sucessores) sem duplicatas
        return sorted(set(predecessores + sucessores))

    def matriz_adjacencia(self) -> pd.DataFrame: #Gera a matriz de adjacência do grafo.
        # Ordena os nós
        nos = sorted(self.estrutura.keys())
        # Cria a matriz de adjacência
        matriz = [[1 if dest in self.estrutura[no] else 0 for dest in nos] for no in nos]
        # Retorna a matriz como um DataFrame do pandas
        return pd.DataFrame(matriz, index=nos, columns=nos)

    

    def busca_em_largura(self, no): #Realiza uma travessia em largura (BFS) no grafo começando de um determinado nó.
        visitados = []  # Lista para rastrear os nós visitados
        fila = []  # Fila para gerenciar a ordem de visitação dos nós
        fila.append(no)  # Adiciona o nó inicial à fila

        while fila:  # Enquanto houver nós na fila
            atual = fila.pop(0)  # Remove o primeiro nó da fila
            if atual not in visitados:  # Se o nó não foi visitado ainda
                visitados.append(atual)  # Marca o nó como visitado
                fila.extend(self.obter_sucessores(atual))  # Adiciona os sucessores do nó à fila

        return visitados  # Retorna a lista de nós visitados