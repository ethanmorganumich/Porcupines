from mediawiki import MediaWiki
import time
import os
import re
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim.corpora import Dictionary
from gensim.models import LdaModel, Phrases
from gensim.test.utils import datapath
from gensim.models.phrases import Phraser
import string

# gensim.corpora.TextCorpus -> plain text -> bow vectors
# https://tedboy.github.io/nlps/generated/generated/gensim.corpora.TextCorpus.html#gensim.corpora.TextCorpus
NUM_TOPICS = 30


def remove_all_symbols(text: str) -> str:
  text = re.sub("http[s]?\://\S+", "", text)  # remove urls
  text = re.sub(r"[0-9]", "", text)  # remove numbers
  text = re.sub(r"\n", " ", text)  # remove newlines
  text = re.sub("[^a-zA-Z ]+", " ", text)  # remove all punctuation
  text = re.sub('\s+', ' ', text)  # remove extra spaces
  text = re.sub(r"\b[a-zA-Z]{1,2}\b", "", text)  # remove 1-2 letter words
  return text


def clean_text(text_str: str) -> list:
  STOPWORDS = set(stopwords.words('english'))
  STOPWORDS.add("also")
  STOPWORDS.add("however")
  STOPWORDS.add("in")
  STOPWORDS.add("depends")
  STOPWORDS.add("depend")
  STOPWORDS.add("")
  STOPWORDS.add("wa")

  text_str = remove_all_symbols(text_str)
  words = text_str.split(" ")
  # words = simple_preprocess(text_str)
  # words = word_tokenize(text_str)

  lemmmatizer = WordNetLemmatizer()
  words = [lemmmatizer.lemmatize(word.lower()) for word in words]

  # remove all words that are in STOPWORDS from words
  words = [w for w in words if not w in STOPWORDS]
  return words


# read files from training-data/set-2 and create a corpus
corpus = []
for file_name in os.listdir('../set-3'):
  with open(f'../set-3/{file_name}', 'r') as f:
    print(file_name)
    file = f.read()
    # 0 -> categories, 1 -> title, 2 -> summary
    # file = file.split("||||||\n")
    # categories = file[0][:-2].split("~")  # into list
    # title = file[1][:-1]  # removing \n
    # summary = file[2]

    file_words = clean_text(file)
    # higher threshold fewer phrases.
    bigram = Phrases(file_words, min_count=5, threshold=100)
    bigram_mod = Phraser(bigram)
    corpus.append(file_words)

# Train nmf model from the corpus
dct = Dictionary(corpus)
BoW_corpus = [dct.doc2bow(doc, allow_update=True)
              for doc in corpus]
nmf = LdaModel(BoW_corpus, num_topics=NUM_TOPICS, id2word=dct)

print("TOPIC TERMS")
for x in range(NUM_TOPICS):
  print(f'TOPIC {x}')
  for term in nmf.show_topic(x, topn=7):
    print(term)
  print()

temp_file = datapath("model")
print(temp_file)
nmf.save(temp_file)
