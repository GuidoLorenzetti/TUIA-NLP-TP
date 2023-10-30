"""
Para cada categoría, realizar las siguientes tareas:
● Procesar el texto mediante recursos de normalización y limpieza.
● Con el resultado anterior, realizar conteo de palabras y mostrar la importancia de las
mismas mediante una nube de palabras.
Escribir un análisis general del resultado obtenido
"""
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

#NORMALIZACION
# Definir las palabras de parada en español
stop_words = set(stopwords.words('spanish'))
# Función para eliminar las palabras de parada de una frase
def remove_stopwords(text):
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]
    return " ".join(filtered_text)

df = pd.read_csv("archivo.csv")

textos = {}

labels = df.categoria.unique()
for label in labels:
    textos[label] = ''

for index, row in df.iterrows():
    textos[row['categoria']] += '   ' + row['texto']

for label, text in textos.items():
    text = text.lower()
    text = remove_stopwords(text)
    text = re.sub(f'[{string.punctuation}]', '', text)
    textos[label] = text
    

#WORDCLOUD
for label, text in textos.items():
    wordcloud = WordCloud(width = 1200, height = 800, background_color ='white', stopwords = None, min_font_size = 10).generate(text)
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.title(label)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()
    