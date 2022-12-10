from gensim.models import Nmf
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.test.utils import datapath

dataset = api.load("text8")

dct = Dictionary(dataset)  # fit dictionary
corpus = [dct.doc2bow(line) for line in dataset]  # convert corpus to BoW format
model = TfidfModel(corpus)  # fit model
vector = model[corpus[0]]

nmf = Nmf(corpus, num_topics=10)
temp_file = datapath("model")
print(temp_file)
nmf.save(temp_file)
