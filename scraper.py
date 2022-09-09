import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import re
import json

session = requests.Session()

# PASTE URL HERE
initial_url = "https://www.goodreads.com/list/show/7023.Best_books_about_Solitude_fiction_"
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


def collect_all_books(books_info):
    page = 0
    next_page = True
    count = 0
    while next_page and page < 1:
        page += 1
        url_page = url + str(page)
        content = session.get(url).content
        content = content.decode("utf-8")
        parse = BeautifulSoup(content, 'lxml')

        next_page = is_next_page(parse)
        books = parse.find_all('tr', attrs={'itemtype': 'http://schema.org/Book'})
        list_name = parse.find('h1', attrs={'class': 'gr-h1 gr-h1--serif'}).text
        books_info['list_name'] = list_name

        for book in books:
            print("{}.".format(count))
            count += 1
            one_url = "https://www.goodreads.com/" + getLink(book)
            one_content = requests.get(one_url).content
            one_parse = BeautifulSoup(one_content, 'lxml')
            books_info['book_title'].append(getTitle(book))
            books_info['author'].append(getAuthor(book))
            avg_rating, review_count = getRatings(book)
            books_info['avg_rating'].append(avg_rating)
            books_info['review_count'].append(review_count)
            books_info['url'].append((getLink(book)))

            book_url = "https://www.goodreads.com"+(getLink(book))
            one_content = requests.get(book_url).content
            one_content = one_content.decode("utf-8")
            book_content = BeautifulSoup(one_content, 'lxml')
            books_info['description'].append(getDescription(book_content))
            books_info['reviews'].append(getReviews(book_content))
            books_info['shelves'].append(getShelves(book_content))
            # books_info['genres'].append(getGenres(book_content))
            print(getTitle(book))

    return books_info


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


if __name__ == "__main__":

    page = 0
    books = defaultdict(list)

    books = collect_all_books(books)

    books_table = pd.DataFrame(books)
    books_table['id'] = books_table.index

    file = books_table.to_json("data.json", orient="records")

    # open exported file and copy the data
    with open('data.json', 'r') as f:
        data = json.load(f)

    filename = get_file_name(books['list_name'])

    # correct the downloaded json to fit the json server format (add the object name)
    # this final file can be copied into db.json in the server folder for the UI
    with open("../goodreads-data/"+filename, 'w') as f:
        new_data = {'books': data}
        json.dump(new_data, f)

    with open('../../web/ui-data/books-list.json', 'w') as f:
        new_data = {'books': data}
        json.dump(new_data, f)
