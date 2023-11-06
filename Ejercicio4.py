"""
Use los modelos de embedding propuestos sobre el final de la Unidad 2 para evaluar la
similitud entre los títulos de las noticias de una de las categorías.
Reflexione sobre las limitaciones del modelo en base a los resultados obtenidos, en
contraposición a los resultados que hubiera esperado obtener.
"""
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import tensorflow_hub as hub
import tensorflow as tf
import plotly.express as px
from sklearn.decomposition import PCA
from collections import defaultdict

# Descargar recursos necesarios de NLTK
nltk.download('stopwords')
nltk.download('punkt')
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"

global model
model = hub.load(module_url)

def process_text(df, category):
    # Filtrar el DataFrame por la categoría deseada
    filtered_df = df[df['categoria'] == category]

    # Obtener una serie de pandas con los títulos filtrados
    titles_series = filtered_df['titulo']

    # Convertir la serie en una lista de títulos
    titles_list = titles_series.tolist()

    return titles_list

#_______________________________________________________________________________________________________________
#Removemos stopwords para cada titulo
def remove_stopwords(text):
    stop_words = set(stopwords.words('spanish'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]
    return " ".join(filtered_text)

#_______________________________________________________________________________________________________________
# heatmap para ver matriz de correlacion, con stopword y sin stopwords
def heatmap_sim(datos, titulo):    
    embeddings = model(datos)

    # Calcular la matriz de correlación de los embeddings
    matriz_correlacion = np.corrcoef(embeddings)

    # Graficar la matriz de similitud usando un mapa de calor
    plt.figure(figsize=(20, 16))
    sns.heatmap(matriz_correlacion, annot=True, cmap='YlGnBu', xticklabels=datos, yticklabels=datos)
    plt.title(titulo)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show(block = False)
    
#_______________________________________________________________________________________________________________
# Aplica PCA para reducir a 2 dimensiones
def pca_2d(datos, titulo):
    
    embeddings = model(datos)

    pca = PCA(n_components=2)
    embeddings_2d = pca.fit_transform(embeddings)

    # Grafica los vectores en un gráfico de dispersión
    plt.figure(figsize=(14, 10))
    for i, oracion in enumerate(datos):
        plt.scatter(embeddings_2d[i, 0], embeddings_2d[i, 1], marker='o')
        plt.annotate(oracion, (embeddings_2d[i, 0], embeddings_2d[i, 1]))

    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.title(titulo)
    plt.grid(True)
    plt.show(block = False)
        
#_______________________________________________________________________________________________________________
# Aplica PCA para reducir a 3 dimensiones
def pca_3d(datos, titulo):
    embeddings = model(datos)
    pca = PCA(n_components=3)
    embeddings_3d = pca.fit_transform(embeddings)
    # Crear un DataFrame con los datos
    df2 = pd.DataFrame(embeddings_3d, columns=['x', 'y', 'z'])
    df2['word'] = datos

    # Visualizar los embeddings en 3D usando plotly
    fig = px.scatter_3d(df2, x='x', y='y', z='z', text='word', size_max=18, opacity=0.7)

    # Agregar un título a la figura
    fig.update_layout(
        title=titulo,  # Agregar el título que desees
        scene=dict(
        xaxis_title='Componente Principal 1',
        yaxis_title='Componente Principal 2',
        zaxis_title='Componente Principal 3'))

    # Mostrar el gráfico
    fig.show(block = False)

def leer_filtrar(category,file_path):    
    
    df = pd.read_csv(file_path)
    
    # En cat guardamos los titulos de la categoria a analizar, sin remover stopwords  
    cat = process_text(df, category)
    
    textos = defaultdict(list)
    for _, row in df.iterrows():
        text = row['titulo'].lower()
        text = remove_stopwords(text)
        text = re.sub(f'[{string.punctuation}]', '', text)
        textos[row['categoria']].append(text)
    
    return cat, textos[category]



