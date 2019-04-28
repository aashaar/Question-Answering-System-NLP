import re
import pysolr

readFile = open('rural.txt', "r")
textcontent = readFile.read()
paragraphs = textcontent.split('\n\n')
num_s=0
for i in range(len(paragraphs)):
	paragraph = paragraphs[i].split("\n")
	for ss in paragraph[1:]:
		num_s += len(ss)

print("Number of Articles: ", len(paragraphs))
print("Number of Words: ", num_s)