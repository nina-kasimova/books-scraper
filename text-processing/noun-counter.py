import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from nltk import RegexpChunkParser

df = pd.read_csv('/Users/nina/Desktop/py/goodreads/books_info.csv')
all_reviews = df.reviews.tolist()
words = set(nltk.corpus.words.words())
# filter out non english words
first_book = "".join(w for w in all_reviews[0] if w.lower() in words or not w.isalpha())

# removes punctuation
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(first_book)

# tagging nouns adjectives etc
tagged = nltk.pos_tag(tokens)
nouns = [t for t in tagged if t[1] == 'NN']

only_nouns = []
for n in nouns:
    only_nouns.append(n[0])

print(Counter(only_nouns).most_common(len(only_nouns)))