import re
import pysolr
import sys
import nltk

feature_vector_file_import = __import__('Project_Part3')

solr = pysolr.Solr('http://localhost:8983/solr/nlp_project_core', timeout=10)

print("Please wait for the libraries to load and Indexing to start...")

#solr.delete(q='*:*')

readFile = open(r"rural.txt", "r")
textcontent = readFile.read()
paragraphs = textcontent.split('\n\n')
#print(len(paragraphs))

sum1 = 0

for i in range(len(paragraphs)):

    paragraph = paragraphs[i].split("\n")
    articlename = paragraph[0]
    articletext = "".join(paragraph[1:])

    #    sentences =re.split('\."| \.',articletext)

    sentences = articletext.split(".")

    article_list = [dict() for x in range(len(sentences))]

    sum1 = sum1 + len(sentences)

    for j in range(len(sentences)):
        #        print(j)
        article_list[j]["id"] = str(i) + "_" + str(j)
        article_list[j]["name"] = articlename
        article_list[j]["textsentence"] = nltk.word_tokenize(sentences[j])
        # sentences[j].split(" ")


        ret = feature_vector_file_import.get_feature_vector(sentences[j])
        feature_list = ['POS', 'Lemma', 'Stem', 'Synonym', 'Hypernym', 'Hyponym', 'Meronym', 'Holonym', 'HeadWord']
        for f, line in zip(feature_list, ret):
            article_list[j][f] = line

        # print("hi")
        # print(article_list)
    solr.add(article_list)

print("Indexing is complete now...")
