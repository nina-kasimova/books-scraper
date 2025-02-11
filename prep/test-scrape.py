from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time

# Path to your ChromeDriver
chrome_driver_path = '/Users/nina/Desktop/py/chromedriver-mac-x64/chromedriver'

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode for efficiency
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Create a service object and pass it to the Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)


# Function to scroll and load more products
def load_all_products(driver):
    SCROLL_PAUSE_TIME = 2
    products_loaded = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("SCROLL\n")
        if new_height == last_height:
            break
        last_height = new_height

try:
    # Navigate to the website
    url = 'https://www.nike.com/gb/w/shoes-y7ok'
    driver.get(url)

    # Wait for the initial products to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-card')))
    load_all_products(driver)

    # Get the rendered HTML content
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    # Find all product cards
    products = soup.find_all('div', attrs={'data-testid': 'product-card'})

    product_data = []
    print("NEW DATA \n")
    print(products)
    print(len(products))

    for product in products:
        # Extract product name
        name_tag = product.find('div', class_='product-card__title')
        name = name_tag.text.strip() if name_tag else 'No name'

        # Extract product price
        price_tag = product.find('div', class_='product-price')
        price = price_tag.text.strip() if price_tag else 'No price'

        # Extract product URL
        url_tag = product.find('a', class_='product-card__link-overlay')
        product_url = url_tag['href'] if url_tag else 'No URL'

        # Extract product image URL
        img_tag = product.find('img', class_='product-card__hero-image')
        image_url = img_tag['src'] if img_tag else 'No image URL'

        # Append extracted data to list
        product_data.append({
            'name': name,
            'price': price,
            'product_url': product_url,
            'image_url': image_url
        })

    # Create DataFrame and save to CSV
    df = pd.DataFrame(product_data)
    df.to_csv('nike_shoes.csv', index=False)

    print("Data saved to nike_shoes.csv")
finally:
    driver.quit()
