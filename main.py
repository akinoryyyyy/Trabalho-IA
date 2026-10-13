# Integrantes:
#   Leonardo Teixeira de Souza - Nº USP 12504602
#   Murilo Amaral              - Nº USP 17074828

from verRota import plotar_rotas
from busca import carrega_nos, carrega_arestas, a_estrela

ARQUIVO_NOS = "nos.csv"
ARQUIVO_ARESTAS = "arestas.csv"
PESO_EXPRESSO = 1.25  
SEPARADOR = "# " + "-" * 42


def imprimir_resultado(titulo, algoritmo, origem, destino, caminho, distancia,
                       expandidos, referencia=None):
    """Imprime no template do enunciado.

    referencia = (distancia_otima, expandidos_otimo): quando informada,
    mostra as porcentagens em relação ao Desafio 1.
    """
    print(SEPARADOR)
    print(f"# RESULTADO DA BUSCA - {titulo}")
    print(SEPARADOR)
    print(f"# Algoritmo utilizado: {algoritmo}")
    print(f"# Origem (osmid): {origem}")
    print(f"# Destino (osmid): {destino}")
    print(SEPARADOR)
    print(f"# Caminho encontrado (Qtd nós): {len(caminho)} cruzamentos")
    if referencia:
        dist_otima, exp_otimo = referencia
        pct_dist = (distancia - dist_otima) / dist_otima * 100 if dist_otima else 0.0
        pct_exp = (expandidos - exp_otimo) / exp_otimo * 100 if exp_otimo else 0.0
        print(f"# Distância da Rota: {distancia:.2f} metros ({pct_dist:+.2f}%)")
        print(f"# NÓS EXPANDIDOS: {expandidos} ({pct_exp:+.2f}%)")
    else:
        print(f"# Distância da Rota: {distancia:.2f} metros")
        print(f"# NÓS EXPANDIDOS: {expandidos}")
    print(SEPARADOR)


def ler_osmid(mensagem):
    """Lê um osmid inteiro do teclado; devolve None se a entrada for inválida."""
    try:
        return int(input(mensagem).strip())
    except ValueError:
        return None


def executar_desafios(grafo, coords, origem, destino):
    """Roda Desafio 1 (ótimo) e Desafio 2 (expresso). Devolve os dois caminhos."""
    caminho1, dist1, exp1 = a_estrela(grafo, coords, origem, destino, peso=1.0)
    if caminho1 is None:
        print("Não existe rota entre a origem e o destino informados.")
        return None, None
    imprimir_resultado("DESAFIO 1 (ROTA ÓTIMA)", "A* (heurística haversine)",
                       origem, destino, caminho1, dist1, exp1)

    caminho2, dist2, exp2 = a_estrela(grafo, coords, origem, destino, peso=PESO_EXPRESSO)
    imprimir_resultado("DESAFIO 2 (ROTA EXPRESSA)", f"A* ponderado (w={PESO_EXPRESSO})",
                       origem, destino, caminho2, dist2, exp2,
                       referencia=(dist1, exp1))

    if dist1 and (dist2 - dist1) / dist1 > 0.15:
        print("AVISO: a rota expressa passou de +15% da ótima. Reduza PESO_EXPRESSO.")

    return caminho1, caminho2


def main():
    try:
        coords = carrega_nos(ARQUIVO_NOS)
        grafo = carrega_arestas(ARQUIVO_ARESTAS, coords)
    except FileNotFoundError as erro:
        print(f"Arquivo não encontrado: {erro.filename}. Coloque os CSVs na mesma pasta.")
        return

    origem = ler_osmid("Origem (osmid): ")
    destino = ler_osmid("Destino (osmid): ")
    if origem is None or destino is None:
        print("Digite apenas números inteiros (osmid).")
        return
    if origem not in coords or destino not in coords:
        print("Origem ou destino não existe no mapa.")
        return

    caminho1, caminho2 = executar_desafios(grafo, coords, origem, destino)

    if caminho1:
        plotar_rotas(coords, caminho1, caminho2)


if __name__ == "__main__":
    main()
