import sys, nltk, os
from nltk.corpus import wordnet as wn 
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.parse.stanford import StanfordDependencyParser

#head word:
#http://textminingonline.com/dive-into-nltk-part-v-using-stanford-text-analysis-tools-in-python 
#https://stackoverflow.com/questions/46745686/dependency-tree-using-stanford-parser-from-nltk-results-not-matching-with-stanfo 
#Download Stanford Dep Parser from http://nlp.stanford.edu/software/stanford-parser-full-2014-08-27.zip 
#Set Java path as per correct installation path: 
os.environ['JAVAHOME']="C:\\Program Files\\Java\\jre1.8.0_151\\bin\\java.exe"
stan_dep_parser = StanfordDependencyParser("C:\\Users\\rksin\\Documents\\Subjects\\NLP\\Project\\stanford-parser-full-2014-08-27\\stanford-parser.jar", "C:\\Users\\rksin\\Documents\\Subjects\\NLP\\Project\\stanford-parser-full-2014-08-27\\stanford-parser-3.4.1-models.jar")

#stopwords = stopwords.words('english')
#test_text = "The latest such tragedy being the shooting to death of 26 people in a Texas church and reasons proffered for the shooting range from a domestic situation to President Donald Trump's view that it is a mental health problem."
#tokens = [word.strip() for word in test_text.split(" ")]

def get_feature_vector(sentence):
	return_list = []
	
	#tokenize
	tokens = nltk.word_tokenize(sentence)
	
	#pos tagger
	pos_tag_list = [i[1] for i in nltk.pos_tag(tokens)]
	return_list.append(pos_tag_list)

	#lemmatize
	lmtzr = WordNetLemmatizer()
	#" ".join([lmtzr.lemmatize(i) for i in tokens])
	lemma_list = [lmtzr.lemmatize(i) for i in tokens]
	return_list.append(lemma_list)

	#stem
	port_stemmer = PorterStemmer()
	#" ".join([port_stemmer.stem(i) for i in tokens])
	stem_list = [port_stemmer.stem(i) for i in tokens]
	return_list.append(stem_list)

	#synonym list 
	synonym_list = []
	for t in tokens:
		if wn.synsets(t) != []:
			this_synonym = ""
			for ss in wn.synsets(t):
				if ss.lemmas() == []:
					continue
				elif ss.lemmas()[0].name() != t:
					this_synonym = ss.lemmas()[0].name()
					break
			if this_synonym == "":
				synonym_list.append(t)
			else:
				synonym_list.append(this_synonym)
		else:
			synonym_list.append(t)
	return_list.append(synonym_list)
	
	#hypernym and holonym
	hypernym_list = []
	hyponym_list = []
	for t in tokens:
		if wn.synsets(t) != []:
			if wn.synsets(t)[0].hypernyms() != []:
				if wn.synsets(t)[0].hypernyms()[0].lemmas() != []:
					hypernym_list.append(wn.synsets(t)[0].hypernyms()[0].lemmas()[0].name())
				else:
					hypernym_list.append("fetchedNULLvalue")
			else:
				hypernym_list.append("fetchedNULLvalue")
				
			if wn.synsets(t)[0].hyponyms() != []:
				if wn.synsets(t)[0].hyponyms()[0].lemmas() != []:
					hyponym_list.append(wn.synsets(t)[0].hyponyms()[0].lemmas()[0].name())
				else:
					hyponym_list.append("fetchedNULLvalue")
			else:
				hyponym_list.append("fetchedNULLvalue")
		else:
			hypernym_list.append("fetchedNULLvalue")
			hyponym_list.append("fetchedNULLvalue")
	
	return_list.append(hypernym_list)
	return_list.append(hyponym_list)
	#sorted([lemma.name() for ss in wn.synsets(t) for synset in ss.hypernyms() for lemma in synset.lemmas()])
	#sorted([lemma.name() for ss in wn.synsets(t) for synset in ss.hyponyms() for lemma in synset.lemmas()])

	#meronym and holonym
	meronym_list = []
	holonym_list = []
	for t in tokens:
		if wn.synsets(t) != []:
			if wn.synsets(t)[0].part_meronyms() != []:
				if wn.synsets(t)[0].part_meronyms()[0].lemmas() != []:
					meronym_list.append(wn.synsets(t)[0].part_meronyms()[0].lemmas()[0].name())
				else:
					meronym_list.append("fetchedNULLvalue")
			else:
				meronym_list.append("fetchedNULLvalue")
				
			if wn.synsets(t)[0].part_holonyms() != []:
				if wn.synsets(t)[0].part_holonyms()[0].lemmas() != []:
					holonym_list.append(wn.synsets(t)[0].part_holonyms()[0].lemmas()[0].name())
				else:
					holonym_list.append("fetchedNULLvalue")
			else:
				holonym_list.append("fetchedNULLvalue")
		else:
			meronym_list.append("fetchedNULLvalue")
			holonym_list.append("fetchedNULLvalue")
	
	return_list.append(meronym_list)
	return_list.append(holonym_list)
	#sorted([lemma.name() for ss in wn.synsets(t) for mero in ss.part_meronyms() for lemma in mero.lemmas()])
	#sorted([lemma.name() for ss in wn.synsets(t) for holo in ss.part_holonyms() for lemma in holo.lemmas()])

	#head word
	print("Sentence: "+sentence)
	striped_sentence = sentence.strip(" '\"")
	#if striped_sentence != "" and striped_sentence != r'"' and striped_sentence != r'""' and striped_sentence != "'"  and striped_sentence != "''":
	if striped_sentence != "":
		dependency_parser = stan_dep_parser.raw_parse(striped_sentence)
		parsetree = list(dependency_parser)[0]
		head_word = ""
		head_word = [k["word"] for k in parsetree.nodes.values() if k["head"] == 0][0]
		if head_word != "":
			return_list.append([head_word])
		else:
			for i,pp in enumerate(pos_tag_list):
				if pp.startswith("VB"):
					return_list.append([tokens[i]])
					break
			if head_word == "":
				for i,pp in enumerate(pos_tag_list):
					if pp.startswith("NN"):
						return_list.append([tokens[i]])
						break
	else:
		return_list.append([""])
	
	return return_list
