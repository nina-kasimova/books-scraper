from playwright.sync_api import sync_playwright


def scrape_imdb_top_250():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://m.imdb.com/chart/top/')

        # Wait for the page to load the required elements
        page.wait_for_selector('h4')

        # Extract data
        movies = page.query_selector_all('.lister-item.mode-detail')

        top_250_movies = []
        for movie in movies:
            title = movie.query_selector('.lister-item-header a').inner_text()
            year = movie.query_selector('.lister-item-year').inner_text()
            rating = movie.query_selector('.ipl-rating-star__rating').inner_text()
            top_250_movies.append({
                'title': title,
                'year': year,
                'rating': rating
            })

        browser.close()

        return top_250_movies


if __name__ == "__main__":
    top_250 = scrape_imdb_top_250()
    for movie in top_250:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
