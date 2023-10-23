#Usamos este script para obtener los datos de la noticia y cargarlos en el dataset

import requests
import pandas as pd
import numpy as np
import re

noticias = pd.read_csv('noticias.csv', sep=';')
def scrap_page(pagina):
   
    


    noticias.to_csv('noticias.csv', sep=';', index=False)