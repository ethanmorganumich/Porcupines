# Author: Ethan Morgan
#        etcmo
from pydoc import doc
import re
import os
import sys
from porterStemmer import PorterStemmer

"""------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------------Remove Tags----------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------------------"""
# remove the <*+> or strings
# could use regex to remove this parts that match
# maybe remove all other tags except <text>
#input: string
#output: string


def removeSGML(input):
  pattern = r'<.*?>'
  return re.sub(pattern, '', input)


"""------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------------Tokenize Text--------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------------------"""


def tokenizeText(docString):
  """Function turns document string into good tokens 
  Parameters:
      docString (str): string of document
  Returns:
      tokens (list of str): tokens from the document
  """
  # regex
  # number with commas -> do not tokenize this
  #   number comma number -> one big number
  # Accroyn
  #   [Capital letter] ([.] [Capital Letter]) => () are recursed
  # Decimal Numbers
  #   number . number -> decimal number
  # Date
  #   number / number / number
  #       could do based on length of decimal
  #

  # expanded all contactions
  docString = expandContractions(docString)

  # get rid of all s' examples
  docString = re.sub(r"s'", '', docString)

  # combine all acroynms -> this was painful
  acron = re.search("([a-zA-Z]\.){2,}", docString)
  while (acron != None):
    for i in range(0, int((acron.end() - acron.start()) / 2)):
      docString = docString[0:(int(i + 1 + acron.start()))] + \
          docString[(int(i + 2 + acron.start())):]
    acron = re.search("([a-zA-Z]\.){2,}", docString)

  # split on any of these, creating the token list initially
  tokens = re.split(
    '(\.|,| |/|\?|\!|\;|\:|\"|\'|\[|\]|\(|\)|\<|\>|\n)', docString)

  # remove all ' ' and '' in token list
  for i, value in enumerate(tokens):
    while (i < len(tokens) and (tokens[i] == ' ' or tokens[i] == '' or tokens[i] == '\n')):
      tokens.pop(i)

  # combine dates and numbers in tokens
  tokens = combineDatesNums(tokens)
  return tokens


def expandContractions(docString):
  """Function looks at the docString and replaces all contractions with their longer versions
  Parameters:
      docString (str): string of document
  Returns:
      expanded docString (str): string with no more contractions
  """

  # Note this clever bit of code was written by alko and arturomp at this stackoverflow
  # https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
  contractions = {
      "ain't": "am not",
      "aren't": "are not",
      "can't": "cannot",
      "can't've": "cannot have",
      "'cause": "because",
      "could've": "could have",
      "couldn't": "could not",
      "couldn't've": "could not have",
      "didn't": "did not",
      "doesn't": "does not",
      "don't": "do not",
      "hadn't": "had not",
      "hadn't've": "had not have",
      "hasn't": "has not",
      "haven't": "have not",
      "he'd": "he had",
      "he'd've": "he would have",
      "he'll": "he will",
      "he'll've": "he will have",
      "he's": "he is",
      "how'd": "how did",
      "how'd'y": "how do you",
      "how'll": "how will",
      "how's": "how is",
      "I'd": "I had / I would",
      "I'd've": "I would have",
      "I'll": "I will",
      "I'll've": "I will have",
      "I'm": "I am",
      "I've": "I have",
      "isn't": "is not",
      "it'd": "it would",
      "it'd've": "it would have",
      "it'll": "it will",
      "it'll've": "it will have",
      "it's": "it is",
      "let's": "let us",
      "ma'am": "madam",
      "mayn't": "may not",
      "might've": "might have",
      "mightn't": "might not",
      "mightn't've": "might not have",
      "must've": "must have",
      "mustn't": "must not",
      "mustn't've": "must not have",
      "needn't": "need not",
      "needn't've": "need not have",
      "o'clock": "of the clock",
      "oughtn't": "ought not",
      "oughtn't've": "ought not have",
      "shan't": "shall not",
      "sha'n't": "shall not",
      "shan't've": "shall not have",
      "she'd": "she would",
      "she'd've": "she would have",
      "she'll": "she will",
      "she'll've": "she will have",
      "she's": "she has / she is",
      "should've": "should have",
      "shouldn't": "should not",
      "shouldn't've": "should not have",
      "so've": "so have",
      "so's": "so is",
      "that'd": "that would",
      "that'd've": "that would have",
      "that's": "that is",
      "there'd": "there would",
      "there'd've": "there would have",
      "there's": "there is",
      "they'd": "they would",
      "they'd've": "they would have",
      "they'll": "they will",
      "they'll've": "they will have",
      "they're": "they are",
      "they've": "they have",
      "to've": "to have",
      "wasn't": "was not",
      "we'd": "we would",
      "we'd've": "we would have",
      "we'll": "we will",
      "we'll've": "we will have",
      "we're": "we are",
      "we've": "we have",
      "weren't": "were not",
      "what'll": "what will",
      "what'll've": "what will have",
      "what're": "what are",
      "what's": "what is",
      "what've": "what have",
      "when's": "when is",
      "when've": "when have",
      "where'd": "where did",
      "where's": "where is",
      "where've": "where have",
      "who'll": "who will",
      "who'll've": "who will have",
      "who's": "who is",
      "who've": "who have",
      "why's": "why is",
      "why've": "why have",
      "will've": "will have",
      "won't": "will not",
      "won't've": "will not have",
      "would've": "would have",
      "wouldn't": "would not",
      "wouldn't've": "would not have",
      "y'all": "you all",
      "y'all'd": "you all would",
      "y'all'd've": "you all would have",
      "y'all're": "you all are",
      "y'all've": "you all have",
      "you'd": "you would",
      "you'd've": "you would have",
      "you'll": "you will",
      "you'll've": "you will have",
      "you're": "you are",
      "you've": "you have"
  }

  def replace(match):
    return contractions[match.group(0)]
  contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))
  return contractions_re.sub(replace, docString)


