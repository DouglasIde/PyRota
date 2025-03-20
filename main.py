import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean as distancia_euclidiana
from itertools import permutations
from deap import base, creator, tools, algorithms
import numpy as np

# Desenhar a rota no gráfico
def desenhar_rota(rota):
    distancia_percorrida = 0
    tamanho_rota = len(rota)

    # Iterar sobre todos os pontos da rota
    for i in range(tamanho_rota):
        x,y = rota[i]
        cor = 'black'
        if i == 0:
            cor = 'blue'
        elif i == tamanho_rota - 1:
            cor = 'red'
        else:
            cor = 'green'
        plt.scatter(x,y,color=cor)
        if i < tamanho_rota - 1:
            x1, y1 = rota[i+1]
            dx = x1 - x
            dy = y1 - y
            plt.arrow(x,y,dx,dy,color='black',head_width=0.1)

            distancia_percorrida += distancia_euclidiana(rota[i], rota[i+1])

    plt.title(f"Rota com distância de {round(distancia_percorrida, 2)}")
    plt.show()

# Calcula a distância total de uma rota
def calcular_distancia_rota(rota):
    distancia = 0
    tamanho_rota = len(rota)

    # Itera sobre todos os pontos da rota
    for i in range(tamanho_rota):
        if i < tamanho_rota - 1:
            distancia += distancia_euclidiana(rota[i], rota[i+1])
        return distancia

# Força Bruta para calcular a menor rota
def forca_bruta(origem, destino, enderecos):
    # Variavel com um valor infinito
    menor_distancia = float('inf')
    menor_rota = None

    # Gera todas as permutações possíveis dos endereços
    for permutacao in permutations(enderecos):
        rota = [origem] + enderecos + [destino]

        # Calculando a distancia total da rota
        distancia_rota = calcular_distancia_rota(rota)

        # Verificando se a rota atual é menor do que a menor_distancia encontrada
        if distancia_rota < menor_distancia:
            menor_distancia = distancia_rota
            menor_rota = rota

        return menor_rota, menor_distancia

def vizinho_mais_proximo(origem, destino, endereco):
    ponto_atual = origem
    enderecos_restantes = enderecos.copy()
    distancia_percorrida = 0
    menor_rota = [ponto_atual]

    # Enquanto houverem endereços restantes
    while enderecos_restantes:
        menor_distancia = float('inf')
        ponto_mais_proximo = None

        # Verifica a distância entre o ponto atual e os endereços restantes
        for endereco in enderecos_restantes:
            distancia = distancia_euclidiana(ponto_atual, endereco)
            if distancia < menor_distancia:
                menor_distancia = distancia
                ponto_mais_proximo = endereco

        # Remover este ponto da lista de endereços
        enderecos_restantes.remove(ponto_mais_proximo)

        # Adicionar esse ponto na menor_rota
        menor_rota.append(ponto_mais_proximo)

        # Atualizar a distancia_percorrida
        distancia_percorrida += distancia_percorrida + menor_distancia

        # Atualizar o ponto atual
        ponto_atual = ponto_mais_proximo

    # Adiciona o destino ao final da rota
    menor_rota.append(destino)

    # Calcula a distância final até o destino
    distancia_percorrida = distancia_percorrida + distancia_euclidiana(ponto_atual, destino)
    return menor_rota, distancia_percorrida

# Calcula a distancia total de uma rota gerada a partir de um indivíduo
def avaliar(individuo, origem, enderecos, destino):
    rota = [origem]

    # Para cada gene do individuo (representação da rota)
    for i in individuo:
        rota.append(enderecos[i])
    rota.append(destino)
    distancia_percorrida = calcular_distancia_rota(rota)

    return distancia_percorrida

# Resolver o problema de otimização de rotas
def algoritmo_generico(origem, destino, enderecos, tamanho_populacao_inicial=100,
                       prob_cruzamento=0.7, prob_mutacao=0.1, numero_geracoes=100):

    # Distancia total da rota minimizado
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

    # Lista de Genes com o atributo fitness
    creator.create("Individuo", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Permutação aleatória dos índices dos endereços
    toolbox.register("Genes", np.random.permutation, len(enderecos))
    toolbox.register("Individuos", tools.initIterate, creator.Individuo, toolbox.Genes)

    # Cria a população de indivíduos
    toolbox.register("Populacao", tools.initRepeat, list, toolbox.Individuos)

    # Gera a população inicial de individuos (rotas aleatórias)
    populacao = toolbox.Populacao(n=tamanho_populacao_inicial)

    toolbox.register("mate", tools.cxPartialyMatched)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=prob_mutacao)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", avaliar, origem=origem, enderecos=enderecos, destino=destino)

    algoritmo = algorithms.eaSimple(populacao,
                                    toolbox,
                                    cxpb=prob_cruzamento,
                                    mutpb=prob_cruzamento,
                                    ngen=numero_geracoes,
                                    verbose=False)

    # Seleciona o melhor individuo da população que é a com a menor distancia
    melhor_ind = tools.selBest(populacao, 1)[0]

    # Reconstrói a sequencia de endereços da rota
    menor_rota = [origem]
    for i in melhor_ind:
        menor_rota.append(enderecos[i])
    menor_rota.append(destino)

    # Calcula a distancia da melhor rota
    distancia_percorrida = calcular_distancia_rota(menor_rota)
    return menor_rota, distancia_percorrida

if __name__ == "__main__":
    
    # Definição de origem, destino e pontos intermediários
    origem = (0,0)
    destino = (4,4)
    enderecos = [(2,2), (2,1), (5,3), (8,3), (10,5), (9,4), (8,7), (6,3), (9,6), (7,5)]

    # menor_rota, menor_distancia = forca_bruta(origem, destino, enderecos)
    menor_rota, menor_distancia = vizinho_mais_proximo(origem, destino, enderecos)


    # Após ter encontrado a menor rota, verifica se uma rota foi encontrada e desenha-a
    if menor_rota is None:
        print("Nenhuma rota foi encontrada")
    else:
        print(menor_rota, menor_distancia)
        desenhar_rota(menor_rota)



