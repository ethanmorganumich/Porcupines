# from gensim.models import Nmf
# import gensim.downloader as api
# from gensim.models import TfidfModel
# from gensim.corpora import Dictionary
# from gensim.test.utils import datapath
from mediawiki import MediaWiki
import os.path
import time
import random
from mediawiki import DisambiguationError

f = open("LIST_OF_PAGES.txt", "r")
LIST_OF_PAGES = f.read().split("\n")
wikipedia = MediaWiki(
  user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5")
wikipedia.rate_limit = True
# wikipedia.rate_limit_min_wait = 0.5
try:
  # for every page in LIST_OF_PAGES write the summary to a file
  for page_name in LIST_OF_PAGES:
    if os.path.isfile(f'../set-3/{page_name}.txt'):
      continue
    try:
      page = wikipedia.page(page_name)
      # Change set before running!
      if len(page.summary) < 2:
        LIST_OF_PAGES.remove(page_name)
        with open("LIST_OF_PAGES.txt", 'w') as f:
          f.write("\n".join(LIST_OF_PAGES))
      parsed_page_name = page_name.replace("/", "_")
      with open(f'../set-3/{parsed_page_name}.txt', 'w') as f:
        for category in page.categories:
          f.write(category + "~")
        f.write("\n||||||\n")
        f.write(f'{page.title}\n')
        f.write("||||||\n")
        f.write(page.summary)
    except DisambiguationError:
      LIST_OF_PAGES.remove(page_name)
      with open("LIST_OF_PAGES.txt", 'w') as f:
        f.write("\n".join(LIST_OF_PAGES))
    except Exception as e:
      print("error: ", str(e), " page_name: ", page_name)
except KeyboardInterrupt as ke:
  print("hello jke")
  with open("LIST_OF_PAGES.txt", 'w') as f:
    f.write("\n".join(LIST_OF_PAGES))

  # time.sleep(random.randInt(0.5, 5))
