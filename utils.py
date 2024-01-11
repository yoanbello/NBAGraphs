import base64
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests

def get_graph_pts(player_id, player_name, stat, graph):
    url = f'https://www.basketball-reference.com/players/t/{player_id}/gamelog/2024'

    # Lee todas las tablas HTML de la página web
    tablas_html = pd.read_html(url, attrs={"id": "pgl_basic"})

    # Si se encontró la tabla, conviértela a DataFrame
    if tablas_html:
        dataframe = tablas_html[0]  # Seleccionar la primera tabla encontrada

        # Filtra los registros donde 'PTS' no sea nulo y sea un valor numérico
        dataframe_filtrado = dataframe[dataframe[f'{stat}'].notnull()]
        dataframe_filtrado = dataframe_filtrado[dataframe_filtrado[f'{stat}'].apply(lambda x: str(x).isdigit())]

        # Convertir la columna 'PTS' a tipo numérico para ordenar correctamente
        dataframe_filtrado[f'{stat}'] = pd.to_numeric(dataframe_filtrado[f'{stat}'])

        # Filtrar registros que no sean "Inactive" o "Did Not Dress"
        dataframe_filtrado = dataframe_filtrado[~dataframe_filtrado['Opp'].str.contains('Inactive|Did Not Dress')]

        # Ordenar el DataFrame por la columna de fechas
        dataframe_filtrado = dataframe_filtrado.sort_values('Date')

        # Graficar los puntos en función de la fecha usando un gráfico de barras
        plt.figure(figsize=(10, 8))  # Tamaño del gráfico
        if graph=="bar":
            bars = plt.bar(dataframe_filtrado['Date'], dataframe_filtrado[f'{stat}'], width=0.8,
                           color="#23D160")  # Gráfico de barras horizontal
            plt.title(f'{stat} by games - {player_name}')  # Título del gráfico
            plt.xlabel('Fecha')
            plt.ylabel(f'{stat}')  # Etiqueta del eje x
            plt.xticks(rotation=90)
            # Añadir el valor de los puntos en la parte superior de cada barra
            for bar, pts in zip(bars, dataframe_filtrado[f'{stat}']):
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(pts), ha='center', va='bottom')



        if graph == "plot":
            fig, ax = plt.subplots()
            ax.plot(dataframe_filtrado['Date'], dataframe_filtrado[f'{stat}'])

            ax.set(xlabel='Date', ylabel=f'{stat}',
                   title='About as simple as it gets, folks')
            ax.grid()



        plt.tight_layout()  # Ajustar el diseño
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        # Codificar la imagen en base64 para mostrarla en la página web
        img_base64 = base64.b64encode(img.getvalue()).decode()
        return img_base64  # Mostrar el gráfico


def get_all_players():
    url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'per_game_stats'})
    # Encontrar todas las etiquetas <td> con los atributos específicos
    rows = table.find_all('td', {'class': 'left', 'data-stat': 'player'})
    datos = {}
    for row in rows:
        player_id = row.get('data-append-csv')
        player_name = row.a.get_text(strip=True)
        if player_id not in datos:
            datos[player_id] = player_name
    return list(datos.items())


def chunks(lst, n):
    """Divide una lista en n partes"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

