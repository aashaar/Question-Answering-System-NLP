*********************************************************************
* All the programs included in the project will run with Python-3.5 *
*********************************************************************

There are following files in the package: 
*****************************************
1. Final_Report-webscrapers.pdf - The project report
2. Indexer.py - Program to create Solr Indexes 
3. prettytable.py - 3rd Party library to print the feature verctors in a tabular format
4. Project_Part3.py - Library that return the feature vector as needed by Part 3 pf the project
5. project_main.py - The Main program file which takes a Search Query as an input
6. get_corpus_size.py - This is a small program that prints number of Atricles and Words in the corpus 
7. rural.txt - The corpus file


STEPS TO RUN THE QUERY PARSER: 
*****************************
1. get_corpus_size.py in Python-3.5 to get the corpus size
2. Run project_main.py using Python-3.5 in the same folder that has the files: Project_Part3.py, prettytable.py & rural.txt 
3. Make sure that the following libraries are installed on Python-3.5: Nltk-3.2.5, Pysolr
4. project_main.py will ask for a search query as input. 
5. After it runs, it will return output for Project Parts 2,3,4 with the feature vector list used in Part3 of the project. 
6. For part 2,3,4 output only the top 10 output will be printed on the console. 
7. Same query can be executed on Solr GUI to compare the results. 

SOLR INSTALLATION
*****************
1) Download the latest version of SOLR from the site http://www.apache.org/dyn/closer.lua/lucene/solr/7.1.0
2) Copy the location of solr to the your required location. 
3) extract the solr documents using the command tar zxf solr-x.y.z.tgz
4) install java if it is not already present. 

RUNNING SOLR
************
1) Go to the main directory of solr. 
2) Run the command bin/solr start.
3) You can find the solr dashboard in the link http://localhost:8983/solr/#/

CREATING SOLR CORE
******************
1) Go the folder solr-7.1.0/bin and run the command ./solr create -c "corename"

PARAMETERS OF CORE
******************
1) Go to the folder solr-7.1.0/server/solr/core_name and change the managed-schema.txt file to add further features to your index. 

STEPS TO RUN THE INDEXER: 
*************************
1. Change the solr core name on line 8 in the code.
2. Start solr server with same core
3. Run Program Indexer.py (using python-3.5) in the same folder as rural.txt
4. It will take few hours to create all the indexes. 
