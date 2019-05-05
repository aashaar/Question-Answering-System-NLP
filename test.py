# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:56:43 2019

@author: aashaar
"""
from __future__ import unicode_literals
import spacy
from nltk import Tree
import pprint
import pysolr

en_nlp =spacy.load('en_core_web_sm')


"""Function to print dependency parsed trees: """
def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_

"""Funtion to get list of PP from a sentences"""
def get_pps(doc):
    "Function to get PPs from a parsed document."
    pps = []
    #verbs = []
    #curr_verb = ""
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        #if token.pos_ == 'VERB' and token.orth_ != curr_verb:
            #curr_verb = token;
        #print(token)
        if token.pos_ == 'ADP':
            pp = ' '.join([tok.orth_ for tok in token.subtree])
            pps.append(pp)
            #verbs.append(curr_verb)
    return pps



result_sent_set=["Abraham Lincoln: A Resource Guide from the Library of Congress\n\"Life Portrait of Abraham Lincoln\", from C-SPAN's American presidents: Life Portraits, June 28, 1999\n\"Writings of Abraham Lincoln\" from C-SPAN's American Writers: A Journey Through History\nAbraham Lincoln: Original Letters and Manuscripts – Shapell Manuscript Foundation\nLincoln/Net: Abraham Lincoln Historical Digitization Project – Northern Illinois University Libraries\nTeaching Abraham Lincoln – National Endowment for the Humanities\nWorks by Abraham Lincoln at Project Gutenberg\nWorks by or about Abraham Lincoln at Internet Archive\nWorks by Abraham Lincoln at LibriVox (public domain audiobooks)\nIn Popular Song:Our Noble Chief Has Passed Away by Cooper/Thomas\nAbraham Lincoln Recollections and Newspaper Articles Collection, McLean County Museum of History\nDigitized items in the Alfred Whital Stern Collection of Lincolniana in the Rare Book and Special Collections Division in the Library of Congress"]
result_sent_set = ["Assassination\nAbraham Lincoln was assassinated by John Wilkes Booth on Good Friday, April 14, 1865, while attending a play at Ford's Theatre, five days after Lee's surrender."]
result_sent_set = ["Assassination\nAbraham Lincoln was assassinated by John Wilkes Booth on Good Friday, April 14, 1865, while attending a play at Ford's Theatre, five days after Lee's surrender.","Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976 to develop and sell Wozniak's Apple I personal computer.","Abraham Lincoln: A Resource Guide from the Library of Congress\n\"Life Portrait of Abraham Lincoln\", from C-SPAN's American presidents: Life Portraits, June 28, 1999\n\"Writings of Abraham Lincoln\" from C-SPAN's American Writers: A Journey Through History\nAbraham Lincoln: Original Letters and Manuscripts – Shapell Manuscript Foundation\nLincoln/Net: Abraham Lincoln Historical Digitization Project – Northern Illinois University Libraries\nTeaching Abraham Lincoln – National Endowment for the Humanities\nWorks by Abraham Lincoln at Project Gutenberg\nWorks by or about Abraham Lincoln at Internet Archive\nWorks by Abraham Lincoln at LibriVox (public domain audiobooks)\nIn Popular Song:Our Noble Chief Has Passed Away by Cooper/Thomas\nAbraham Lincoln Recollections and Newspaper Articles Collection, McLean County Museum of History\nDigitized items in the Alfred Whital Stern Collection of Lincolniana in the Rare Book and Special Collections Division in the Library of Congress"]
result_PP_set =[]
for s in result_sent_set:
    doc = en_nlp(s)
    [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
    result_PP_set.append(get_pps(doc))
    print(get_pps(doc))
 


results = solr.search(q=query,start=0, rows=10000)
    print("length of the results", len(results))
    for result in results:
        #print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
        print(result['name'])



from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
  
example_sent = "when was Abraham Lincoln killed?"#"When did Warren Buffett buy Berkshire Hathaway's shares?"#"This is a sample sentence, showing off the stop words filtration."
example_sent = example_sent.lower()
stop_words = set(stopwords.words('english'))| set(string.punctuation)


word_tokens = word_tokenize(example_sent) 
  
filtered_sentence = [w for w in word_tokens if not w in stop_words] 
print(filtered_sentence) 
 
  
print(word_tokens) 


query= "entity_labels_list:\"DATE\" AND "
for token in filtered_sentence:
    query += "(word_tokens:\""+token+"\" OR lemmatize_word:\""+token+"\" OR synonymns_list:\""+token+"\" OR hypernyms_list:\""+token+"\" OR meronyms_list:\""+token+"\" OR entites_list:\""+token+"\") AND "
query = query[:-4]


print(query[:-4])

sentence_nlp = word_tokenize("Steve Jobs founded Apple in 1980")

import spacy
#nlp = spacy.load("en_core_web_sm")
doc = nlp("Steve Jobs founded Apple in 1980 and went public in 1933") #("I shot an elephant in my sleep")
#doc =nlp("Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne on 5th March April 1976 to develop and sell Wozniak's Apple I personal computer.")
for token in doc:
    print("{2}({3}-{6}, {0}-{5})".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_, token.i+1, token.head.i+1))
    if(token.text == "Apple"):
        print("*********Verb is--> ", token.head.text)


import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(u"Autonomous cars shift insurance liability toward manufacturers")
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])



"""
Query:
    entities_list:"Abraham Lincoln" AND entity_labels_list: "DATE" AND (word_tokens : 'killed' OR lemmatize_word : 'killed' OR synonymns_list : 'die' OR hypernyms_list : 'die' OR hyponyms_list : 'die' OR meronyms_list : 'die' OR entities_list : 'die')

links:
    https://stackoverflow.com/questions/39100652/python-chunking-others-than-noun-phrases-e-g-prepositional-using-spacy-etc
    https://stackoverflow.com/questions/36610179/how-to-get-the-dependency-tree-with-spacy
    https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/
    https://universaldependencies.org/u/pos/all.html
    https://spacy.io/usage/linguistic-features

"""    