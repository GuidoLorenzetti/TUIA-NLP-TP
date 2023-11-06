"""
Para cada categoría, realizar las siguientes tareas:
● Procesar el texto mediante recursos de normalización y limpieza.
● Con el resultado anterior, realizar conteo de palabras y mostrar la importancia de las
mismas mediante una nube de palabras.
Escribir un análisis general del resultado obtenido
"""
#Importaciones ya hechas pero que permiten el coloreo sintáctico
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Función para eliminar las stopwords en español de una frase
def remove_sp_stopwords(text):
    # Definir las palabras de parada en español
    stop_words = set(stopwords.words('spanish'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]
    return " ".join(filtered_text)

#Extracción de textos del df y normalización y limpieza
def df2texts(df):
    # Inicialización de diccionario de textos
    textos = {}
    for label in df.categoria.unique():
        textos[label] = ''
    # Llenado del diccionario de textos
    for index, row in df.iterrows():
        textos[row['categoria']] += ' . ' + row['texto']
    
    return textos

#Normalización y limpiado de textos
def texts_normalization(textos):
    nltk.download('stopwords')
    nltk.download('punkt')
    for label, text in textos.items():
        text = text.lower()
        text = remove_sp_stopwords(text)
        text = re.sub(f'[{string.punctuation}]', '', text)
        text = text.replace('“', '').replace('”', '')
        textos[label] = text

    return textos

#Conteo de palabras
def texts2freqs(textos):
    freqs = {}
    for label, text in textos.items():
        words = word_tokenize(text)
        freq = FreqDist(words)
        freqs[label] = dict(freq)
    return freqs

# Top 5 de palabras más frecuentes
def top_freqs(freqs, label):
    print(f'5 palabras más frecuentes de {label}:')
    freq = freqs[label]
    sorted_items = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    print(dict(sorted_items[:5]))

#Nubes de palabras
def wordclouds(textos): # SOLO FUNCIONA PARA 4 de cada
    fig, axes = plt.subplots(2, 2) 
    axes = axes.flat
    for i, (label, text) in enumerate(textos.items()):
        wordcloud = WordCloud(width = 1000, height = 400, background_color ='white', stopwords = None, min_font_size = 15).generate(text)
        axes[i].imshow(wordcloud)
        axes[i].set_title(label)
        axes[i].axis("off")
    plt.tight_layout()
    plt.show()

# Sólo una nube de palabras
def wordcloud(textos, label):
    text = textos[label]
    wordcloud = WordCloud(width = 1000, height = 400, background_color ='white', stopwords = None, min_font_size = 15).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()