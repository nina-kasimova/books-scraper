import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk import RegexpParser
import nltk
from collections import Counter


def get_first_review():
    df = pd.read_csv('/Users/nina/Desktop/py/goodreads-data/books_info.csv')
    reviews = df.reviews.tolist()
    return reviews[0]


# reviews for specified books
def get_reviews(start, end):
    df = pd.read_csv('/Users/nina/Desktop/py/goodreads/books_info.csv')
    reviews = df.reviews.tolist()
    return reviews[start:end]


def tokenize(reviews):
    tokenizer = RegexpTokenizer(r'\w+')
    all_tokens = []
    for r in range(len(reviews)):
        tokens = tokenizer.tokenize(reviews[r])
        all_tokens.append(tokens)
    return all_tokens


def tag_words(tokens):
    tagged = []
    for t in range(len(tokens)):
        tag = nltk.pos_tag(tokens[t])
        tagged.append(tag)
    return tagged


# NN - nouns, JJ - adjectives, NNP doesnt really works
def get_part_of_speech(abbreviation, tagged):
    final = []
    for tag in range(len(tagged)):
        final.append([t for t in tagged[tag] if t[1] == abbreviation])

    return final


def clean_tagged(tagged):
    only_words = []
    for n in tagged:
        only_words.append(n[0])
    return only_words


def get_frequency(tagged_words):
    only_words = []
    for n in tagged_words:
        only_words.append(n[0])

    return Counter(only_words).most_common(len(only_words))


if __name__ == '__main__':
    print(tokenize(get_reviews(0, 1)))
