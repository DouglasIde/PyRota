import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean as distancia_euclidiana
from itertools import permutations

def desenhar_rota(rota):
    distancia_percorrida = 0
    tamanho_rota = len(rota)
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

if __name__ == "__main__":
    
    # Definição de origem, destino e pontos intermediários
    origem = (0,0)
    destino = (4,4)
    enderecos = [(2,1), (2,2), (8,3), (5,3)]
    rota = [origem] + enderecos + [destino]

    desenhar_rota(rota)



