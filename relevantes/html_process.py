import requests

url = "https://pluto.tv/latam/on-demand/series/6346d286cba1290014d86384/details?lang=en"

response = requests.get(url)

if response.status_code == 200:
    with open("pluto_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("Contenido guardado en pluto_page.html")
else:
    print(f"Error: {response.status_code}")
