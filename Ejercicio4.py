import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
from collections import defaultdict


def ejercicio_4(category):

    df = pd.read_csv("archivo.csv")

    # Inicializa un diccionario vacío para almacenar las noticias por categoría
    titulo_categoria = {}

    # Itera a través de las filas del DataFrame
    for index, row in df.iterrows():
        titulo = row['titulo']
        categoria = row['categoria']

        # Verifica si la categoría ya está en el diccionario
        if categoria in titulo_categoria:
            titulo_categoria[categoria].append(titulo)
        else:
            titulo_categoria[categoria] = [titulo]
  #_______________________________________________________________________________________________________________
  # En cat guardamos los titulos de la categoria a analizar, sin remover stopwords  
    cat = titulo_categoria[category]
  #_______________________________________________________________________________________________________________
    #Removemos stopwords para cada titulo
    stop_words = set(stopwords.words('spanish'))
  
    def remove_stopwords(text):
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]
        return " ".join(filtered_text)

    textos = defaultdict(list)

    labels = df.categoria.unique()

    for index, row in df.iterrows():
        text = row['titulo'].lower()
        text = remove_stopwords(text)
        text = re.sub(f'[{string.punctuation}]', '', text)
        textos[row['categoria']].append(text)