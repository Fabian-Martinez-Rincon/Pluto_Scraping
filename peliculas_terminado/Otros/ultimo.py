from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def setup_driver(driver_path, incognito=True, maximized=True):
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    if incognito:
        options.add_argument("--incognito")
    if maximized:
        options.add_argument("--start-maximized")
    return webdriver.Chrome(service=service, options=options)

def wait_and_click(driver, xpath, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except Exception as e:
        print(f"Error al hacer clic en el elemento con XPath '{xpath}': {str(e)}")

def scroll_down(driver, steps=200, delay=0.01):
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(steps):
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(delay)

def is_button_selected(driver, button_text):
    try:
        button = driver.find_element(By.XPATH, f"//span[text()='{button_text}']/ancestor::div[contains(@class, 'l2-category-atc')]")
        return "selected" in button.get_attribute("class")
    except Exception as e:
        print(f"Error verificando el estado del botón '{button_text}': {str(e)}")
        return False

def movie_init(driver):
    wait_and_click(driver, '/html/body/div[1]/div/div/div/main/div[2]/section/div[3]/div[3]')
    scroll_down(driver, steps=15, delay=0.1)

def movie_peliculas(driver, button_text="Películas"):
    print("Clic y scroll completados con éxito")
    wait_and_click(driver, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/section[4]/span/div')
    
    # Realizar scroll hasta que el botón no esté seleccionado
    while is_button_selected(driver, button_text):
        scroll_down(driver, steps=1, delay=0.01)
    
    print(f"El botón '{button_text}' ya no está seleccionado.")
    wait_and_click(driver, f"//span[text()='{button_text}']/ancestor::div[contains(@class, 'l2-category-atc')]")

def click_button_by_text(driver, button_text):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{button_text}']"))
        )
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on: {button_text}")
    except Exception as e:
        print(f"Error al hacer clic en '{button_text}': {str(e)}")

def extract_elements_between_categories(driver, start_label="Películas", end_label="Series"):
    all_items = []
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        # Realizar scroll hacia abajo para cargar más contenido
        scroll_down(driver, steps=5, delay=0.5)
        
        # Esperar un momento para que el contenido se cargue
        time.sleep(2)
        
        # Intentar encontrar el inicio y fin de la sección
        start_element = driver.find_elements(By.XPATH, f"//h3[text()='{start_label}']")
        end_element = driver.find_elements(By.XPATH, f"//h3[text()='{end_label}']")

        # Si se encuentra la sección de inicio, comenzar a extraer elementos
        if start_element:
            section_items = driver.find_elements(By.XPATH, f"//section[contains(@class, 'contentListRow-0-2-232 category')]")
            for item in section_items:
                # Asegúrate de que el elemento está entre las secciones que te interesan
                if item.location['y'] >= start_element[0].location['y'] and (not end_element or item.location['y'] < end_element[0].location['y']):
                    title_element = item.find_element(By.TAG_NAME, 'h4')
                    title = title_element.text
                    link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    all_items.append({'title': title, 'link': link})
        
        # Si se encuentra el elemento de fin, detener el scroll
        if end_element:
            scrolling = False
        
        # Comprobar si hemos llegado al final de la página
        new_position = driver.execute_script("return window.pageYOffset;")
        if new_position == last_position:
            scrolling = False
        last_position = new_position

    return all_items

# Función principal
def main():
    driver_path = 'chromedriver.exe'
    driver = setup_driver(driver_path)
    driver.get('https://pluto.tv')
    
    time.sleep(5)
    click_button_by_text(driver, 'On Demand')
    
    time.sleep(5)
    movie_init(driver)
    
    time.sleep(1)
    click_button_by_text(driver, "Películas")
    
    time.sleep(5)
    movie_peliculas(driver, "Películas")
    
    # Extraer elementos entre "Películas" y "Series"
    extracted_data = extract_elements_between_categories(driver)
    
    # Mostrar los elementos extraídos
    for item in extracted_data:
        print(f"Title: {item['title']}, Link: {item['link']}")
    
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
