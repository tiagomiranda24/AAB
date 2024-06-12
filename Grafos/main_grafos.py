from grafo import GrafoDirigido

def main():
    # Cria um grafo dirigido vazio
    grafo = GrafoDirigido()

    # Adiciona nós ao grafo
    grafo.adicionar_no('A')
    grafo.adicionar_no('B')
    grafo.adicionar_no('C')
    grafo.adicionar_no('D')
    grafo.adicionar_no('E')

    # Adiciona arestas ao grafo
    grafo.adicionar_arestas(['A->B,C', 'B->D', 'C->E', 'D->E'])

    # Exibe o grafo
    grafo.mostrar(txt=True, gviz=True)

    # Remove um nó do grafo
    grafo.remover_no('B')

    # Exibe o grafo novamente
    grafo.mostrar(txt=True, gviz=True)

    # Obtém os sucessores de um nó
    print("Sucessores de A:", grafo.obter_sucessores('A'))

    # Obtém os predecessores de um nó
    print("Predecessores de E:", grafo.obter_predecessores('E'))

    # Obtém os nós adjacentes de um nó
    print("Adjacentes de C:", grafo.obter_adjacentes('C'))

    # Gera a matriz de adjacência do grafo
    print("Matriz de adjacência:")
    print(grafo.matriz_adjacencia())

    # Realiza uma travessia em largura (BFS) no grafo
    print("Travessia em largura a partir de A:", grafo.busca_em_largura('A'))

if __name__ == "__main__":
    main()