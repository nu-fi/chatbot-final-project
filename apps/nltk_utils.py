import numpy as np
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import nltk
import torch

# Case Folding
def case_folding(sentence):
    sentence = sentence.lower() # lowercase text
    return sentence

# Remove Puncutuation and Number
clean_spcl = re.compile('[/(){}\[\]\|@,;]')
clean_symbol = re.compile('[^0-9a-z]')
def clean_punct(sentence):
    sentence = clean_spcl.sub('', sentence)
    sentence = clean_symbol.sub(' ', sentence)
    return sentence
    
# Tokenize
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Filtering (stopword removal)
def stopwords_removal(word):
  listStopword = ["ya", "sih"]
  words = []
  for t in word:
    if t not in listStopword:
        words.append(t)
  return words

# Stemming Indo
def stem(word):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(word)

def de_tokenize(text):
    return " ".join(text)

def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag

FILE = "apps/data.pth"
data = torch.load(FILE)

all_words = data['all_words']

from collections import Counter

WORDS = Counter(all_words)

def P(word, N=sum(WORDS.values())):
    # "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    # "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    # "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    # "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)] # [('', 'kemarin'), ('k', 'emarin'), ('ke', 'marin'), dst]
    deletes    = [L + R[1:]               for L, R in splits if R] # ['emarin', 'kmarin', 'kearin', dst]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1] # ['ekmarin', 'kmearin', 'keamrin', dst]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters] # ['aemarin', 'bemarin', 'cemarin', dst]
    inserts    = [L + c + R               for L, R in splits for c in letters] # ['akemarin', 'bkemarin', 'ckemarin', dst]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    # "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