"""------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------------Remove Stopwords-----------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------------------"""


def removeStopwords(tokens):
  """Function that removes all stopwords from list of tokens
  Parameters:
      tokens (list of str): tokens with stopwords
  Returns:
      tokens (list of str): tokens without stopwords
  """

  # check to make sure stopwords exists first
  if not os.path.isfile("stopwords"):
    return -1
  file = open("stopwords", "r")

  stopwords = file.read().split()
  # check if all stopwords are valid
  for index, value in enumerate(stopwords):
    while (index < len(stopwords) and (stopwords[index] == ' ')):
      stopwords.pop(index)

  stopwords = set(stopwords)
  # stopword set is created
  # run through all tokens to see if they are stopwords

  for index, token in enumerate(tokens):
    if tokens[index].lower() in stopwords:
      tokens.pop(index)
      while (index < len(tokens) and tokens[index].lower() in stopwords):
        tokens.pop(index)
  return tokens


"""------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------------Stem Wordss----------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------------------"""


def stemWords(tokens):
  """Function that changes the tokens to be stems
  Parameters:
      tokens (list of str): non-stemmed tokens
  Returns:
      tokens (list of str): stemmed tokens
  """
  stemmer = PorterStemmer()
  for value in tokens:
    value = stemmer.stem(value, 0, len(value) - 1)
  return tokens


"""------------------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------------Main Functionality---------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------------------"""

# open folder containing the data collection, provided as the first arugment on the command line ("cranfieldDocs/")
#   read one file at a time from the folder
#   apply removeSGML, then TokenizeText, removeStopwords, stemWords
#   write code to determine
#       total number of words in collection
#       vocab size
#       most frequent 50 words in the collection, along with their frequencies

"""
words [total number of words]
Vocabulary [total number of unique words]
Top 50 words
Word1 [frequency of word 1]
Word2 [frequency of word 2]
...
Word50 [frequency of word 50]
"""
if __name__ == '__main__':
  # check to make sure cranfieldDocs folder Exist
  if len(sys.argv) < 2:
    print("enter in command line folder for data")
    exit(1)
  if not os.path.isdir('./' + sys.argv[1]):
    print("folder does not exist")
    exit(1)

  tokenFreqNum = dict()
  totalWords = 0

  # for each of the files in cranfield docs
  for file in os.listdir('./' + sys.argv[1]):
    docString = ''
    tokens = list()
    with open('./' + sys.argv[1] + file, 'r') as f:
      # read in and parse tokens
      docString = f.read()
      docString = removeSGML(docString)
      tokens = tokenizeText(docString)
      tokens = removeStopwords(tokens)
      tokens = stemWords(tokens)

      # get token frequency
      for token in tokens:
        if not token in tokenFreqNum:
          tokenFreqNum[token] = 1
        else:
          tokenFreqNum[token] += 1

      # add total number of tokens
      totalWords += len(tokens)

  # get 50 most frequent words in the collection
  tokenFreqNum = dict(
    sorted(tokenFreqNum.items(), key=lambda item: item[1], reverse=True))

  # total output for preprocess.answers
  preprocessAnswers = open('preprocess.output', 'w')
  preprocessAnswers.write("Words " + str(totalWords) + '\n')
  # TODO: elminating keys with puncutation
  preprocessAnswers.write("Vocabulary " + str(len(tokenFreqNum.keys())) + '\n')
  preprocessAnswers.write("Top 50 words" + '\n')

  # for key, value in d.iteritems()
  num = 0
  for key, value in tokenFreqNum.items():
    if (50 < num):
      break
    if (key == '.' or key == ',' or key == "'" or key == "\\" or key == "(" or key == ")" or key == "/"):
      continue
    preprocessAnswers.write(str(key) + ' ' + str(value) + '\n')
    num += 1
  preprocessAnswers.close()

  # Calculating 25% of wordcount
  # oneFourthTotalWords = totalWords * .25
  # wordSum = 0
  # numcount = 0
  # for key, value in tokenFreqNum.items():
  #     if oneFourthTotalWords <= wordSum:
  #         break
  #     if (key == '.' or key == ',' or key == "'"  or key == "\\" or key == "(" or key == ")" or key == "/"):
  #         continue
  #     numcount += 1
  #     wordSum += value
  # print("25% wordSum ", numcount)
