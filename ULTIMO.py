from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys

def movie_init(driver):
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/button/span/span')))
    element.click()
    # body = driver.find_element(By.TAG_NAME, 'body')
    # for i in range(15): 
    #     print(i)
    #     body.send_keys(Keys.ARROW_DOWN)
    #     time.sleep(0.1)

def is_button_selected(driver, button_text):
    try:
        # Verificar si el botón tiene la clase "selected"
        button = driver.find_element(By.XPATH, f"//span[text()='{button_text}']/ancestor::div[contains(@class, 'l2-category-atc')]")
        return "selected" in button.get_attribute("class")
    except Exception as e:
        print(f"Error verificando el estado del botón '{button_text}': {str(e)}")
        return False

def movie_peliculas(driver, button_text="Películas"):
    print("Clic y scroll completados con éxito")
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/div/span/span/h3')))
    element.click()
    body = driver.find_element(By.TAG_NAME, 'body')
    
    # Realizar scroll hasta que el botón no esté seleccionado
    while is_button_selected(driver, button_text):
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.01)
    
    print(f"El botón '{button_text}' ya no está seleccionado.")
    
    # Continuar con cualquier otra acción si es necesario
    # Por ejemplo, hacer clic en un elemento
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{button_text}']/ancestor::div[contains(@class, 'l2-category-atc')]"))
        )
        element.click()
    except Exception as e:
        print(f"Error al hacer clic en '{button_text}': {str(e)}")

def click_button_by_text(driver, button_text):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{button_text}']"))
        )
        ActionChains(driver).move_to_element(button).click().perform()
        print(f"Clicked on: {button_text}")
        
    except Exception as e:
        print(f"Error al hacer clic en '{button_text}': {str(e)}")

def main():
    driver_path = 'chromedriver.exe'
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://pluto.tv')
    time.sleep(5)
    movie_init(driver)
    time.sleep(1)
    movie_peliculas(driver, "Películas")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
