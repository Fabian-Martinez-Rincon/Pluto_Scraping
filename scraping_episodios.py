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
        seccion = soup.find('div', class_='inner')

        # Buscar temporadas
        EXPRESIONES = r'(Temporada|Season|season|temporada) \d+'
        temporadas = [a.get_text(strip=True) for a in seccion.findAll('a') if re.match(EXPRESIONES, a.get_text(strip=True))] if seccion else []

        # Scrape episodios de la primera temporada
        season_number = 1
        series_data[f"Temporada {season_number}"] = [
            parse_episode(episode) for episode in soup.find_all('li', class_='episode-container-atc')
        ]

        # Iterar sobre las temporadas restantes
        for i in range(2, len(temporadas) + 1):
            season_url = f"{url[:-1]}{i}"
            html_content = fetch_html(season_url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                season_number += 1
                series_data[f"Temporada {season_number}"] = [
                    parse_episode(episode) for episode in soup.find_all('li', class_='episode-container-atc')
                ]

    return series_data

# Enlace a la primera temporada
link = "https://pluto.tv/latam/on-demand/series/65f47080ea323e0013229672/season/1"
series_json = scrape_series(link)

# Convertir el diccionario a JSON y guardar en un archivo o imprimir
series_json_str = json.dumps(series_json, indent=4, ensure_ascii=False)
print(series_json_str)
