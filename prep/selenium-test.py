from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
import time
from bs4 import BeautifulSoup

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

# Function to add random delay
def random_delay():
    time.sleep(random.uniform(2, 5))

try:
    # Navigate to the website
    url = 'https://www.newbalance.co.uk/women/shoes/#'
    driver.get(url)

    # Wait for the page to load completely
    random_delay()

    # Get the rendered HTML content
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    print("soup", soup)

    # Continue with your data extraction
    products = soup.find_all('div', class_='product-container')
    product_data = []

    for product in products:
        name = product.find('div', class_='product-name').text.strip()
        price = product.find('div', class_='product-price').text.strip()
        rating = product.find('div', class_='rating').text.strip() if product.find('div', class_='rating') else 'No rating'
        reviews = product.find('div', class_='reviews').text.strip() if product.find('div', class_='reviews') else 'No reviews'
        product_url = product.find('a', class_='product-link')['href']
        image_url = product.find('img', class_='product-image')['src']
        product_id = product['data-product-id']

        product_data.append({
            'name': name,
            'price': price,
            'rating': rating,
            'reviews': reviews,
            'product_url': product_url,
            'image_url': image_url,
            'product_id': product_id
        })

    df = pd.DataFrame(product_data)
    df.to_csv('new_balance_women_shoes.csv', index=False)

    print("Data saved to new_balance_women_shoes.csv")
finally:
    driver.quit()
