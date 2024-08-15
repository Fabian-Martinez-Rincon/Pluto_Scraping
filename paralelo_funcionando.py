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
from selenium.common.exceptions import TimeoutException

options = Options()
options.headless = True
options.add_argument("--start-maximized")  # Inicia maximizado

def scroll(driver):
    try:
        time.sleep(5)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div > div > h1'))
        ).click()
        
        body_element = driver.find_element(By.TAG_NAME, 'body')
        for i in range(40):
            body_element.send_keys(Keys.PAGE_DOWN)
            if i % 10 == 0:
                time.sleep(2)  # Pausa cada 10 scrolls
    except TimeoutException:
        print("Element not visible for scrolling")

def procesar_link(data):
    text, url = data['text'], data['href']
    print(f"Procesando {text} en {url}")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        scroll(driver)
        items = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.custom-scroll > ul.reset-ul > li.itemContainer.vod-item-poster-atc"))
        )
        alt_attributes = [item.find_element(By.TAG_NAME, 'img').get_attribute('alt') if item.find_element(By.TAG_NAME, 'img') else "No image available" for item in items]
        print(alt_attributes)
    except Exception as e:
        print(f"Error processing {text}: {e}")
    finally:
        driver.quit()

with open('buttons.json', 'r') as file:
    links_json = json.load(file)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(procesar_link, links_json)
