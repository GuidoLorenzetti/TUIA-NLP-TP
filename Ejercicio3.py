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
from nltk.probability import FreqDist
nltk.download('stopwords')
nltk.download('punkt')
import itertools

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
    

#CONTEO DE PALABRAS
for label, text in textos.items():
    words = word_tokenize(text)
    fdist_words = FreqDist(words)
    freq = dict(fdist_words)
    print(f'Frecuencia de 5 palabras random de {label}:')
    for key, value in itertools.islice(freq.items(), 5):
        print(f'{key}: {value}')
    print("año:", freq['año'])
    print('\n')


#WORDCLOUD
fig, axes = plt.subplots(2, 2) # SOLO FUNCIONA PARA 4 CATEGORIAS
axes = axes.flat
for i in range(4):
    label = labels[i]  
    text = textos[label]
    wordcloud = WordCloud(width = 1000, height = 400, background_color ='white', stopwords = None, min_font_size = 15).generate(text)
    axes[i].imshow(wordcloud)
    axes[i].set_title(label)
    axes[i].axis("off")
plt.tight_layout()
plt.show()
    