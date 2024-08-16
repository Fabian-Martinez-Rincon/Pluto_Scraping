from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

# Navegar a la página
driver.get('https://pluto.tv/')

# Esperar a que la página cargue completamente
time.sleep(3)

# Lista para almacenar los elementos capturados

try:
    element_to_click = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/button/span/span')
    element_to_click.click()
    time.sleep(30)
    print("Elemento clicado exitosamente.")
except Exception as e:
    print(f"No se pudo hacer clic en el elemento: {e}")


all_channels = []
