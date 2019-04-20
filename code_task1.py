# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 14:20:15 2019

@author: aashaar
"""
import glob
import errno
import nltk
import spacy
from spacy import displacy
#nltk.download()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import copy
from itertools import chain
#from nltk.stem import PorterStemmer

path = 'E:/UTD/4th Sem/Natural Language Processing CS 6320/Project/WikipediaArticles/*.txt' #note C:

#Tokenization:

docs = [] # stores every document in one index of the arrays
sent_tokens = [] # stores sentence tokens of all the documents in one single array
word_tokens = [] # stores word tokens of all the documents in one single array

files = glob.glob(path)
for name in files:
    try:
        with open(name,encoding="utf-8-sig") as f:
            print(f.read())
            file = f.read()
            docs.append(file)
            word_tokens.extend(word_tokenize(file))
            sent_tokens.extend(sent_tokenize(file))
    except IOError as exc: #Not sure what error this is
        if exc.errno != errno.EISDIR:
            raise

#Lemmatization:
lemmatize_word = []
lemmatizer = WordNetLemmatizer() 

for word in word_tokens:
    lemmatize_word.append(lemmatizer.lemmatize(word))
     
# Parts of Speech Tagging:
POS_tags = []
    
POS_tags = nltk.pos_tag(word_tokens)   

#Dependency Graphs with Spacey:
en_nlp =spacy.load('en_core_web_sm')

temp_sent = ['My name is Aashaar', 'he was born in 1994','Apple was founded in 1998','Microsoft was founded in 1800','Who founded Apple?','When did Abraham Lincoln die?','When was the Gettysburg address by Abraham Lincoln']

dependency_parse_dict = dict()


#for sentence in sent_tokens:
for sentence in temp_sent:
    doc = en_nlp(sentence)
    #print(doc.root)
    sent= list(doc.sents)
    for s in sent:
        #print(s.root)
        if s.root.text in dependency_parse_dict:
            dependency_parse_dict[s.root.text].append(s)
        else:
            tempList = []
            tempList.append(s)
            dependency_parse_dict[s.root.text] = tempList

#dependency_parse_dict


#Extract Synonyms, Hypernyms, Hyponyms, Holonyms & Meronymns:
lists = ['Abraham', 'America', 'slavery', 'founded','Apple','lands']

temp_syn=[]
synonymns_dict = dict()

temp_hyper = []
hypernyms_dict = dict()

temp_hypo = []
hyponyms_dict = dict()

temp_mero = []
meronyms_dict = dict()

temp_holo = []
holonyms_dict = dict()

#for word in word_tokens:    
for word in lists:
    for i,j in enumerate(wn.synsets(word)):
        temp_syn.extend(wn.synset(j.name()).lemma_names())
        temp_hyper.extend(list(chain(*[l.lemma_names() for l in j.hypernyms()])))
        temp_hypo.extend(list(chain(*[l.lemma_names() for l in j.hyponyms()])))
        temp_mero.extend(list(chain(*[l.lemma_names() for l in j.part_meronyms()])))
        temp_holo.extend(list(chain(*[l.lemma_names() for l in j.part_holonyms()])))
        
    synonymns_dict[word] = copy.deepcopy(temp_syn)
    hypernyms_dict[word] = copy.deepcopy(temp_hyper)
    hyponyms_dict[word] = copy.deepcopy(temp_hypo)
    meronyms_dict[word] = copy.deepcopy(temp_mero)
    holonyms_dict[word] = copy.deepcopy(temp_holo)
    
    temp_syn.clear()
    temp_hyper.clear()
    temp_hypo.clear()
    temp_mero.clear()
    temp_holo.clear()
    
    
#Named Entity Recognition:
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
doc = nlp('When was the Gettysburg address by Abraham Lincoln?')
print([(X.text, X.label_) for X in doc.ents])


   