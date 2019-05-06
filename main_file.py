from nltk.corpus import stopwords 
import string
import os
from nltk.tokenize import word_tokenize 
import NLPFeatures as fl
import en_core_web_sm
nlp = en_core_web_sm.load()
import spacy
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import pysolr
import json   
en_nlp =spacy.load('en_core_web_sm')
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 
#,"WHO is Abraham Lincoln killed?","Where is Abraham Lincoln killed?"
solr = pysolr.Solr('http://localhost:8983/solr/test3', timeout=10)   

input_sentences = ["Where was Melinda born?","Where is the birth place of Oprah Winfrey?",
                   "Where is the headquarters of AT&T?"]


#input_sentences = ["Who founded Apple Inc.?","Who supported Apple in creating a new computing platform?", "When was Apple Inc. founded?",
#                   "When did Apple go public?","Where is Apple’s headquarters?","Where did Apple open its first retail store?",
#                   "When did Abraham Lincoln die?","Where did Thomas Lincoln purchase farms?","When was the Gettysburg address by Abraham Lincoln?",
#                   "When was the Gettysburg address by Abraham Lincoln?","Who founded UTD?","When was UTD established?","Where was Melinda born?","Where is the birth place of Oprah Winfrey?",
#                   "Where is the headquarters of AT&T?"]

input_questions = ["When did Warren Buffett buy Berkshire Hathaway's shares?","When did Steve Jobs die?","Where is the headquarters of Exxon Mobil?","When was ExxonMobile created?","Where is the headquarters of Amazon.com?"]
input_questions = ["When did Apple go public?","When was the Gettysburg address by Abraham Lincoln?"]
def readQuestions(fileName):
    with open(fileName, 'r') as f:
        temp = f.read().splitlines()
    #function call to delete existing answers.json file if it exists:
    deleteJSONFile()
    
    #function call to process questions
    processQuestions(temp)
    #return temp



def processQuestions(input_questions): 
    term1=""
    term2=""
    stop_words = set(stopwords.words('english'))| set(string.punctuation)
    for question in input_questions:
        print("Started processing for question -> ", question)
        req_entity_type = []
        lower_question = question.lower()
        if "when" in lower_question:
            req_entity_type.extend(["\"DATE\"","\"TIME\""])
            term1="DATE"
            term2="TIME"
     
        elif "who" in lower_question:
            req_entity_type.extend(["\"PERSON\"","\"ORG\""])
            term1="PERSON"
            term2="ORG"
            
        elif "where" in lower_question:
            req_entity_type.extend(["\"GPE\"","\"LOC\""])
            term1="GPE"
            term2="LOC"
            
        
        word_tokens = word_tokenize(lower_question) 
        filtered_question = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = " ".join(filtered_question)
        a,b,c,d,e,f,g,h,i1,j = fl.getNLPFeatures(filtered_sentence)
        word_tokens = ",".join(a)
        lemmatize_word = ",".join(b)
        rootOfSentence = ",".join(c)
        synonymns_list = ",".join(d)
        hypernyms_list = ",".join(e)
        hyponyms_list = ",".join(f)
        meronyms_list = ",".join(g)
        holonyms_list = ",".join(h)
        entities_list = ",".join(i1)
        entities_labels_list = ",".join(j)
        
        
        
        query = "entity_labels_list:("+",".join('{0}'.format(w) for w in (req_entity_type))+" )^10 AND "
        
        query += "((word_tokens:"+word_tokens+")^10 OR (lemmatize_word:"+ lemmatize_word+") OR (synonymns_list:"+synonymns_list+") OR (hypernyms_list:"+hypernyms_list+") OR (hyponyms_list:"+hyponyms_list+") OR (meronyms_list:"+meronyms_list+") OR (holonyms_list:"+holonyms_list+"))"
                
        #print("sentence:"+sentence)
        
        print("Query created for the question")
        #print(query)
        
        
        #print("*************************************************")
    
        ######## call function to get Answer to the query
        answer,sentence,document = getAnswer(query,term1,term2)
        writeToJSON(question,answer,sentence,document)
        print("Processing complete!\n")
    print("******************Program execution finished ******************")
    
    
    
    
    
    
    
    
    
def getAnswer(query,term1,term2):
    results = None
    results = solr.search(q=query,start=0, rows=1)

    #print("length of the results", len(results))
    for result in results:
        #print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
        doc = nlp(str(result['sentence']))
        answer = ""
        for X in doc.ents:
            if(X.label_ == term1 or X.label_ == term2):
                answer += X.text + ","
            #print("Answer is--> ",X.text)
    #if(answer[:-1].isnumeric()):
        return answer[:-1], result['sentence'][0], result['name'][0]


##########
#function to create a JSON file:
def createJSONFile():
    data={}
    data['answers'] =[]
    with open('answers.json', 'w') as json_file:  # writing JSON object
        json.dump(data, json_file)
    print("JSON file created!")

def deleteJSONFile():
    if(os.path.isfile('./answers.json')):
        os.remove('answers.json')

#########
#function to write/append data to the JSON file:  
def writeToJSON(question, answer, sentence, docName):
    #if the JSON file does not exist, create it:
    if(not os.path.isfile('./answers.json')):
        createJSONFile()
    data = {}
    data['answers'] = []
    with open('answers.json') as json_file:  
        data = json.load(json_file)
    data['answers'].append({
            'Question': question,
            'answers': answer,
            'sentences': sentence,
            'documents' : docName            
            })
    with open('answers.json', 'w') as json_file:  # writing JSON object
        json.dump(data, json_file)
    print("JSON file updated!")
    
################################    
    
    
    # Parts of Speech Tagging:
    POS_tags = []
    is_verb = lambda pos: pos[:2] == 'VB'
    verbs = [ps.stem(word) for (word, pos) in nltk.pos_tag(filtered_question) if is_verb(pos)]
    
    mVerbs = []
    for verb in verbs:
        mVerbs.append("\""+verb+"\"")
    
    verbQuery = ",".join(mVerbs) 
    #verbQuery = "hypernyms_list:("+",".join(mVerbs)+" ) AND "
    
    #print(verbQuery)
    
    
    #print("**************************************")
    
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

