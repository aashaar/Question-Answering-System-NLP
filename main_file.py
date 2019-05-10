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
import sys

solr = pysolr.Solr('http://localhost:8983/solr/final1', timeout=10)   

#input_questions = ["Who founded Apple Inc.?","Who supported Apple in creating a new computing platform?", "When was Apple Inc. founded?",
#                   "When did Apple go public?","Where is Apple’s headquarters?","Where did Apple open its first retail store?",
#                   "When did Abraham Lincoln die?","Where did Thomas Lincoln purchase farms?","When was the Gettysburg address by Abraham Lincoln?",
#                   "When was the Gettysburg address by Abraham Lincoln?","Who founded UTD?","When was UTD established?","Where was Melinda born?","Where is the birth place of Oprah Winfrey?",
#                   "Where is the headquarters of AT&T?"]

#input_questions = ["When did Warren Buffett buy Berkshire Hathaway's shares?","When did Steve Jobs die?","Where is the headquarters of Exxon Mobil?","When was ExxonMobile created?","Where is the headquarters of Amazon.com?"]
#input_questions = ["When did Apple go public?","When was the Gettysburg address by Abraham Lincoln?"]



def readQuestions(fileName):
    if(os.path.isfile(fileName)):
        with open(fileName, 'r') as f:
            temp = f.read().splitlines()
        #function call to delete existing answers.json file if it exists:
        deleteJSONFile()
        
        #function call to process questions
        processQuestions(temp)
        #return temp
    else:
        print("ERROR: Please provide a valid path for the questions file in the arguments.")



def processQuestions(input_questions): 
    
    stop_words = set(stopwords.words('english'))| set(string.punctuation)
    for question in input_questions:
        term1=""
        term2=""
        if (len(question) == 0) or (question == ""): # if question string is empty
            continue
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
        else:   
            req_entity_type.extend("*")
             
        word_tokens = word_tokenize(question) 
        filtered_question = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = " ".join(filtered_question)
        a,b,c,d,e,f,g,h,i1,j,k,l,m = fl.getNLPFeatures(filtered_sentence)
        word_tokens = ",".join(a) if len(a) != 0 else "*"
        lemmatize_word = ",".join(b) if len(b) != 0 else "*"
        rootOfSentence = ",".join(c) if len(c) != 0 else "*"
        synonymns_list = ",".join(d) if len(d) != 0 else "*"
        hypernyms_list = ",".join(e) if len(e) != 0 else "*"
        hyponyms_list = ",".join(f) if len(f) != 0 else "*"
        meronyms_list = ",".join(g) if len(g) != 0 else "*"
        holonyms_list = ",".join(h) if len(h) != 0 else "*"
        entities_list = ",".join(i1) if len(i1) != 0 else "*"
        entities_labels_list = ",".join(j) if len(j) != 0 else "*"
        stemmatize_word = ",".join(k) if len(k) != 0 else "*"
        
        
        
        #query = "entity_labels_list:("+",".join('{0}'.format(w) for w in (req_entity_type))+" )^10 AND "
        #query += "((word_tokens:"+word_tokens+")^10 OR (lemmatize_word:"+ lemmatize_word+") OR (synonymns_list:"+synonymns_list+") OR (hypernyms_list:"+hypernyms_list+") OR (hyponyms_list:"+hyponyms_list+") OR (meronyms_list:"+meronyms_list+") OR (holonyms_list:"+holonyms_list+"))"
                
        query = "entity_labels_list:("+",".join(req_entity_type)+" )^20 AND "
        #query += "((word_tokens:"+word_tokens+")^10 AND (lemmatize_word:"+ lemmatize_word+") AND (synonymns_list:"+synonymns_list+") AND \
        #(hypernyms_list:"+hypernyms_list+") AND (hyponyms_list:"+hyponyms_list+") AND (meronyms_list:"+meronyms_list+") AND \
        #(holonyms_list:"+holonyms_list+") OR (entities_list:"+entities_list+")^10 OR (stemmatize_word:"+stemmatize_word+"))"
            
        query += "((word_tokens:"+word_tokens+")^20 OR (lemmatize_word:"+ lemmatize_word+")^10 OR (synonymns_list:"+synonymns_list+")^10 OR \
        (hypernyms_list:"+hypernyms_list+") OR (hyponyms_list:"+hyponyms_list+") OR (stemmatize_word:"+stemmatize_word+")^10 AND (entities_list:"+entities_list+")^20)"
        
        #print("sentence:"+sentence)
        #print(query)
        
        print("Query created for the question")
        #print(query)
        
        #print("*************************************************")
    
        ######## call function to get Answer to the query
        answer,sentence,document = getAnswer(query,term1,term2,entities_list)
        writeToJSON(question,answer,sentence,document)
        print("Processing complete!\n")
    print("*********Program execution finished *********")
    
  
    
    
def getAnswer(query,term1,term2,entities_list):
    results = None
    #print("term1", term1)
    if term1 == "" or term2 == "": # if an invalid question type is provided.
        return "WARNING: Question type not recognized", "N.A.", "N.A."
    results = solr.search(q=query,start=0, rows=10)
    if len(results) == 0:
        return "Answer not found", "N.A.", "N.A."

    #print("length of the results", len(results))
    counter = 0
    for result in results:
        #print(result['sentence'])
        ######## code to check entities
        #counter += 1
#        ans_entity_list = result['entities_list']
#        flag = False
#        print((ans_entity_list))
#        print((entities_list))
#        for e1 in ans_entity_list:
#            for e2 in  entities_list:
#                print(e1+":::"+e2)
#                if((e1 in e2) or (e2 in e1)):
#                    print("flag made true")
#                    flag = True
#                    break
#            if(flag==True):
#                break
#        if(not flag and counter<len(results)-1):
#            continue
        
            
        
        #print("The title is '{0}','{1}'.".format(result['sentence'],result['name']))
        doc = nlp(str(result['sentence'][0]))
        answer = ""
        for X in doc.ents:
            if(X.label_ == term1 or X.label_ == term2):
                ######### for WHO questions: ensure that that ensure that answer is not same/
                # as the question's main entity. ex: Who founded Apple? shouldn't return 'Apple'
                if(term1 == 'PERSON'):
                    #print(type(result['sentence'][0]),"::",X.text,"**", entities_list)
                    if (not (X.text in entities_list)):# filter out the entity in question from the answer
                        #print("X.text",X.text)
                        answer = X.text
                        break
                else:
                    answer = X.text
                    break                       
            #print("Answer is--> ",X.text)
    #if(answer[:-1].isnumeric()):
        #return answer[:-1], result['sentence'][0], result['name'][0]
        counter += 1
        if(len(answer)==0 and counter<10):
            continue
        
        return answer, result['sentence'][0], result['name'][0]


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

if __name__ == '__main__':
    path = ""
    path = sys.argv[1]
    #print("path= ",path)
    readQuestions(path)
    