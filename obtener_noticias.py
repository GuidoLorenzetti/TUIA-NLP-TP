import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
import torch
from transformers import BartForConditionalGeneration, BartTokenizer

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

from bs4 import BeautifulSoup

def scrap_new(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    title_element = soup.find('h1', class_='article-headline')
    title_text = title_element.text.strip()

    subheadline_element = soup.find('h2', class_='article-subheadline')
    subheadline_text = subheadline_element.text.strip()

    paragraph_elements = soup.find_all('p', class_='paragraph')

    paragraphs = []  # Lista para almacenar los párrafos

    # Agrega el subtítulo como el primer párrafo
    paragraphs.append(subheadline_text)

    for paragraph_element in paragraph_elements:
        # Extrae y almacena el texto del párrafo en la lista de párrafos
        paragraph_text = paragraph_element.text.strip()
        paragraphs.append(paragraph_text)

    # Combina los párrafos en un solo texto, separados por saltos de línea
    texto = '\n'.join(paragraphs)

    return title_text, texto

def generate_summaries(article_texts, max_length=500, num_beams=4, length_penalty=2.0, batch_size=4):
    # Dividir los textos en lotes más pequeños
    text_batches = [article_texts[i:i + batch_size] for i in range(0, len(article_texts), batch_size)]
    
    # Definir el dispositivo (GPU si está disponible, de lo contrario, CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    summaries = []

    for batch in text_batches:
        # Tokenización por lotes
        input_ids = tokenizer(
            batch,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=1024  # Ajusta el tamaño máximo según tus necesidades
        )["input_ids"].to(device)

        # Generación de resúmenes por lotes
        output_ids = model.generate(
            input_ids=input_ids,
            max_length=max_length,  # Ajusta la longitud del resumen deseado
            num_beams=num_beams,
            length_penalty=length_penalty,
            early_stopping=True,
        )

        # Decodificación de los resúmenes en texto
        batch_summaries = [tokenizer.decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False) for ids in output_ids]
        summaries.extend(batch_summaries)

    return summaries

def load_csv():
    df = pd.DataFrame(columns=['url', 'titulo', 'texto', 'categoria'])
    categoria = ["economia", "deportes", "salud", "tecno"]
    print("Cargando noticias...")
    for categ in categoria:
        noticias = scrap_page(categ)
        for url in noticias[:10]:
            response = requests.get(url)
            if response.status_code == 200:                
                title_text, text = scrap_new(response)
                nueva_fila = {'url': url,'titulo': title_text, 'texto': text, 'categoria': categ}
                df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    print("Noticias cargadas!")
    print("Generando resumenes...")
    df['resumen'] = generate_summaries(df['texto'].tolist())
    print("Resumenes generados!")
    df.to_csv('noticias.csv', sep=';', index=False) 

    return df

def generate_category_summary(df, category, max_length=500, num_beams=4, length_penalty=2.0):
    # Filtrar el DataFrame por la categoría especificada
    category_df = df[df['categoria'] == category]

    if category_df.empty:
        print(f"No se encontraron noticias para la categoría '{category}'.")
        return ""

    # Definir el dispositivo (GPU si está disponible, de lo contrario, CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    summaries = []

    for index, row in category_df.iterrows():
        article_text = row['resumen']
        input_ids = tokenizer(
            article_text,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=1024  # Ajusta el tamaño máximo según tus necesidades
        )["input_ids"].to(device)

        output_ids = model.generate(
            input_ids=input_ids,
            max_length=max_length,  # Ajusta la longitud del resumen deseado
            num_beams=num_beams,
            length_penalty=length_penalty,
            early_stopping=True,
        )

        summary = tokenizer.decode(output_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        summaries.append(summary)

    # Combinar resúmenes individuales en un resumen completo
    result_summary = " ".join(summaries)

    return result_summary

def obtener_precio_dolar():
    url = "https://www.infobae.com"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encuentra todos los divs con la clase "exchange-dolar-container"
        divs = soup.find_all('div', class_='exchange-dolar-item')

        # Inicializa variables para precios
        precio_bn = None
        precio_libre = None
        
        # Itera a través de los divs para buscar los datos de interés
        for div in divs:
            # print(div)
            # print("\n")
            aria_label = div.find_next('a', {'aria-label': True})
            if aria_label:
                label_text = aria_label['aria-label']
                if label_text == 'Dólar Banco Nación':
                    precio_bn = div.find("p", class_="exchange-dolar-amount").text
                elif label_text == 'Dólar Libre':
                    precio_libre = div.find("p", class_="exchange-dolar-amount").text
        
        return precio_bn, precio_libre
    else:
        print(f"No se pudo acceder a la página. Código de estado: {response.status_code}")
        return None, None