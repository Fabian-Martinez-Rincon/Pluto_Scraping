from bs4 import BeautifulSoup

with open("pluto_page.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

movies = []
start_collecting = False  

ul_element = soup.find('ul')

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
                        'link': link,
                        'image': img_url
                    })

for movie in movies:
    print(f"Title: {movie['title']}")
    print(f"Link: {movie['link']}")
    print(f"Image: {movie['image']}")
    print("-----")
    
print(f"Total movies: {len(movies)}")
