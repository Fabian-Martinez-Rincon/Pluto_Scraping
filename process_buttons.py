import json
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import io

options = Options()
options.headless = True

html_dir = 'html_files'
os.makedirs(html_dir, exist_ok=True)

def procesar_link(data):
    text, url = data['text'], data['href']
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        html_content = driver.page_source
        filename = os.path.join(html_dir, f"{text.replace(' ', '_').replace('/', '_')}.html")
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML de {text} guardado en {filename}")
    finally:
        driver.quit()

with open('buttons.json', 'r') as file:
    links_json = json.load(file)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(procesar_link, links_json)
