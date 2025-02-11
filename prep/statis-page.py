import requests
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd


url = "https://m.imdb.com/chart/top/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"
}

response = requests.get(url, headers=headers)


def scrape_imdb():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set headless=False if you want to see the browser UI
        page = browser.new_page()

        # Open the IMDb Top 250 movies page
        url = "https://m.imdb.com/chart/top/"
        page.goto(url)
        time.sleep(2)
        # Wait for the content to load
        page.wait_for_load_state('networkidle')

        # Get the updated page source with all movies
        content = page.content()
        with open("html_content", 'w', encoding='utf-8') as file:
            file.write(content)
        # Close the browser
        browser.close()


def parse_html(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    all_movies = soup.find_all("div",attrs={"class": "sc-b189961a-0 hBZnfJ cli-children"})

    movie_list = []
    for movie in all_movies:
        # print(movie.prettify(), '\n')
        try:
            title_element = movie.find("h3", attrs={'class':"ipc-title__text"})
            title = title_element.text.split('.')[1] if title_element else None
            year_element = movie.find_all("span", attrs={"class": "sc-b189961a-8 kLaxqf cli-title-metadata-item"})

            year = year_element[0].text if year_element else None
            rating_element = movie.find("span", attrs={"class":"ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"})
            rating = rating_element.text.split()[0] if rating_element else None
            age_restr = year_element[2].text if year_element else None

            movie_dict = {
                'title': title,
                'year': year,
                'rating': rating,
                'age_restr': age_restr
            }

            # Append the dictionary to the list
            movie_list.append(movie_dict)
        except Exception as e:
            print(f"Error occured while parsing: {e}")
    return movie_list


if __name__=='__main__':
    result = parse_html('html_content')
    movies_df = pd.DataFrame(result)
    movies_df.index = movies_df.index +1
    print(movies_df)
    movies_df.to_csv("imdb-top.csv",index_label='Index')







