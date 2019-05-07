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
from nltk.corpus import stopwords 

#nltk.download()
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import copy
import string
from itertools import chain
from nltk.stem import PorterStemmer


#removing stop words and punctuations from the sentence
stop_words = set(stopwords.words('english'))
all_stops = stop_words | set(string.punctuation)

#Tokenization:

docs = [] # stores every document in one index of the arrays
sent_tokens = [] # stores sentence tokens of all the documents in one single array



def getNLPFeatures(sentence):
#    print(sentence)
    word_tokens_all = [] # stores word tokens of all the documents in one single array
    word_tokens_all.extend(word_tokenize(sentence))   
    word_tokens = [w for w in word_tokens_all if not w in all_stops]

 
    #Lemmatization and Stemming:
    lemmatize_word = []
    stemmatize_word = []
    lemmatizer = WordNetLemmatizer() 
    ps = PorterStemmer()
    
    for word in word_tokens:
        lemmatize_word.append(lemmatizer.lemmatize(word))
        stemmatize_word.append(ps.stem(word))
         
    # Parts of Speech Tagging:
    POS_tags = []
        
    POS_tags = nltk.pos_tag(word_tokens)   
    
    #Dependency Parsed Tree & root of the sentence with Spacey:
    #dependency parsed tree of the sentence will be a list of list, for example:
        #   [['compound', 'Jobs', 'Steve'],
        #   ['nsubj', 'founded', 'Jobs'],
        #    ['ROOT', 'founded', 'founded'],
        #   ['dobj', 'founded', 'Apple'],
    dependency_parsed_tree =[]
    en_nlp =spacy.load('en_core_web_sm')
    doc = en_nlp(sentence)
    sent= list(doc.sents)
    for s in sent:
        rootOfSentence = s.root.text
    for token in doc:
        dependency_parsed_tree.append([token.dep_,token.head.text,token.text])
    
    #Extract Synonyms, Hypernyms, Hyponyms, Holonyms & Meronymns:

    synonymns_list = []
    hypernyms_list = []
    hyponyms_list = []
    meronyms_list = []
    holonyms_list = []
    
    #for word in word_tokens:    
    for word in word_tokens:
        for i,j in enumerate(wn.synsets(word)):
            synonymns_list.extend(wn.synset(j.name()).lemma_names())
            hypernyms_list.extend(list(chain(*[l.lemma_names() for l in j.hypernyms()])))
            hyponyms_list.extend(list(chain(*[l.lemma_names() for l in j.hyponyms()])))
            meronyms_list.extend(list(chain(*[l.lemma_names() for l in j.part_meronyms()])))
            holonyms_list.extend(list(chain(*[l.lemma_names() for l in j.part_holonyms()])))
    
    entities = []
    entity_labels = []
#    Named Entity Recognition:
    import en_core_web_sm
    nlp = en_core_web_sm.load()
    doc = nlp(sentence)
    for X in doc.ents:
        entities.append(X.text)
        entity_labels.append(X.label_)        
    #print(set(hypernyms_list))
    return word_tokens,lemmatize_word,rootOfSentence,set(synonymns_list),set(hypernyms_list),set(hyponyms_list),set(meronyms_list),set(holonyms_list), entities, entity_labels, stemmatize_word, dependency_parsed_tree
    
     

#
    