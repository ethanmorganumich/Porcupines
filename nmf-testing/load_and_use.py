from gensim.models import Nmf
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.test.utils import datapath
import time


startTime = time.time()
dataset = api.load("text8")
print("load dataset:", time.time() - startTime)

startTime = time.time()
dct = Dictionary(dataset)  # fit dictionary
print("load dct of dataset:", time.time() - startTime)

startTime = time.time()
temp_file = datapath("model")
nmf = Nmf.load(temp_file)
print("nmf.load:", time.time() - startTime)

other_texts = [
    ['computer', 'time', 'graph'],
    ['survey', 'response', 'eps'],
    ['human', 'system', 'computer']
]
other_corpus = [dct.doc2bow(text) for text in other_texts]
for text in other_texts:
    print(dct.doc2bow(text))
print(other_corpus)

unseen_doc = other_corpus[0]
vector = nmf[unseen_doc]
print(vector)
for identity, stat in vector:
    print(f"{dct[identity]}: {stat}")

unseen_doc = other_corpus[1]
vector = nmf[unseen_doc]
print(vector)
for identity, stat in vector:
    print(f"{dct[identity]}: {stat}")

unseen_doc = other_corpus[2]
vector = nmf[unseen_doc]
print(vector)
for identity, stat in vector:
    print(f"{dct[identity]}: {stat}")
