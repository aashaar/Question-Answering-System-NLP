from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import NLPFeatures as fl
import en_core_web_sm
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from nltk.corpus import wordnet as wn
en_nlp =spacy.load('en_core_web_sm')
#,"WHO is Abraham Lincoln killed?","Where is Abraham Lincoln killed?"


input_sentences = ["When is Abraham Lincoln killed?","Who founded Apple Inc.?","Who supported Apple in creating a new computing platform?","When was Apple Inc. founded?","When did Apple go public?","Where is Apple’s headquarters?","Where did Apple open its first retail store?","When did Abraham Lincoln die?",
                   "Where did Thomas Lincoln purchase farms?","When was the Gettysburg address by Abraham Lincoln?","Who founded UTD?"]


for sentence in input_sentences:
    
    rootOfSentence = None
    entities = []
    entity_labels = []
    req_entity_type = []
    lower_sentence = sentence.lower()
    if "when" in lower_sentence:
        req_entity_type.extend(["DATE","TIME"])
        print("1") 
    elif "who" in lower_sentence:
        req_entity_type.extend(["PERSON","ORG"])
        print("2")
    elif "where" in lower_sentence:
        req_entity_type.extend(["GPE","LOC"])
        print("3")

    doc = en_nlp(sentence)
    sent= list(doc.sents)
    for s in sent:
        rootOfSentence = s.root.text
    doc = nlp(sentence)
    for X in doc.ents:
        entities.append(X.text)
        entity_labels.append(X.label_)
    print(sentence)
    print(rootOfSentence, entities, entity_labels, req_entity_type)
    print("*********************************")
   
synonymns_list = [] 
word_tokens = ["Apple'"]
for word in word_tokens:
    print(word)
    for i,j in enumerate(wn.synsets(word)):
        synonymns_list.extend(wn.synset(j.name()).lemma_names())
        
print(synonymns_list)