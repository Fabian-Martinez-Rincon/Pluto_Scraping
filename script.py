from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


def movie_init():
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/section/div[3]/div[3]')))

    element.click()

    time.sleep(2)

    body = driver.find_element(By.TAG_NAME, 'body')
    for i in range(10): 
        print(i)
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.2)


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
    driver.find_element(By.LINK_TEXT, 'On Demand').click()
    time.sleep(5)
    click_button_by_text(driver, "Películas")
    time.sleep(5)

    driver.quit()

if __name__ == "__main__":
    main()
