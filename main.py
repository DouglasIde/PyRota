import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean as distancia_euclidiana
from itertools import permutations


if __name__ == "__main__":
    

    origem = (0,0)
    destino = (4,4)
    enderecos = [(2,1), (2,2), (8,3), (5,3)]

    rota = [origem] + enderecos + [destino]

    print(rota)