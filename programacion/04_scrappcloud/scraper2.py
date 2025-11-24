import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def init_driver(headless=True):
    chrome_opts = Options()
    if headless:
        chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--window-size=1920,1080")

    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome(options=chrome_opts)
    
    #service = Service(ChromeDriverManager(version="latest").install())
    #driver = webdriver.Chrome(service=service, options=chrome_opts)
    return driver

def scrape_public_page(page_url, max_scrolls=20, wait_time=4):
    driver = init_driver()
    driver.get(page_url)
    time.sleep(wait_time)

    posts_data = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolls):
        # 🔽 Baja hasta el final
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time+2)

        # 🟢 Busca todos los posts actualmente cargados
        articles = driver.find_elements(By.XPATH, "//div[@role='article']")

        print(f"[Scroll {i+1}] Se encontraron {len(articles)} artículos visibles.")

        for art in articles:
            try:
                # Expande "See more"/"Ver más" si existe
                see_more_buttons = art.find_elements(
                    By.XPATH,
                    ".//div[@role='button' and (text()='See more' or text()='Ver más' or text()='Mostrar más')]"
                )
                for btn in see_more_buttons:
                    try:
                        driver.execute_script("arguments[0].click();", btn)
                        time.sleep(0.3)
                    except:
                        pass

                # Extrae texto principal del post
                text_els = art.find_elements(By.XPATH, ".//div[@data-ad-preview='message']")
                for t in text_els:
                    text = t.text.strip()
                    if len(text) > 30:  # evita textos vacíos o cortos
                        posts_data.add(text)

            except Exception as e:
                continue

        # Verifica si ya no hay más contenido
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("⚠️ No se cargó más contenido, deteniendo scroll.")
            break
        last_height = new_height

    driver.quit()
    return list(posts_data)

def save_to_csv(posts, filename="fb_posts.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Post"])
        for post in posts:
            writer.writerow([post])
    print(f"✅ Saved {len(posts)} posts to {filename}")

if __name__ == "__main__":
    # Ejemplo: una página pública (puedes cambiar esta URL)
    urls = [
        "https://www.facebook.com/1aplanamx",
        "https://www.facebook.com/emprendedorpoliticomx",
        "https://www.facebook.com/LaVozdeMichoacan",
        "https://www.facebook.com/lanotarojamich",
        "https://www.facebook.com/agenciamich",
        "https://www.facebook.com/groups/2406893716312968",
        "https://www.facebook.com/agenciacomunicaciongrafica"
    ]
    for url in urls:
        #url = "https://www.facebook.com/1aplanamx"  # ejemplo de página institucional pública
        posts = scrape_public_page(url, max_scrolls=1900, wait_time=170)
        for i, post in enumerate(posts, 1):
            print(f"\nPOST #{i}\n{post[:400]}...\n{'-'*60}")
        save_to_csv(posts, filename=f"./fb_scraping/{url.split('/')[3]}.txt")

