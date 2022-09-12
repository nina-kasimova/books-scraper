import pandas as pd
import nltk
from collections import Counter


def get_first_review(file):
    df = pd.read_csv(file)
    reviews = df.reviews.tolist()
    return reviews[0]


# reviews for specified books
def get_reviews(file, start, end):
    df = pd.read_json(file)
    reviews = df.reviews
    return reviews[start:end].tolist()


def get_tokens(text):
    # get rid of list, use string
    tokens = nltk.word_tokenize(text[0])
    return tokens


def tag_words(text):
    tokens = get_tokens(text)
    tagged = nltk.pos_tag(tokens)
    return tagged


# NN - nouns, JJ - adjectives, NNP doesnt really work
def get_part_of_speech(abbreviation, text):
    tagged = tag_words(text)
    filtered_tagged = [t for t in tagged if t[1] == abbreviation]
    return filtered_tagged


# remove the abbreviation from the tuple eg NN
def clean_tagged_text(tagged):
    only_words = []
    for n in tagged:
        only_words.append(n[0])
    return only_words


def get_frequency(tagged_words):
    only_words = clean_tagged_text(tagged_words)
    return Counter(only_words).most_common(len(only_words))


if __name__ == '__main__':

    example_file = '/Users/nina/Desktop/py/books-scraper/data.json'
    example_text = get_reviews(example_file, 1, 5)
    for r in example_text:
        if r:
            frequency_of_nouns = get_frequency(get_part_of_speech('NN', r))
            print(frequency_of_nouns)
