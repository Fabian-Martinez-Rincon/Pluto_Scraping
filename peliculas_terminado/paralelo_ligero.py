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
from queue import Queue

options = Options()
options.headless = True
options.add_argument("--start-maximized")

def create_browser():
    return webdriver.Chrome(options=options)

def scroll(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div > div > h1'))
        ).click()

        body_element = driver.find_element(By.TAG_NAME, 'body')
        for i in range(40):
            body_element.send_keys(Keys.PAGE_DOWN)
            if i % 10 == 0:
                time.sleep(2)
    except TimeoutException:
        print("Element not visible for scrolling")

def procesar_link(data, browser_queue):
    text, url = data['text'], data['href']
    print(f"Procesando {text} en {url}")
    driver = browser_queue.get()
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
        browser_queue.put(driver)

with open('buttons.json', 'r') as file:
    links_json = json.load(file)

browser_queue = Queue(maxsize=4)
for _ in range(4):
    browser_queue.put(create_browser())

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(procesar_link, link, browser_queue) for link in links_json]
    concurrent.futures.wait(futures)

while not browser_queue.empty():
    driver = browser_queue.get()
    driver.quit()
