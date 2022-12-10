# This is the file version which is uploaded to the cloud function via zip file
from gensim.models import Nmf
from gensim.corpora import Dictionary
from google.cloud import storage
from nltk import data
import re
from nltk.stem import WordNetLemmatizer
import json

# Instantiates a storage client
storage_client = storage.Client()

# Enables nltk to look for data in /nltk_data
data.path.append('./nltk_data')


def load_and_use_model(request):
  """Responds to any HTTP request.
  Args:
      request (flask.Request): HTTP request object.
  Returns:
      The response text or any set of values that can be turned into a
      Response object using
      `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
  """
  request_json = request.get_json()
  if 'note_text' in request_json:
    nmf, dct = load_model()

    # Create list of tags associated with each topic
    TOPICS_TO_TAGS = []
    for topic in nmf.show_topics(num_topics=50, num_words=2, formatted=False):
      # Example topic looks like:
      # (0, [('new', 0.04927730786772849), ('york', 0.045536340221838695), ('city', 0.03610552021069998), ('state', 0.022837394513592096), ('manhattan', 0.02158441764544512), ('world', 0.015081501532756553), ('united', 0.014942394226562994), ('computer', 0.014220414818740834), ('central', 0.013146910359001075), ('national', 0.012290741830119386)])
      TOPICS_TO_TAGS.append(topic[1][0][0])

    # Get tags for new document (note_text)
    doc = dct.doc2bow(clean_text(request_json['note_text']))
    prediction = nmf[doc]
    tags = []
    for topic in prediction:
      if topic[1] > 0.15:
        tags.append((TOPICS_TO_TAGS[topic[0]], topic[1]))
    return json.dumps(tags), 200, {"Content-Type": "application/json"}

  return json.dumps({"error": "no note_text in request"}), 400, {"Content-Type": "application/json"}


def load_model():
  # load model and dictionary from uploaded files
  nmf = Nmf.load('./nlp_store/model')
  dct = Dictionary.load('./nlp_store/dictionary')
  return nmf, dct


def load_stopwords():
  # Get stopwords from uploaded file
  with open('./nltk_data/corpora/stopwords/english', 'r') as f:
    STOPWORDS = set(f.read().split("\n"))
    STOPWORDS.add("also")
    STOPWORDS.add("however")
    STOPWORDS.add("in")
    STOPWORDS.add("depends")
    STOPWORDS.add("depend")
    STOPWORDS.add("")
    STOPWORDS.add("wa")
    return STOPWORDS


def remove_all_symbols(text: str) -> str:
  text = re.sub("http[s]?\://\S+", "", text)  # remove urls
  text = re.sub(r"[0-9]", "", text)  # remove numbers
  text = re.sub(r"\n", " ", text)  # remove newlines
  text = re.sub('\s+', ' ', text)  # remove extra spaces
  text = re.sub("[^a-zA-Z ]+", " ", text)  # remove all punctuation
  return text


def clean_text(text_str: str) -> list:
  STOPWORDS = load_stopwords()

  text_str = remove_all_symbols(text_str)
  words = text_str.split(" ")

  lemmmatizer = WordNetLemmatizer()
  words = [lemmmatizer.lemmatize(word.lower()) for word in words]

  # remove all words that are in STOPWORDS from words
  words = [w for w in words if not w in STOPWORDS]
  return words
