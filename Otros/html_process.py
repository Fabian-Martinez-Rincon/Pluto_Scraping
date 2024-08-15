import requests

url = "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6245e3e75b72240007129448?lang=en"

response = requests.get(url)

if response.status_code == 200:
    with open("pluto_page.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("Contenido guardado en pluto_page.html")
else:
    print(f"Error: {response.status_code}")
