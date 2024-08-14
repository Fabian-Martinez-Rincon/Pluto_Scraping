from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://pluto.tv/latam/on-demand?lang=en")

    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/section/div[3]/div[3]')))

    element.click()

    time.sleep(2)

    body = driver.find_element(By.TAG_NAME, 'body')
    for i in range(10): 
        print(i)
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.2)

    print("Clic y scroll completados con éxito")
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/div[1]/span')))
    element.click()
    body = driver.find_element(By.TAG_NAME, 'body')
    for i in range(500): 
        print(i)
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.01) 

except Exception as e:
    print(f"Se produjo un error: {e}")

finally:
    driver.quit()


