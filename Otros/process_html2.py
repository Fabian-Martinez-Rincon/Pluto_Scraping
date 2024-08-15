from bs4 import BeautifulSoup

with open("pluto_page.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

movies = []

# Encuentra el contenedor principal
container = soup.find('div', class_='custom-scroll')
if container:
    # Encuentra todos los items dentro del contenedor
    items = container.find_all('li', class_='itemContainer vod-item-poster-atc')
    
    for item in items:
        link_tag = item.find('a')
        if link_tag:
            link = 'https://pluto.tv' + link_tag.get('href')
            title = link_tag.get('title', link_tag.get_text(strip=True))

            img_url = None
            img_tag = link_tag.find('img')
            if img_tag:
                img_url = img_tag.get('src')
            
            movies.append({
                'title': title,
                'link': link,
                'image': img_url
            })

for movie in movies:
    print(f"Title: {movie['title']}")
    print(f"Link: {movie['link']}")
    print(f"Image: {movie['image']}")
    print("-----")
