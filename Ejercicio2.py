"""
Utilizando los datos de título y categoría del dataset del ejercicio anterior, entrenar un
modelo de clasificación de noticias en categorías específicas.
"""
#Importaciones ya hechas pero que permiten el coloreo sintáctico
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.linear_model import LogisticRegression
import pandas as pd
# Cargar el tokenizador y modelo preentrenado de BERT en español
sp_bert_name = 'dccuchile/bert-base-spanish-wwm-cased'
sp_bert_tokenizer = BertTokenizer.from_pretrained(sp_bert_name)
sp_bert_model = BertModel.from_pretrained(sp_bert_name)


# Obtener los embeddings de BERT para una lista de textos
def get_sp_bert_embeddings(texts):
    embeddings = []
    for text in texts:
        inputs = sp_bert_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            outputs = sp_bert_model(**inputs)
        # Usamos el embedding del token [CLS] como la representación del texto
        embeddings.append(outputs.last_hidden_state[0][0].numpy())
    return np.array(embeddings)


# Preparado de datos
def data_preprocessing_and_split(df):
    # Preparar X e y
    X = df.titulo.values
    y = df.categoria.values
    # División del dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Obtenemos los embeddings de BERT para los conjuntos de entrenamiento y prueba
    X_train_vectorized = get_sp_bert_embeddings(X_train)
    X_test_vectorized = get_sp_bert_embeddings(X_test)
    return X_train_vectorized, X_test_vectorized, y_train, y_test


# Entrenamiento del modelo
def training(X_train, y_train):
    # Creación y entrenamiento del modelo de Regresión Logística
    modelo_LR = LogisticRegression(max_iter=1000, multi_class='multinomial')
    modelo_LR.fit(X_train, y_train)
    return modelo_LR

# Evaluación del modelo
def evaluation(modelo_LR, X_test, y_test):
    # Predicción
    y_pred_LR = modelo_LR.predict(X_test)
    # Evaluación
    acc_LR = accuracy_score(y_test, y_pred_LR)
    report_LR = classification_report(y_test, y_pred_LR, zero_division=1)
    print("Precisión Regresión Logística:", acc_LR)
    print("Reporte de clasificación Regresión Logística:\n", report_LR)
    # Matriz de confusión
    confusion = confusion_matrix(y_test, y_pred_LR)
    print(confusion, '\n')


# Clasificación de nuevas frases
def classify_new_phrases(modelo_LR, new_phrases):
    # Preprocesamiento y vectorización de las nuevas frases
    new_phrases_lower = [text.lower() for text in new_phrases]
    new_phrases_vectorized = get_sp_bert_embeddings(new_phrases_lower)
    # Predicciones de las mismas con el modelo entrenado
    new_predictions = modelo_LR.predict(new_phrases_vectorized)
    # Mostrando las predicciones
    for text, label in zip(new_phrases, new_predictions):
        print(f"Texto: '{text}.Clasificación predicha: {label}\n'")
