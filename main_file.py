from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import string
example_sent = "This is a sample : sentence, showing_off the stop words filtration."
#  
#stop_words = set(stopwords.words('english')) 
#all_stops = stop_words | set(string.punctuation)
#word_tokens = word_tokenize(example_sent) 
#
#filtered_sentence = [w for w in word_tokens if not w in all_stops] 
#  
##filtered_sentence = [] 
#  
##for w in word_tokens: 
##    if w not in stop_words: 
##        filtered_sentence.append(w) 
#  
#print(word_tokens) 
#print(filtered_sentence)

#Named Entity Recognition:
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
#doc = nlp('When was the Gettysburg address by Abraham Lincoln?')
print([(X.text, X.label_) for X in doc.ents])