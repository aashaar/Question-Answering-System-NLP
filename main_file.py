from nltk.corpus import stopwords 
import string
from nltk.tokenize import word_tokenize 
import NLPFeatures as fl
import en_core_web_sm
import spacy
nlp = en_core_web_sm.load()
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import pysolr   
en_nlp =spacy.load('en_core_web_sm')
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 
#,"WHO is Abraham Lincoln killed?","Where is Abraham Lincoln killed?"
solr = pysolr.Solr('http://localhost:8983/solr/test3', timeout=10)   

#input_sentences = ["When was Abraham Lincoln killed?","Who founded Apple Inc.?","Who supported Apple in creating a new computing platform?","When was Apple Inc. founded?","When did Apple go public?","Where is Apple’s headquarters?","Where did Apple open its first retail store?","When did Abraham Lincoln die?",
#                   "Where did Thomas Lincoln purchase farms?","When was the Gettysburg address by Abraham Lincoln?","Who founded UTD?"]

#input_sentences = ["When did Apple go public?","When did Abraham Lincoln die?","Who was the chairman of Apple","Where did Thomas Lincoln purchase farms?"]#,"Who founded Apple Inc.?","When did Warren Buffett buy Berkshire Hathaway's shares?","Where did AT&T spread to South America?"]

input_sentences = ["Who founded Apple Inc.?","Who supported Apple in creating a new computing platform?", "When was Apple Inc. founded?",
                   "When did Apple go public?","Where is Apple’s headquarters?","Where did Apple open its first retail store?",
                   "When did Abraham Lincoln die?","Where did Thomas Lincoln purchase farms?","When was the Gettysburg address by Abraham Lincoln?",
                   "When was the Gettysburg address by Abraham Lincoln?","Who founded UTD?","When was UTD established?"]
#query = "entites_list:'Abraham Lincoln' AND entity_labels_list: 'DATE' AND (word_tokens : 'killed' OR lemmatize_word : 'killed' OR synonymns_list : 'die' OR hypernyms_list : 'die' OR hyponyms_list : 'die' OR meronyms_list : 'die' OR entites_list : 'die')"
#query = "entites_list:\"Abraham Lincoln\" AND entity_labels_list: \"DATE\" AND (word_tokens : 'killed' OR lemmatize_word : 'killed' OR synonymns_list : 'die' OR hypernyms_list : 'die' OR hyponyms_list : 'die' OR meronyms_list : 'die' OR entites_list : 'die')"
#query = "entites_list:\"Abraham Lincoln\" AND entity_labels_list: \"DATE\" AND (word_tokens : \"killed\" OR lemmatize_word : \"killed\" OR synonymns_list : \"die\" OR hypernyms_list : \"die\" OR hyponyms_list : \"die\" OR meronyms_list : \"die\" OR entites_list : \"die\")"
#query = "*:*"


stop_words = set(stopwords.words('english'))| set(string.punctuation)
for sentence in input_sentences:
    req_entity_type = []
    lower_sentence = sentence.lower()
    if "when" in lower_sentence:
        req_entity_type.extend(["\"DATE\"","\"TIME\""])
        print("1") 
    elif "who" in lower_sentence:
        req_entity_type.extend(["\"PERSON\"","\"ORG\""])
        print("2")
    elif "where" in lower_sentence:
        req_entity_type.extend(["\"GPE\"","\"LOC\""])
        print("3")
    
    word_tokens = word_tokenize(lower_sentence) 
    filtered_question = [w for w in word_tokens if not w in stop_words]
    # Parts of Speech Tagging:
    POS_tags = []
    is_verb = lambda pos: pos[:2] == 'VB'
    verbs = [ps.stem(word) for (word, pos) in nltk.pos_tag(filtered_question) if is_verb(pos)]
    
    mVerbs = []
    for verb in verbs:
        mVerbs.append("\""+verb+"\"")
    
    verbQuery = ",".join(mVerbs) 
    #verbQuery = "hypernyms_list:("+",".join(mVerbs)+" ) AND "
    
    print(verbQuery)
    
    
    print("**************************************")
    
    query= "entity_labels_list:("+",".join(req_entity_type)+" ) AND "
    query += "(synonymns_list:"+verbQuery+" OR hypernyms_list:"+verbQuery+" OR meronyms_list:"+verbQuery+" OR hyponyms_list:"+verbQuery+") AND "
    
    #print(query)
    for token in filtered_question:
        query += "(word_tokens:\""+token+"\" OR lemmatize_word:\""+lemmatizer.lemmatize(token)+"\" OR synonymns_list:\""+token+"\" OR hypernyms_list:\""+token+"\" OR meronyms_list:\""+token+"\" OR entities_list:\""+token+"\") AND "
    query = query[:-4]
    print(query)
    print("*********************************************************************************")
    results = solr.search(q=query,start=0, rows=10000)
    print("length of the results", len(results))
    for result in results:
        print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
    ###################################### Commented block aplha starts
    #example o/p: 
     #   When was Abraham Lincoln killed?
      #  killed ['Abraham Lincoln'] ['PERSON'] ['DATE', 'TIME']
    #doc = en_nlp(sentence)
    #sent= list(doc.sents)
    #for s in sent:
    #   rootOfSentence = s.root.text
    #doc = nlp(sentence)
    #for X in doc.ents:
    #    entities.append(X.text)
    #    entity_labels.append(X.label_)
    #print(sentence)
    #print(rootOfSentence, entities, entity_labels, req_entity_type)
    #print("*********************************")
    ##################################### Commented block aplha end
    
#    results = solr.search(q=query,start=0, rows=10000)
#    print("length of the results", len(results))
#    for result in results:
#       print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))


    
    
    
synonymns_list = [] 
hypernyms_list =[]
hyponyms_list=[]
meronyms_list = []
holonyms_list = []

word_tokens = ["die"]
for word in word_tokens:
    #print(word)
    for i,j in enumerate(wn.synsets(word)):
        synonymns_list.extend(wn.synset(j.name()).lemma_names())
        hypernyms_list.extend(wn.synset(j.name()).hypernyms()) 
        hyponyms_list.extend(wn.synset(j.name()).hyponyms())
        meronyms_list.extend(wn.synset(j.name()).part_meronyms())
        holonyms_list.extend(wn.synset(j.name()).part_holonyms())
print(synonymns_list)
