import requests

url = "https://pluto.tv/latam/on-demand/63595e964ea0c60007fc1801/5e98bb7fcff347000722985e"

response = requests.get(url)

if response.status_code == 200:
    with open("pluto_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("Contenido guardado en pluto_page.html")
else:
    print(f"Error: {response.status_code}")
