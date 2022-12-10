from gensim.models import Nmf
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.test.utils import datapath

NUM_TOPICS = 2

# dataset = api.load("text8")
# dct = Dictionary(dataset)  # fit dictionary
# # corpus = [dct.doc2bow(line) for line in dataset]  # convert corpus to BoW format

# # print(type(dct))

# count = 0
# for id, word in dct:
#   print("**************              **************")
#   print()
#   print()
#   print(f'{id}: {word}')
#   if count > 10:
#     break

texts = [['human', 'interface', 'computer']]
dct = Dictionary(texts)  # initialize a Dictionary
# add more document (extend the vocabulary)
dct.add_documents([["cat", "say", "meow"], ["dog"]])
train_set = ["dog", "cat", "bark"], ["human", "interface",
                                     "computer", "design"], ["bark", "dog", "says"]
corpus = [dct.doc2bow(doc) for doc in train_set]
nmf = Nmf(corpus, num_topics=NUM_TOPICS, id2word=dct)

print("ID TO WORD")
for x in nmf.id2word.iteritems():
  print(x)

# print("TOPICS")
# for x in nmf.show_topics():
#   print(x)

print()
print("TOPIC TERMS")
for x in range(NUM_TOPICS):
  print(f'TOPIC {x}')
  for term in nmf.show_topic(x, topn=4):
    print(term)
  print()
