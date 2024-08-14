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
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/section/div[3]/div[3]')))
    element.click()
    body = driver.find_element(By.TAG_NAME, 'body')
    for i in range(15): 
        print(i)
        body.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.01)

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
    movie_init(driver)
    time.sleep(1)
    click_button_by_text(driver, "Películas")
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/section/div/div/div/div/section[3]/span/div/div[1]/span/a').click()
    time.sleep(5)
    
    button_xpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div[1]/div/div[1]/div/button'
    
    buttons = click_button_and_get_nav_items(driver, button_xpath)
    for button in buttons:
        print(f"Text: {button['text']}, Link: {button['href']}")
        
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
