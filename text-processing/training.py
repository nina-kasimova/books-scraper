from nltk import classify
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
import random
from nltk.tag import pos_tag
from nltk import NaiveBayesClassifier
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import pickle


def get_tokens_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def remove_noise(tweet_tokens, stop_words=()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tokens(text):
    # get rid of list, use string
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens


if __name__ == '__main__':
    # read csv
    # tokenise the sentences
    # df = pd.read_csv('/Users/nina/Desktop/datasets/IMDB_dataset.csv', index_col=False)
    # df = df.reset_index(drop=True)
    # positive = df[df['sentiment'] == 'positive']
    # positive_reviews = positive.loc[:, 'review']
    #
    # negative = df[df['sentiment'] == 'negative']
    # negative_reviews = negative.loc[:, 'review']
    #
    # positive_tokens = []
    # for i in positive_reviews.iteritems():
    #     positive_tokens.append(get_tokens(i[1]))
    # negative_tokens = []
    # for i in negative_reviews.iteritems():
    #     negative_tokens.append(get_tokens(i[1]))
    #
    # # negative_tokens = negative_tokens[:10]
    # # positive_tokens = positive_tokens[:10]
    #
    # stop_words = stopwords.words('english')
    #
    # positive_cleaned_tokens_list = []
    # # go through the list of words and clean them off punctuation etc
    # for tokens in positive_tokens:
    #     positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
    # negative_cleaned_tokens_list = []
    # # go through the list of words and clean them off punctuation etc
    # for tokens in negative_tokens:
    #     negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
    #
    # positive_tokens_for_model = get_tokens_for_model(positive_cleaned_tokens_list)
    # negative_tokens_for_model = get_tokens_for_model(negative_cleaned_tokens_list)
    #
    # positive_dataset = [(tweet_dict, "Positive")
    #                     for tweet_dict in positive_tokens_for_model]
    # negative_dataset = [(tweet_dict, "Negative")
    #                     for tweet_dict in negative_tokens_for_model]
    #
    # dataset = positive_dataset + negative_dataset
    #
    # random.shuffle(dataset)
    #
    # dataset_train = dataset[:40000]
    # dataset_test = dataset[40000:]

    # classifier = NaiveBayesClassifier.train(dataset_train)
    #
    # with open('/Users/nina/Desktop/datasets/naive_bayes_classifier1.pkl', 'wb') as fid:
    #     pickle.dump(classifier, fid)

    with open('/Users/nina/Desktop/datasets/naive_bayes_classifier1.pkl', 'rb') as fid:
        classifier_loaded = pickle.load(fid)

    custom_review = "i really like this book"
    custom_tokens = remove_noise(get_tokens(custom_review))
    custom_tokens_for_model = get_tokens_for_model(custom_tokens)
    print(dict([token, True] for token in custom_tokens))
    # print(classifier_loaded.classify(dict([token, True] for token in custom_tokens)))

    # print("Accuracy is:", classify.accuracy(classifier_loaded, dataset_test))
    #
    # print(classifier_loaded.show_most_informative_features(10))
