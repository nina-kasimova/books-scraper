import re
from nltk import FreqDist
import pandas as pd
import nltk
from collections import Counter
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pickle


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
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text[0])
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


# normalise the words (be instead of being, book instead of books)
def lemmatise_sentence(tokens):
    lemmatiser = WordNetLemmatizer()
    lemmatised_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatised_sentence.append(lemmatiser.lemmatize(word, pos))
    return lemmatised_sentence


def clean_text(words):
    stop_words = stopwords.words('english')
    cleaned_tokens = []
    for token, tag in tag_words(words):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@'\w'+)", "", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(words) > 0 and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


if __name__ == '__main__':

    example_file = '/Users/nina/Desktop/py/books-scraper/data.json'
    example_text = get_reviews(example_file, 1, 5)

    with open('/Users/nina/Desktop/datasets/naive_bayes_classifier1.pkl', 'rb') as fid:
        classifier_loaded = pickle.load(fid)
    for r in example_text:
        if r:
            count = 0
            for one in r:
                # print(len(one))
                example_tokens = get_tokens(one)
                clean = clean_text(one)
                print(count, ": ", one)
                print(classifier_loaded.classify(dict([token, True] for token in clean)))
                print("--------------------------")
                count += 1


