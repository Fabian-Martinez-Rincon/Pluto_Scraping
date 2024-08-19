from bs4 import BeautifulSoup
import requests
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

def scrape_metadata(url):
    """Scrapes metadata from the given URL and returns a dictionary of metadata."""
    html_content = fetch_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {
            "Title": soup.find('title').text if soup.find('title') else "No encontrado",
            "Description": soup.find('meta', attrs={"name": "description"})['content'] if soup.find('meta', attrs={"name": "description"}) else "No encontrada",
            "Open Graph Data": {meta.attrs['property'][3:]: meta.attrs['content'] for meta in soup.find_all('meta', property=True) if meta.attrs['property'].startswith('og:')},
            "Twitter Card Data": {meta.attrs['name'][6:]: meta.attrs['content'] for meta in soup.find_all('meta', attrs={"name": lambda value: value and value.startswith("twitter:")})},
            "Schema.org Data": [json.loads(script.string) for script in soup.find_all('script', type="application/ld+json") if script.string],
            "Favicons": [link['href'] for link in soup.find_all('link', rel="icon") + soup.find_all('link', rel="shortcut icon")]
        }
        return metadata
    else:
        return "Error fetching HTML content."

# URL to scrape
url = "https://pluto.tv/latam/on-demand/series/6346d286cba1290014d86384/details?lang=en"

# Fetch metadata
metadata = scrape_metadata(url)

# Convert the dictionary to JSON and print
metadata_json = json.dumps(metadata, indent=4, ensure_ascii=False)
print(metadata_json)
