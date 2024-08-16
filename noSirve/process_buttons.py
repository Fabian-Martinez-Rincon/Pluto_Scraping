from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import json
import concurrent.futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = Options()
options = Options()
options.headless = True
options.add_argument("--start-maximized")  # Inicia maximizado

def scroll(driver):
    elementos= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div.custom-scroll > ul.reset-ul')
            )
        )
    elementos.click()
    body_element = driver.find_element(By.TAG_NAME, 'body')
    for i in range(40):
        body_element.send_keys(Keys.PAGE_DOWN)
        if (i == 15):
            time.sleep(2)
        if (i == 30):
            time.sleep(2)

def procesar_link(data):
    text, url = data['text'], data['href']
    print(f"Procesando {text}")
    print(f"URL: {url}")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        scroll(driver)
        time.sleep(2)
        items = driver.find_elements(By.CSS_SELECTOR, "div.custom-scroll > ul.reset-ul > li.itemContainer.vod-item-poster-atc")
        alt_attributes = []
        time.sleep(2)
        for item in items:
            try:
                img_element = item.find_element(By.TAG_NAME, 'img')
                alt = img_element.get_attribute('alt')
                alt_attributes.append(alt)
            except NoSuchElementException:
                alt_attributes.append("No image available")
        print(alt_attributes)
    finally:
        driver.quit()

with open('buttons.json', 'r') as file:
    links_json = json.load(file)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(procesar_link, links_json)
