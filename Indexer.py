# If on Python 2.X
#from _future_ import print_function
import pysolr
import NLPFeatures as fl
import glob
import errno
import os
from spacy import displacy
from nltk.tokenize import sent_tokenize, word_tokenize
# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/test3', timeout = 1000)
path = 'E:/UTD/4th Sem/Natural Language Processing CS 6320/Project/WikipediaArticles/*.txt'
docs = []
sent_tokens = []
def readFiles(path):
    files = glob.glob(path)
    for name in files:
        nameOfFile = (os.path.basename(name))
        print("Started indexing for ",nameOfFile)
        try:
            with open(name,encoding="utf-8-sig") as f:
            #with open(name,encoding="latin-1") as f:
                file = f.read()
                docs.append(file)
                sent_tokens = [] ## bugfix
                sent_tokens.extend(sent_tokenize(file))
                doc_sentences = [dict() for x in range(len(sent_tokens))]
                word_tokens=[]
                lemmatize_word=[]
                rootOfSentence=[]
                synonymns_list=[]
                hypernyms_list=[]
                hyponyms_list=[]
                meronyms_list=[]
                holonyms_list=[]
                entities_list = []
                entity_labels_list = []
                for i in range(0,len(sent_tokens)):
                    a,b,c,d,e,f,g,h,i1,j = fl.getNLPFeatures(sent_tokens[i])
                    #print("sentence", i, "done")
                    word_tokens.append(a)
                    lemmatize_word.append(b)
                    rootOfSentence.append(c)
                    synonymns_list.append(d)
                    hypernyms_list.append(e)
                    hyponyms_list.append(f)
                    meronyms_list.append(g)
                    holonyms_list.append(h)
                    entities_list.append(i1)
                    entity_labels_list.append(j)
                indexSolr(nameOfFile,doc_sentences,sent_tokens,word_tokens,lemmatize_word,rootOfSentence,
                          synonymns_list,hypernyms_list,hyponyms_list,meronyms_list,holonyms_list, entities_list, entity_labels_list)
        except IOError as exc: #Not sure what error this is
            if exc.errno != errno.EISDIR:
                raise

def indexSolr(name, doc_sentences,sentences, word_tokens,lemmatize_word,rootOfSentence,
              synonymns_list,hypernyms_list,hyponyms_list,meronyms_list,holonyms_list,entities_list, entity_labels_list):
    for i in range(0,len(sentences)):
        doc_sentences[i]["name"] = name
        doc_sentences[i]["sentence"] = sentences[i] 
        doc_sentences[i]["word_tokens"] = word_tokens[i]
        doc_sentences[i]["lemmatize_word"] = lemmatize_word[i] 
        doc_sentences[i]["rootOfSentence"] = rootOfSentence[i]
        doc_sentences[i]["synonymns_list"] = synonymns_list[i] 
        doc_sentences[i]["hypernyms_list"] = hypernyms_list[i]
        doc_sentences[i]["hyponyms_list"] = hyponyms_list[i] 
        doc_sentences[i]["meronyms_list"] = meronyms_list[i]
        doc_sentences[i]["holonyms_list"] = holonyms_list[i]
        doc_sentences[i]["entities_list"] = entities_list[i]
        doc_sentences[i]["entity_labels_list"] = entity_labels_list[i]
        
    solr.add(doc_sentences, commit = True)
    print("*******************Indexing done for the file ",name)
#
#coreData=[
#    {
#        "id": "doc_1",
#        "title": "A test document",
#    },
#    {
#        "id": "doc_2",
#        "title": "The Banana: Tasty or Dangerous?"
#    },
#]
#
#print(type(coreData[0]))

#print(solr.add(coreData, commit = True))


#results = solr.search('id:doc_1')
#print("Saw {0} result(s).".format(len(results)))
#
## Just loop over it to access the results.
#for result in results:
#    print("The title is '{0}'.".format(result))

## For a more advanced query, say involving highlighting, you can pass
## additional options to Solr.
#results = solr.search('bananas', **{
#    'hl': 'true',
#    'hl.fragsize': 10,
#})
#
## You can also perform More Like This searches, if your Solr is configured
## correctly.
#similar = solr.more_like_this(q='id:doc_2', mltfl='text')
#
## Finally, you can delete either individual documents,
#solr.delete(id='doc_1')
#
## also in batches...
#solr.delete(id=['doc_1', 'doc_2'])
#
## ...or all documents.
#solr.delete(q=':')

readFiles(path)