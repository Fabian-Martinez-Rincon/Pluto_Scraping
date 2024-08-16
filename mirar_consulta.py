from bs4 import BeautifulSoup
import requests
import re

def fetch_html(url):
    with requests.Session() as session:
        response = session.get(url)
        return response.text if response.status_code == 200 else None

def imprimir_elementos(soup):
    for i in soup:
        print(i.find('h4').get_text())
    print("____________")

link = "https://pluto.tv/latam/on-demand/series/65f47080ea323e0013229672/season/1"

html_content = fetch_html(link)

soup = BeautifulSoup(html_content, 'html.parser')
seccion = soup.find('div', class_='inner')
EXPRESIONES = r'(Temporada|Season|season|temporada) \d+'
temporadas = [a.get_text(strip=True) for a in seccion.findAll('a') if re.match(EXPRESIONES, a.get_text(strip=True))] if seccion else []
imprimir_elementos(soup.find_all('section', class_='episode-details'))

for i in range(2, len(temporadas)+1):
    html_content = fetch_html(link[:-1] + str(i))
    soup = BeautifulSoup(html_content, 'html.parser')
    imprimir_elementos(soup.find_all('section', class_='episode-details'))





















#temporadas = soup.find_all('li', class_='episode-container-atc')
#temporadas = [a.get_text(strip=True) for a in soup.findAll('a') if 'season' in a.get('href', '').lower()] if soup else []


# for i in seccion:
#     print(i.find('h4').get_text())
#print(soup.prettify())
    
print()
#print(seccion)
    
    