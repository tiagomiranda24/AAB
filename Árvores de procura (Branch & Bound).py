#!/usr/bin/env python
# coding: utf-8

# Método de busca exaustiva

# In[1]:


def proxima(seqs: list[str], L: int, s: list[int]) -> list[int]:
    # Verificamos se todas as sequências têm o mesmo tamanho
    assert all(len(seq) == len(seqs[0]) for seq in seqs), "as sequências não têm todas o mesmo tamanho"
    
    tam_seq = len(seqs[0])
    offset_max = tam_seq - L
    nova = s.copy()  # Utilizamos o 'copy()' para evitar referências indesejadas
    idx = -1
    continua = True 

    while continua: 
        continua = False
        assert (nova[idx] <= offset_max)
        nova[idx] += 1

        if nova[idx] > offset_max:
            nova[idx] = 0
            idx -= 1
            continua = True

        if abs(idx) >= tam_seq:
            continua = False
    
    return nova

# Inicializa a lista 'off' com zeros
off = [0] * 5

while True: 
    off = proxima("AAAAAA AAAAAA AAAAAA AAAAAA AAAAAA".split(), 3, off)
    print(off)

    # Verifica se a soma da lista 'off' é zero para encerrar o loop
    if sum(off) == 0:
        break


# Enumeração exaustiva

# In[2]:


# Função para encontrar motivos em sequências de ADN
def encontrar_motivo(posicoes_anteriores: list[int], sequencias: list[str], comprimento_motivo: int):
    # Número total de sequências
    num_sequencias = len(sequencias)
    
    # Comprimento de cada sequência
    comprimento_sequencia = len(sequencias[0])
    
    # Se todas as posições já foram escolhidas, imprimir e retornar
    if len(posicoes_anteriores) == num_sequencias:
        print(posicoes_anteriores)
        return
    
    # Iterar sobre todas as posições possíveis para o início do motivo
    for posicao_inicial in range(comprimento_sequencia - comprimento_motivo + 1):
        # Chamada recursiva para encontrar motivos nas sequências restantes
        encontrar_motivo(posicoes_anteriores + [posicao_inicial], sequencias, comprimento_motivo)

# Exemplo de utilização da função com sequências de ADN e comprimento do motivo 3
encontrar_motivo([], "AAAAAA AAAAAA AAAAAA AAAAAA AAAAAA".split(), 3)


# Árvores de procura (Branch & Bound)

# In[3]:


import random  # Importa o módulo random para gerar sequências aleatórias

debug = False  # Variável de controle para imprimir informações de depuração

def score_so_far(offsets: list[int], seqs: list[str], L: int) -> int:
    # Calcula a pontuação atual com base nos offsets fornecidos
    snips = [seqs[i][p : p + L] for i, p in enumerate(offsets)]
    if debug: print(snips, end=" ")  # Imprime os trechos (snippets) se debug estiver ativado
    return sum(max({x: s.count(x) for x in "ACGT"}.values()) for s in zip(*snips))

print(score_so_far([0, 0], "ACGT ACGT ACGT".split(), 2))  # Exemplo de uso da função

def max_possible_score(offsets: list[int], seqs: list[str], L: int) -> int:
    # Calcula a pontuação máxima possível considerando os offsets fornecidos
    current_score = score_so_far(offsets, seqs, L)
    remaining_seqs = len(seqs) - len(offsets)
    if debug: print(offsets, current_score, remaining_seqs)  # Imprime informações de depuração se debug estiver ativado
    return current_score + L * remaining_seqs

def motif(offsets_so_far: list[int], seqs: list[str], L: int, best_score_so_far: int) -> tuple[list[int], int]:
    prune = True  # Variável de controle para poda (pruning)
    t = len(seqs[0])
    best_offsets = []
    
    # Verifica se todos os offsets foram escolhidos
    if len(offsets_so_far) == len(seqs):
        current_score = max_possible_score(offsets_so_far, seqs, L)
        # Retorna os offsets e a pontuação se a pontuação for maior que a melhor pontuação até agora
        if current_score > best_score_so_far:
            return offsets_so_far, current_score
        else:
            return [], -1
    
    # Poda: Se a pontuação máxima possível for menor ou igual à melhor pontuação até agora, interrompe a busca
    if prune and max_possible_score(offsets_so_far, seqs, L) <= best_score_so_far:
        return [], -1
    
    # Loop sobre os offsets possíveis
    for i in range(t - L + 1):
        new_offsets, current_score = motif(offsets_so_far + [i], seqs, L, best_score_so_far)
        # Atualiza os melhores offsets e a melhor pontuação se a pontuação for maior que a melhor pontuação até agora
        if current_score > best_score_so_far:
            best_offsets = new_offsets
            best_score_so_far = current_score
    
    return best_offsets, best_score_so_far

# Geração de sequências aleatórias para teste
seqs = [random.choices("ACGT", k=1000) for _ in range(20)]
# Chama a função motif com parâmetros iniciais
motif([], seqs, 3, -1)

