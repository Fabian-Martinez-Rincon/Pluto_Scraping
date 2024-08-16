import requests
import json
from bs4 import BeautifulSoup

def search_description(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        div = soup.find('div', class_='inner')
        if div:
            description = div.find('p')
        if description:
            return description.get_text(strip=True)
    return None

with open('resultados.json', 'r', encoding='utf-8') as json_file:
    links_json = json.load(json_file)

categories = {}

for item in links_json:
    button_text = item['button_text']
    url = item['url']
    
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Procesando de '{button_text}'...")
        html_content = response.text  # Trabajar directamente con el contenido HTML
        
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
                        link = 'https://pluto.tv' + link_tag.get('href') + '/details?lang=en'
                        description = search_description(link)
                        movies.append({
                            'title': title,
                            'link': link,
                            'description': description
                            #'image': img_url  # Puedes descomentar esta línea si necesitas la imagen
                        })

        categories[button_text] = {
            "count": len(movies),
            "movies": movies
        }

    else:
        print(f"Error al descargar {button_text}: {response.status_code}")

# Paso 3: Guardar los resultados en un archivo JSON
output_json_file = "movies_by_category.json"
with open(output_json_file, "w", encoding="utf-8") as outfile:
    json.dump(categories, outfile, ensure_ascii=False, indent=4)

print(f"Resultados guardados en {output_json_file}")
