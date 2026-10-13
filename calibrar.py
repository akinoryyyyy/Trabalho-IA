# Integrantes:
#   Leonardo Teixeira de Souza - Nº USP 12504602
#   Murilo Amaral              - Nº USP 17074828
#   (adicionar o terceiro integrante, se houver)

import random
from busca import carrega_nos, carrega_arestas, a_estrela, dijkstra, haversine

QTD_ROTAS = 150
PESOS = [1.1, 1.2, 1.25, 1.27, 1.29 , 1.3, 1.4, 1.45, 1.47, 1.5, 1.75, 2.0, 2.5, 3.0]
LIMITE = 0.15          # tolerância do enunciado
MARGEM = 0.10          # só recomendamos pesos com excesso máximo <= 10% (folga de segurança)
FAIXAS_METROS = [(300, 2000), (2000, 6000), (6000, 1e9)]  # curtas, médias, longas
SEMENTE = 7


def sortear_rotas(coords, quantidade):
    """Sorteia pares (origem, destino) misturando rotas curtas, médias e longas."""
    random.seed(SEMENTE)
    nos = list(coords)
    rotas = []
    while len(rotas) < quantidade:
        minimo, maximo = FAIXAS_METROS[len(rotas) % len(FAIXAS_METROS)]
        origem = random.choice(nos)
        for _ in range(300):
            destino = random.choice(nos)
            if minimo <= haversine(coords[origem], coords[destino]) < maximo:
                break
        else:  # nenhuma faixa atendida (mapa pequeno): usa um destino qualquer
            destino = random.choice(nos)
        if destino != origem:
            rotas.append((origem, destino))
    return rotas


def main():
    coords = carrega_nos("nos.csv")
    grafo = carrega_arestas("arestas.csv", coords)
    rotas = sortear_rotas(coords, QTD_ROTAS)

    # ---------- 1) validação do ótimo ----------
    print("== 1) Validação: A* (peso=1.0) vs Dijkstra ==")
    base = []  # (origem, destino, dist_otima, expansoes_A*)
    erros = 0
    sem_rota = 0
    for origem, destino in rotas:
        _, dist_dij, _ = dijkstra(grafo, origem, destino)
        if dist_dij is None:
            sem_rota += 1
            continue
        _, dist_a, exp_a = a_estrela(grafo, coords, origem, destino, 1.0)
        if abs(dist_a - dist_dij) > 1e-6:
            erros += 1
            print(f"  DIVERGIU: {origem} -> {destino}: A*={dist_a:.2f} Dijkstra={dist_dij:.2f}")
        base.append((origem, destino, dist_dij, exp_a))
    print(f"  Rotas testadas: {len(base)} (sem rota: {sem_rota}) | divergências: {erros}")
    print("  RESULTADO:", "ÓTIMO CONFIRMADO" if erros == 0 else "HÁ PROBLEMA NO A*")

    # ---------- 2) calibração do peso ----------
    print("\n== 2) Calibração do peso (A* ponderado) ==")
    print(f"{'peso':>5} | {'excesso máx':>11} | {'excesso médio':>13} | {'economia média exp.':>19} | {'> 15%':>5}")
    recomendado = 1.0
    for peso in PESOS:
        excessos, economias, violacoes = [], [], 0
        for origem, destino, dist_otima, exp_otimo in base:
            _, dist_p, exp_p = a_estrela(grafo, coords, origem, destino, peso)
            excesso = (dist_p - dist_otima) / dist_otima if dist_otima else 0.0
            economia = (exp_otimo - exp_p) / exp_otimo if exp_otimo else 0.0
            excessos.append(excesso)
            economias.append(economia)
            violacoes += excesso > LIMITE
        max_exc = max(excessos)
        print(f"{peso:>5} | {max_exc*100:>10.2f}% | {sum(excessos)/len(excessos)*100:>12.2f}% "
              f"| {sum(economias)/len(economias)*100:>18.2f}% | {violacoes:>5}")
        if max_exc <= MARGEM and violacoes == 0:
            recomendado = peso

    print(f"\nPeso recomendado (maior com excesso máx <= {MARGEM*100:.0f}%): {recomendado}")
    print("Coloque esse valor em PESO_EXPRESSO no main.py.")


if __name__ == "__main__":
    main()
