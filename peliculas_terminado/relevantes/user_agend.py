import requests

# Crear una solicitud GET
url = "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/6419c584dbdaaa000845cad0?lang=en"
response = requests.get(url)

# Imprimir el User-Agent utilizado
print(f"User-Agent utilizado: {response.request.headers['User-Agent']}")
