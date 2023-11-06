def libraries_import():
    # EJ 1
    import warnings
    #warnings.filterwarnings("ignore")
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from obtener_noticias import scrap_page

    # EJ 2
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

    # EJ 3
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

    #EJ 4
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