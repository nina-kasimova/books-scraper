import re
import time
import json
from playwright.sync_api import sync_playwright


def handle_response(response):
    if "products" in response.url:
        try:
            json_response = response.json()
            file_path = "response_data.json"

            # Read existing data from file
            try:
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                existing_data = []

            # Append new data
            existing_data.append(json_response)

            # Write updated data back to file
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)

            print("JSON response appended to response_data.json")
        except Exception as e:
            print(f"Error processing response from {response.url}: {e}")


def scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size(
            {
                "width":1280,
                "height": 1080
            }
        )
        page.on("response", lambda response: handle_response(response))

        page.goto("https://www.nike.com/gb/w/shoes-y7ok")
        time.sleep(2)
        if page.is_visible(".dialog-backdrop-container"):
            page.click(".dialog-actions-accept-btn")
        time.sleep(5)
        page.wait_for_load_state("networkidle")

        for i in range(5):  # make the range as long as needed
            page.mouse.wheel(0, 15000)
            time.sleep(2)
        browser.close()


if __name__=='__main__':


    with open("response_data.json") as f:
        data = json.load(f)
        products = data[0]['hydratedProducts']
    
    print(len(products))
    for p in products:
        print(p)
    # Process the data
    # for entry in data:
    #     for product in entry.get('products', []):
    #         print({
    #             "title": product.get('title'),
    #             "rating": product.get('rating'),
    #             # Add other fields as needed
    #         })