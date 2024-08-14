from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


def is_element_in_viewport(driver, element):
    element_location = element.location_once_scrolled_into_view
    window_height = driver.execute_script("return window.innerHeight")
    element_height = element.size['height'] 

    if element_location['y'] < 0 or element_location['y'] > window_height - element_height:
        return False
    return True

driver_path = 'chromedriver.exe'
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)
driver.get('https://pluto.tv')
time.sleep(5) 
driver.find_element(By.LINK_TEXT, 'On Demand').click()
time.sleep(1)

text_elements = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/section/div[2]/ul')
button_texts = [element.text for element in text_elements]
button_texts = button_texts[0].split('\n')
print(button_texts)

print("Lista de textos de botones:")
for text in button_texts:
    try:
        peliculas_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//span[text()='{text}']"))
        )
        if not is_element_in_viewport(driver, peliculas_button):
            driver.execute_script("arguments[0].scrollIntoView(true);", peliculas_button)
            ActionChains(driver).move_to_element(peliculas_button).perform()

        ActionChains(driver).move_to_element(peliculas_button).click().perform()
        print(f"Clicked on: {text}")
        time.sleep(1)
    except Exception as e:
        print(f"Error clicking on {text}: {str(e)}")

time.sleep(5)
driver.quit()
