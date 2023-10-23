#Usamos este script para obtener los datos de la noticia y cargarlos en el dataset

import requests
import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup


noticias = pd.read_csv('noticias.csv', sep=';')
noticias = noticias.iloc[0:0]

def scrap_page(categoria):
    noticias = []
    # URL de la página que deseas raspar
    url = f"https://www.infobae.com/{categoria}/"

    # Realizar una solicitud GET a la URL
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Analizar el contenido HTML de la página con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los enlaces en la página
        divs = soup.find_all('div', {"class":'story-card-info'})
        links = [x.find_all('a', href=True) for x in divs]
        links1 = [item for sublist in links for item in sublist]
        # Filtrar los enlaces que empiezan por "{cateogoria}/" y no están en elementos de imagen
        url_links = [link['href'] for link in links1 if link['href'].startswith(f'/{categoria}/')]

        # Imprimir los enlaces
        for link in url_links:
            if f"https://www.infobae.com{link}" not in noticias:
                noticias.append(f"https://www.infobae.com{link}")
    else:
        print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")

    return noticias