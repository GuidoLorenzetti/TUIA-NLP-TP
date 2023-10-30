import requests
import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup

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
        divs = soup.find_all('div', {"class":'feed-list-wrapper'})
        links = [x.find_all('a', href=True) for x in divs]
        links1 = [item for sublist in links for item in sublist]
        # Filtrar los enlaces que empiezan por "{cateogoria}/" y no están en elementos de imagen
        url_links = [link['href'] for link in links1 if link['href'].startswith(f'/{categoria}/')]

        # Encontrar todos los enlaces en la página
        divs2 = soup.find_all('div', {"class":'story-card-info'})
        links2 = [x.find_all('a', href=True) for x in divs2]
        links2 = [item for sublist in links2 for item in sublist]
        # Filtrar los enlaces que empiezan por "{cateogoria}/" y no están en elementos de imagen
        url_links2 = [link['href'] for link in links2 if link['href'].startswith(f'/{categoria}/')]

        # Imprimir los enlaces
        for link in url_links+url_links2:
            if f"https://www.infobae.com/{link}" not in noticias:
                noticias.append(f"https://www.infobae.com/{link}")

    else:
        print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")

    return noticias

def agregar_text_title(df, url, titulo, texto, categoria):
    # Crear una nueva fila como un diccionario
    nueva_fila = {'url': url,'titulo': titulo, 'texto': texto, 'categoria': categoria}

    # Usar el método append para agregar la nueva fila al DataFrame
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

    return df

def title_text(df, url, categoria):
    #Acá voy a tener una lista de urls, la recorro y hago esto para cada noticia
    # URL de la página a la que deseas hacer web scraping
    #Aca lo cargo a la fila del csv en df["url"]


    # Realiza una solicitud GET a la página
    response = requests.get(url)

    # Verifica si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Parsea el contenido HTML de la página usando BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encuentra el elemento HTML que contiene el título
        # Ajusta el selector CSS según la estructura de la página
        title_element = soup.find('h1', class_='article-headline')

        # Extrae y muestra el texto del título
        title_text = title_element.text.strip()
        #print(f'Título: {title_text}')

        # Encuentra los elementos HTML que son párrafos
        # En este caso, simplemente buscamos todos los elementos <p> en la página
        paragraph_elements = soup.find_all('p', class_='paragraph')

        texto = ""
        # Itera a través de los elementos y muestra el texto de los párrafos
        for paragraph_element in paragraph_elements:
            # Extrae y muestra el texto del párrafo
            paragraph_text = paragraph_element.text.strip()
            texto = texto + paragraph_text

        df = agregar_text_title(df, url, title_text, texto, categoria)

    else:
        print(f'Error al obtener la página. Código de estado: {response.status_code}')

    return df

def cargar_csv():
    df = pd.DataFrame(columns=['url', 'titulo', 'texto', 'categoria'])
    categoria = ["economia", "deportes", "salud", "tecno"]

    for categ in categoria:
        noticias = scrap_page(categ)
        for url in noticias:
            df = title_text(df, url, categ)

    df.to_csv('noticias.csv', sep=';', index=False) 

    return df