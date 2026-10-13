# Integrantes:
#   Leonardo Teixeira de Souza - Nº USP 12504602
#   Murilo Amaral              - Nº USP 17074828

import folium


def plotar_rotas(coords, caminho_otimo, caminho_expresso=None, arquivo="rota.html"):
    """Gera um mapa HTML: ótima em azul (Desafio 1), expressa em vermelho (Desafio 2)."""
    pontos_otimo = [coords[no] for no in caminho_otimo]
    mapa = folium.Map(
    location=pontos_otimo[0],
    zoom_start=15,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Street Map",
    )

    folium.PolyLine(pontos_otimo, color="blue", weight=7, opacity=0.8,
                    tooltip="Desafio 1 (ótima)").add_to(mapa)

    if caminho_expresso:
        pontos_expresso = [coords[no] for no in caminho_expresso]
        folium.PolyLine(pontos_expresso, color="red", weight=3, opacity=0.9,
                        tooltip="Desafio 2 (expressa)").add_to(mapa)

    folium.Marker(pontos_otimo[0], tooltip="Origem",
                  icon=folium.Icon(color="green")).add_to(mapa)
    folium.Marker(pontos_otimo[-1], tooltip="Destino",
                  icon=folium.Icon(color="black")).add_to(mapa)

    mapa.fit_bounds(pontos_otimo)
    legenda = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 9999;
                background: white; padding: 10px 14px; border: 2px solid #888;
                border-radius: 6px; font-size: 14px; color: #000;">
        <b>Legenda</b><br>
        <span style="color:blue;">&#9632;</span> Desafio 1 (rota ótima)<br>
        <span style="color:red;">&#9632;</span> Desafio 2 (rota expressa)<br>
        <span style="color:green;">&#9679;</span> Origem &nbsp;
        <span style="color:black;">&#9679;</span> Destino
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(legenda))
    mapa.save(arquivo)
    print(f"Mapa salvo em {arquivo}. Abra no navegador.")