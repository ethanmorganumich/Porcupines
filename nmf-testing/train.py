import os
from gensim import corpora
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import Nmf


corpus = []

STOPWORDS = set(stopwords.words('english'))
STOPWORDS.add("also")
STOPWORDS.add("however")
STOPWORDS.add("in")
STOPWORDS.add("depends")
STOPWORDS.add("depend")

# for every file in the training-data folder, read the file and add to a list called corpus
for filename in os.listdir("training-data/set-1/"):
  with open("training-data/set-1/" + filename, "r") as f:
    corpus.append(f.read())

# lemmatize each word in the corpus
# LEMMATIZATION
# Stemming with lemmatization to get proper meaning words after stemming
# Create obj of Lemmatizer
lemmmatizer = WordNetLemmatizer()

for i in range(len(corpus)):
  words = word_tokenize(corpus[i])

  # List comprehension
  words = [lemmmatizer.lemmatize(
      word.lower()) for word in words]

  # remove all words that are in STOPWORDS from words
  words = [w for w in words if not w in STOPWORDS]

  corpus[i] = ' '.join(words)
# print(corpus)

# make the corpus into a document-term frequency matrix
doc_tokenized = [simple_preprocess(doc) for doc in corpus]
dictionary = corpora.Dictionary(doc_tokenized)
print(dictionary)
BoW_corpus = [dictionary.doc2bow(doc, allow_update=True)
              for doc in doc_tokenized]
print(dictionary)

# for doc in BoW_corpus:
#     print([[dictionary[id], freq] for id, freq in doc])

nmf = Nmf(BoW_corpus, num_topics=10, id2word=dictionary)

test_doc = ""
with open("testing-data/set-1/" + "Ancient Rome.md", "r") as f:
  test_doc = f.read()

test_doc = word_tokenize(test_doc)
# List comprehension
words = [lemmmatizer.lemmatize(
    word.lower()) for word in test_doc if word not in set(stopwords.words('english'))]
test_doc = ' '.join(words)

test_bow_corpus = dictionary.doc2bow(
    simple_preprocess(test_doc), allow_update=False)

vector = nmf[test_bow_corpus]

# TODO figure out what is actually in the vector
print(vector)
for topic in vector:
  print(topic)
  nmf.show_topic(topic[0])

print()
print()
print("----------- ALL TOPICS -----------")
print()

for topic in nmf.print_topics():
  print(topic)
