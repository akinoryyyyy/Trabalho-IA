# Integrantes:
#   Leonardo Teixeira de Souza - Nº USP 12504602
#   Murilo Amaral              - Nº USP 17074828

import csv
import math
import heapq


def carrega_nos(caminho):
    """Lê nos.csv e devolve {osmid: (latitude, longitude)}."""
    coords = {}
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            osmid = int(linha["osmid"])
            coords[osmid] = (float(linha["latitude"]), float(linha["longitude"]))
    return coords


def carrega_arestas(caminho, coords):
    """Lê arestas.csv e devolve o grafo como {no: {vizinho: distancia}}.

    O grafo é não orientado: cada aresta é inserida nos dois sentidos.
    Se houver arestas repetidas entre o mesmo par, fica a de menor distância.
    Arestas que citam nós ausentes em nos.csv são ignoradas.
    """
    grafo = {osmid: {} for osmid in coords}
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            origem = int(linha["origem"])
            destino = int(linha["destino"])
            distancia = float(linha["distancia"])

            if origem not in grafo or destino not in grafo:
                continue

            # roda duas vezes, trocando origem e destino (grafo não orientado)
            for no_a, no_b in ((origem, destino), (destino, origem)):
                if distancia < grafo[no_a].get(no_b, float("inf")):
                    grafo[no_a][no_b] = distancia
    return grafo


def haversine(coord_a, coord_b):
    """Distância em linha reta (metros) entre dois pontos (lat, lon em graus).

    Usada como heurística h(n) do A*:
    - Admissível: a linha reta nunca é maior que qualquer caminho real pelas ruas.
    - Consistente: obedece à desigualdade triangular, então um nó fechado
      nunca precisa ser reaberto.
    """
    raio_terra = 6371000  # metros
    lat1, lon1 = map(math.radians, coord_a)
    lat2, lon2 = map(math.radians, coord_b)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    termo = (math.sin(delta_lat / 2) ** 2
             + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2)

    return 2 * raio_terra * math.asin(math.sqrt(termo))


def reconstruir_caminho(pais, destino):
    """Segue os 'pais' do destino até a origem e inverte a lista."""
    caminho = [destino]
    while pais[caminho[-1]] is not None:
        caminho.append(pais[caminho[-1]])
    caminho.reverse()
    return caminho


def dijkstra(grafo, origem, destino):
    """Menor caminho sem heurística. Usado só para validar o A*.

    Retorna (caminho, distancia, nos_expandidos) ou (None, None, nos_expandidos).
    """
    fronteira = [(0.0, origem)]  # (custo acumulado g, nó)
    melhor_g = {origem: 0.0}
    pais = {origem: None}
    fechados = set()
    nos_expandidos = 0

    while fronteira:
        custo_atual, atual = heapq.heappop(fronteira)

        if atual in fechados:  # entrada velha do heap: ignora, sem contar
            continue

        if atual == destino:  # só testado, não expandido
            return reconstruir_caminho(pais, destino), custo_atual, nos_expandidos

        fechados.add(atual)
        nos_expandidos += 1  # EXPANSÃO: nó retirado da fronteira e processado

        for vizinho, distancia in grafo[atual].items():
            novo_g = custo_atual + distancia
            if novo_g < melhor_g.get(vizinho, float("inf")):
                melhor_g[vizinho] = novo_g
                pais[vizinho] = atual
                heapq.heappush(fronteira, (novo_g, vizinho))

    return None, None, nos_expandidos  # fronteira esvaziou: sem rota


def a_estrela(grafo, coords, origem, destino, peso=1.0):
    """A* com f = g + peso * h.

    peso = 1.0  -> A* clássico (ótimo, pois h é admissível).
    peso > 1.0  -> A* ponderado: dá mais importância ao palpite h, expande
                   menos nós, mas pode devolver caminho até ~peso vezes mais
                   longo que o ótimo.

    Retorna (caminho, distancia, nos_expandidos) ou (None, None, nos_expandidos).
    """
    coord_destino = coords[destino]
    cache_h = {}  # evita recalcular haversine para o mesmo nó

    def h(no):
        if no not in cache_h:
            cache_h[no] = haversine(coords[no], coord_destino)
        return cache_h[no]

    # Elementos do heap: (f, -g, nó). O -g desempata: entre f iguais,
    # sai primeiro o de MAIOR g (mais perto do destino).
    fronteira = [(peso * h(origem), 0.0, origem)]
    melhor_g = {origem: 0.0}
    pais = {origem: None}
    fechados = set()
    nos_expandidos = 0

    while fronteira:
        _, menos_g, atual = heapq.heappop(fronteira)
        custo_atual = -menos_g

        if atual in fechados:  # entrada velha do heap: ignora, sem contar
            continue

        if atual == destino:  # só testado, não expandido
            return reconstruir_caminho(pais, destino), custo_atual, nos_expandidos

        fechados.add(atual)
        nos_expandidos += 1  # EXPANSÃO: único ponto de incremento do contador

        for vizinho, distancia in grafo[atual].items():
            novo_g = custo_atual + distancia
            if novo_g < melhor_g.get(vizinho, float("inf")):
                melhor_g[vizinho] = novo_g
                pais[vizinho] = atual
                f = novo_g + peso * h(vizinho)
                heapq.heappush(fronteira, (f, -novo_g, vizinho))

    return None, None, nos_expandidos
