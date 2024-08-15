import os
import requests
import json
from bs4 import BeautifulSoup

# Paso 1: Descargar las páginas HTML y guardarlas
with open('resultados.json', 'r', encoding='utf-8') as json_file:
    links_json = json.load(json_file)

output_folder = "pluto_pages"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for item in links_json:
    button_text = item['button_text']
    url = item['url']
    response = requests.get(url)
    if response.status_code == 200:
        safe_button_text = button_text.replace(" ", "_").replace("/", "_")
        filename = f"{safe_button_text}.html"
        filepath = os.path.join(output_folder, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(response.text)
        
        print(f"Contenido de '{button_text}' guardado en {filepath}")
    else:
        print(f"Error al descargar {button_text}: {response.status_code}")

# Paso 2: Procesar las páginas HTML descargadas con BeautifulSoup
categories = {}

for item in links_json:
    button_text = item['button_text']
    safe_button_text = button_text.replace(" ", "_").replace("/", "_")
    filepath = os.path.join(output_folder, f"{safe_button_text}.html")
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        start_collecting = False  # Reiniciar para cada página
        movies = []

        for item in soup.find_all('li'):
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.get('title', link_tag.get_text(strip=True))

                if title == "Invierno de Película":
                    start_collecting = True
                    continue

                if start_collecting: 
                    img_tag = link_tag.find('img')
                    if img_tag:
                        img_url = img_tag['src']
                        
                        if 'image' in img_url:
                            link = 'https://pluto.tv' + link_tag.get('href')
                            movies.append({
                                'title': title,
                                'link': link
                                #'image': img_url
                            })

        categories[button_text] = {
            "count": len(movies),
            "movies": movies
        }

# Paso 3: Guardar los resultados en un archivo JSON
output_json_file = "movies_by_category.json"
with open(output_json_file, "w", encoding="utf-8") as outfile:
    json.dump(categories, outfile, ensure_ascii=False, indent=4)

print(f"Resultados guardados en {output_json_file}")
