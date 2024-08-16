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
    series_data = {}

    html_content = fetch_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        print(soup.prettify())
    return series_data

# Enlace a la primera temporada
link = "https://pluto.tv/latam/live-tv/63eb9255c111bc0008fe6ec4/details?lang=en"

series_json = scrape_series(link)

# Convertir el diccionario a JSON y guardar en un archivo o imprimir
series_json_str = json.dumps(series_json, indent=4, ensure_ascii=False)
print(series_json_str)
