from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def save_page_content(url, output_file):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        html = driver.page_source

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html)
        
        print(f"Contenido guardado en {output_file}")

    except Exception as e:
        print(f"Error al procesar la URL: {url}")
        print(str(e))

    finally:
        driver.quit()

if __name__ == "__main__":
    urls = [
        "https://pluto.tv/latam/on-demand/618da9791add6600071d68b0/669eb36efe11e500084757fb?lang=en",
    ]

    for index, url in enumerate(urls):
        output_file = f"pluto_page_{index + 1}.html"
        save_page_content(url, output_file)
