from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configura las opciones del navegador
options = Options()
options.headless = True  # Ejecuta el navegador en modo headless (sin interfaz gráfica)

# Inicializa el navegador con las opciones configuradas
driver = webdriver.Chrome(options=options)

# Carga la página
url = "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/631a0596822bbc000747c340?lang=en"
driver.get(url)

# Espera hasta que un elemento clave esté presente para asegurarte de que todo el contenido está cargado
# Ajusta el selector según lo que sea necesario para la página
driver.implicitly_wait(10)

# Obtén el HTML renderizado
html = driver.page_source

# Guarda el HTML renderizado en un archivo
with open("pluto_page_rendered.html", "w", encoding="utf-8") as file:
    file.write(html)

# Cierra el navegador
driver.quit()

print("Contenido completamente renderizado guardado en pluto_page_rendered.html")
