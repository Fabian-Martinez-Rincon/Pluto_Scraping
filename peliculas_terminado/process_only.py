from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
import json
import csv
from selenium.common.exceptions import NoSuchElementException


def save_to_json(data, filename="buttons.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def movie_peliculas(driver):
    print("Clic y scroll completados con éxito")
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/div/span/span/h3')))
    element.click()
    body = driver.find_element(By.TAG_NAME, 'body')
    for i in range(200): 
        print(i)
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.01)

def click_button_by_text(driver, button_text):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{button_text}']"))
        )
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on: {button_text}")
        
    except Exception as e:
        print(f"Error al hacer clic en '{button_text}': {str(e)}")

def click_button_and_get_nav_items(driver, button_xpath):
    driver.find_element(By.XPATH, button_xpath).click()
    nav = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/nav"))
    )
    nav_items = nav.find_elements(By.TAG_NAME, "a")
    buttons = [{'text': item.text, 'href': item.get_attribute('href')} for item in nav_items]
    
    return buttons

def config():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def start():
    driver = config()
    driver.get('https://pluto.tv')

    on_demand= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, 'On Demand')
        )
    )
    on_demand.click()
    
    time.sleep(1)
    click_button_by_text(driver, "Películas")
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/section[3]/span/div/div[1]/span/a').click()
    time.sleep(1)
    
    button_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button'
    
    buttons = click_button_and_get_nav_items(driver, button_xpath)
    print("Buttons:", buttons)
    save_to_json(buttons)
    time.sleep(3)
    
    return driver

def main():
    driver = start()
    elementos= WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'ul.reset-ul')
        )
    )
    elementos.click()
    
    # Realiza un desplazamiento hacia abajo en la página
    body_element = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(10):
        body_element.send_keys(Keys.PAGE_DOWN)
    
    time.sleep(3)
    items = driver.find_elements(By.CSS_SELECTOR, "div.custom-scroll > ul.reset-ul > li.itemContainer.vod-item-poster-atc")
    alt_attributes = []
    for item in items:
        try:
            img_element = item.find_element(By.TAG_NAME, 'img')
            alt = img_element.get_attribute('alt')
            alt_attributes.append(alt)
        except NoSuchElementException:
            alt_attributes.append("No image available")
            
    for alt in alt_attributes:
        print(alt)
        time.sleep(1)
        link_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"a img[alt='{alt}']"))
        )
        parent_link = link_element.find_element(By.XPATH, "..")
        driver.execute_script("arguments[0].scrollIntoView(true);", parent_link)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(parent_link))
        parent_link.click()
        time.sleep(1)
        rect_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-content-details-atc"))
        )
        rect_element.click()
        time.sleep(1)
    
    # results = []

    # for item in items:
    #     try:
    #         link_element = item.find_element(By.TAG_NAME, 'a')
    #         link = link_element.get_attribute('href')
            
    #         try:
    #             img_element = link_element.find_element(By.TAG_NAME, 'img')
    #             name = img_element.get_attribute('alt')
    #         except NoSuchElementException:
    #             name = "No image available"  # Manejo de casos donde no hay imagen disponible

    #         results.append((name, link))
    #     except NoSuchElementException as e:
    #         print(f"Error: {e}")

    # # Guardar los resultados en un archivo CSV
    # with open('pluto_tv_content.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Nombre', 'Enlace'])  # Escribir la cabecera del CSV
    #     writer.writerows(results)  # Escribir todas las filas de resultados

    print("Datos guardados en 'pluto_tv_content.csv'.")
    driver.quit()
    
if __name__ == "__main__":
    main()