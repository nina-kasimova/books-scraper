import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import re
import json
import asyncio
import aiohttp


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0"
}
#session = requests.Session()

# PASTE URL HERE
initial_url = "https://www.goodreads.com/list/show/100384.Most_Anticipated_Christian_Fiction_2017"
url = initial_url + "?page="


def is_next_page(parser):
    next_page = False
    pagination = parser.find('div', attrs={'class': 'pagination'})

    if pagination is None:
        next_page = False
    else:
        disabled = pagination.find('span', attrs={'class': 'next_page disabled'})
        if disabled is None:
            next_page = True

    return next_page


async def fetch_page(session, url):
    async with session.get(url) as response:
        content = await response.text()
        print("fetched url", url)
        return content


async def fetch_all_pages(session, urls):
    tasks = [fetch_page(session, url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


def get_pages_urls(content):
    page = 0
    next_page = True
    count = 0
    all_urls = [url]
    pagination = content.find('div', attrs={'class': 'pagination'})

    pages_count = pagination.find_all('a')
    # Extract page numbers
    pages = set()  # Use a set to avoid duplicates
    for link in pages_count:
        if 'next_page' not in link.get('class', []):  # Skip 'Next' button
            href = link['href']
            match = re.search(r'page=(\d+)', href)  # Extract the page number
            if match:
                pages.add(int(match.group(1)))  # Add page number to the set

    # Convert to sorted list
    pages = sorted(pages)

    for i in range(1,max(pages)):
        all_urls.append(url + str(i))

    return all_urls


async def collect_all_books(session, books_info):
    count = 0

    content = await fetch_page(session, url)
    content = BeautifulSoup(content, 'lxml')
    all_urls = get_pages_urls(content)

    all_pages_content = await fetch_all_pages(session, all_urls)
    for page_content in all_pages_content:
        content = BeautifulSoup(page_content, 'lxml')

        books = content.find_all('tr', attrs={'itemtype': 'http://schema.org/Book'})
        list_name = content.find('h1', attrs={'class': 'gr-h1 gr-h1--serif'}).text
        books_info['list_name'] = list_name

        book_detail_tasks = []
        for book in books:
            print("{}.".format(count))
            count += 1

            books_info['book_title'].append(getTitle(book))
            print(getTitle(book))
            books_info['author'].append(getAuthor(book))
            avg_rating, review_count = getRatings(book)
            books_info['avg_rating'].append(avg_rating)
            books_info['review_count'].append(review_count)

            book_url = "https://www.goodreads.com" + (getLink(book))
            books_info['url'].append(book_url)

            book_detail_tasks.append(fetch_book_details(session, book_url))

        book_details = await asyncio.gather(*book_detail_tasks)
        for book_detail in book_details:
            book_content = BeautifulSoup(book_detail, 'lxml')
            books_info['description'].append(getDescription(book_content))
            books_info['reviews'].append(getReviews(book_content))
            books_info['shelves'].append(getShelves(book_content))
            # books_info['genres'].append(getGenres(book_content))

    return books_info


async def fetch_book_details(session, url):
    async with session.get(url, headers=headers) as response:
        book_content = await response.text()

        return book_content


def getTitle(book):
    book_title = book.find('a', attrs={'class': 'bookTitle'}).text
    return book_title.strip()


def getAuthor(book):
    author = book.find('a', attrs={'class': 'authorName'}).span.text
    return author


def getRatings(book):
    ratings = book.find('span', attrs={'class': 'minirating'}).text
    numbers = re.findall(r'\d+', ratings)
    avg_rating = float(numbers[0] + '.' + numbers[1])
    review_count = ''
    for i in numbers[2:]:
        review_count += i
    review_count = int(review_count)
    return avg_rating, review_count


def getShelves(book):
    reviews = book.find_all('div', {'class': 'friendReviews elementListBrown'})
    shelves = []
    for r in reviews:
        one_shelves = r.find_all('a', {'class': 'actionLinkLite'})
        for s in one_shelves:
            shelves.append(s.text)

    return shelves


def getReviews(book):
    reviews = book.find_all('div', {'class': 'friendReviews elementListBrown'})
    all_reviews = []
    for r in reviews:
        one_text = r.find('div', {'class': 'reviewText stacked'}).text
        all_reviews.append(cleanText(one_text))
    return all_reviews


def cleanText(s):
    return s.strip().replace("...more",".").replace("\n","").replace('\\','')


def getDescription(book):
    try:
        description = book.find('div', {'id': 'description'}).text
        return description.strip().replace('\n', '').replace('...more', '')
    except AttributeError:
        return []


def getLink(book):
    url = book.find('a', attrs={'class': 'bookTitle'})['href']
    return url


def get_file_name(name):
    # convert to lower case, add _ instead of spaces and remove numbers
    name = name.lower()
    valid_file_name = re.sub(r"[^\w\s]", '', name)
    valid_file_name = re.sub(r"\s+", '-', valid_file_name)
    valid_file_name = valid_file_name[:-1] + '.json'
    return valid_file_name


async def main():
    page = 0
    books = defaultdict(list)

    async with aiohttp.ClientSession() as session:
        books = await collect_all_books(session,books)

    books_table = pd.DataFrame(books)
    books_table['id'] = books_table.index

    file = books_table.to_json("data.json", orient="records")

    # open exported file and copy the data
    with open('../goodreads-data/data.json', 'r') as f:
        data = json.load(f)

    filename = get_file_name(books['list_name'])

    # correct the downloaded json to fit the json server format (add the object name)
    # this final file can be copied into db.json in the server folder for the UI
    with open("../goodreads-data/" + filename, 'w') as f:
        new_data = {'books': data}
        json.dump(new_data, f)

    with open('../../../web/ui-data/books-list.json', 'w') as f:
        new_data = {'books': data}
        json.dump(new_data, f)

if __name__ == "__main__":
    asyncio.run(main())
