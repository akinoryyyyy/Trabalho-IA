# Roteamento em Ribeirão Preto

Trabalho 1 de Inteligência Artificial (USP, 2º Semestre/2026).

Encontra rotas na malha viária de Ribeirão Preto (dados do OpenStreetMap) com A* e A* ponderado.

Integrantes:
- Leonardo Teixeira de Souza (12504602)
- Murilo Amaral (17074828)

Arquivos:
- busca.py: carrega o grafo, heurística haversine, A* e Dijkstra
- main.py: pede origem e destino, roda os Desafios 1 e 2 e gera o mapa
- verRota.py: gera o mapa rota.html com as duas rotas
- calibrar.py: valida o ótimo contra o Dijkstra e calibra o peso do Desafio 2
- nos.csv e arestas.csv: dados do mapa

Como rodar:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install folium pandas
4. python3 main.py
5. Informe os osmids de origem e destino
6. Abra o rota.html no navegador (azul: Desafio 1, vermelho: Desafio 2)

Desafios:
- Desafio 1: A* com peso 1.0 (rota ótima)
- Desafio 2: A* ponderado com peso 1.25 (menos nós expandidos, até 15% mais longo)
