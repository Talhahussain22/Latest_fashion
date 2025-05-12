import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import time
import datetime
import warnings
from pathlib import Path

warnings.simplefilter("ignore", category=ResourceWarning)

urls = [
    "https://m.flipkart.com/search?q=men%27s+trousers",
    "https://m.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy",
    "https://m.flipkart.com/clothing-and-accessories/topwear/shirt/men-shirt/casual-shirt/pr?sid=clo,ash,axc,mmk,kp7",
    "https://m.flipkart.com/clothing-and-accessories/bottomwear/jeans/men-jeans/pr?sid=clo,vua,k58,i51",
]

def scrape_flipkart_selenium(urls, limit=150):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    products = []
    seen_ids = set()

    try:
        for url in urls:
            driver.get(url)
            time.sleep(5)  

            cards = driver.find_elements(By.XPATH, "//div[@data-id]")
            for card in cards:
                try:
                    product_id = card.get_attribute("data-id")
                    if product_id in seen_ids:
                        continue

                    img = card.find_element(By.TAG_NAME, "img")
                    image_url = img.get_attribute("src") or img.get_attribute("data-src")
                    if image_url:
                        products.append({
                            "product_id": product_id,
                            "image_url": image_url,
                            "timestamp": datetime.datetime.now().isoformat()
                        })
                        seen_ids.add(product_id)

                    if len(products) >= limit:
                        break
                except Exception:
                    continue

            if len(products) >= limit:
                break

            time.sleep(3)
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error during Selenium cleanup: {e}")
        finally:
            driver.stop_client() 

    return products

all_path = Path("all_products.json")
all_data = []

if all_path.exists():
    with open(all_path, "r") as f:
        all_data = json.load(f)["products"]

new_products = scrape_flipkart_selenium(urls, limit=150)

all_data.extend(new_products)

with open("all_products.json", "w") as f:
    json.dump({"products": all_data}, f, indent=4)

with open("latest_batch.json", "w") as f:
    json.dump({"products": new_products}, f, indent=4)

print(f"Scraped and saved {len(new_products)} new products!")
