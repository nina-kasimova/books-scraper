import nltk
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re
from nltk import FreqDist
from nltk.tag import pos_tag


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:

        yield dict([token, True] for token in tweet_tokens)


def remove_noise(tweet_tokens, stop_words = ()):

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


if __name__ == '__main__':
    # sentences
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    # sentences split into words
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')

    stop_words = stopwords.words('english')
    positive_cleaned_tokens_list = []
    # go through the list of words and clean them off punctuation etc
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    # will iterate over each words and add a True to make it into a dictionary
    # each element of the list will be a key value pair
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)

    # yield each such pair
    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    # each sentence will be assigned a label
    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    train_data = positive_dataset[:700]
    # print(positive_tokens_for_model)
    print(positive_dataset[:5])

