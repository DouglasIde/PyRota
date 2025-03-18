import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean as distancia_euclidiana


class RotaManager:

    def __init__(self, rota):
        self.rota = rota

    def desenhar_rota(self):
            tamanho_rota = len(self.rota)
            distancia_percorrida = 0

            for i in range(tamanho_rota):
                x,y = self.rota[i]
                cor = 'black'
                if i == 0:
                    cor = 'blue'
                elif i == tamanho_rota - 1:
                    cor = 'red'
                else:
                    cor = 'green'
                plt.scatter(x,y,color=cor)
                if i < tamanho_rota - 1:
                    x1, y1 = self.rota[i+1]
                    dx = x1 - x
                    dy = y1 - y
                    plt.arrow(x,y,dx,dy,color='black', head_width=0.1)

                    distancia_percorrida = distancia_percorrida + distancia_euclidiana(self.rota[i], self.rota[i+1])

                plt.title(f"Rota com distancia de {round(distancia_percorrida, 2)}")
                plt.show()

    def calcular_distancia_rota(self):
        distancia = 0
        tamanho_rota = len(self.rota)
        for i in range(tamanho_rota):
            if i < tamanho_rota - 1:
                distancia = distancia + distancia_euclidiana(self.rota[i], self.rota[i+1])
            return distancia