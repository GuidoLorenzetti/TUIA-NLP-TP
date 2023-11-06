"""
Construir un dataset haciendo web scraping de páginas web de su elección.
● Definir 4 categorías de noticias/artículos.
● Para cada categoría, extraer los siguientes datos de 10 noticias diferentes:
    ○ url (sitio web donde se publicó el artículo)
    ○ título (título del artículo)
    ○ texto (contenido del artículo)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from obtener_noticias import scrap_page

def agregar_text_title(url, titulo, texto, categoria):
    global df
    # Crear una nueva fila como un diccionario
    nueva_fila = {'url': url,'titulo': titulo, 'texto': texto, 'categoria': categoria}

    # Usar el método append para agregar la nueva fila al DataFrame
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)

def title_text(url, categoria):
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

        #print(texto)
        agregar_text_title(url, title_text, texto, categoria)

    else:
        print(f'Error al obtener la página. Código de estado: {response.status_code}')
# lista_url = ['https://www.infobae.com/economia/2023/10/23/por-que-se-mantiene-la-presion-cambiaria-a-pesar-de-que-se-alejo-la-posibilidad-del-plan-de-dolarizacion-de-milei/']

def scrapping():
    categoria = ["economia", "deportes", "salud", "tecno"]

    for categ in categoria:
        noticias = scrap_page(categ)
        for url in noticias:
            title_text(url, categ)