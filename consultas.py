from bs4 import BeautifulSoup
import requests
import re
import json

def fetch_html(url):
    """Fetches the HTML content from the given URL using a session."""
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_episode(episode):
    """Parses and returns the information of a single episode."""
    link = episode.find('a').get('href') if episode.find('a') else "No encontrado"
    title = episode.find('h4').get_text(strip=True) if episode.find('h4') else "No encontrado"
    description = episode.find('p', class_="episode-description-atc").get_text(strip=True) if episode.find('p', class_="episode-description-atc") else "No encontrada"
    metadata = episode.find('p', class_="episode-metadata-atc").get_text(strip=True) if episode.find('p', class_="episode-metadata-atc") else "No encontrada"

    return {
        "Titulo": title,
        "Link": link,
        "Descripción": description,
        "Metadata": metadata
    }

def scrape_series(url):
    """Scrapes the series from the given URL and returns a dictionary with episodes organized by season."""
    #series_data = {}

    html_content = fetch_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup.prettify())  
        # seccion = soup.find('div', class_="inner")
        # titulo = seccion.find('h2').get_text(strip=True) if seccion.find('h2') else "No encontrado"
        # descripcion = seccion.find('p').get_text(strip=True) if seccion.find('p') else "No encontrada"
        # print(f"Titulo: {titulo}")
        # print(f"Descripción: {descripcion}")
        #print(soup.prettify())
    return "titulo"


# Bien
# https://pluto.tv/latam/live-tv/5dcde437229eff00091b6c30/details?lang=en
# Mal
# https://pluto.tv/latam/live-tv/5dcde437229eff00091b6c30/details/66ba2d6dfe11e5000881b201?lang=en
# Mal body-0-2-14
# https://pluto.tv/latam/live-tv/5dcde437229eff00091b6c30/details/66ba2d6dfe11e5000881b201?lang=en
# https://pluto.tv/latam/on-demand/series/650b116e6930bb00136f67a5/season/1?lang=en    
link = "https://pluto.tv/latam/on-demand/619043246d03190008131b89/60941dfa8ab0970007f41c59?lang=en"


series_json = scrape_series(link)

# Convertir el diccionario a JSON y guardar en un archivo o imprimir
series_json_str = json.dumps(series_json, indent=4, ensure_ascii=False)

