import os
import string
import pathlib
import math
from rank_bm25 import BM25Okapi

folder = "test-files"

print("Word to search:")
search_word_user = input().lower()
wordDict = {}
fileDict = {}




def add_to_dict(word_list, file):
                        
    for word in word_list:
        word = word.lower()
        if word not in wordDict:
            wordDict[word] = {}
        if file in wordDict[word]:
            # Counting amount, probebly add aditional variables later for ranking
            wordDict[word][file] += 1 
        else:
            wordDict[word][file] = 1

# make function
with os.scandir(folder) as files:
    for file in files:
        if file.is_file() and file.name.endswith(".txt"):
            with open(file.path, "r") as openFile:  

                #Same to file name as for each line
                file_name = pathlib.Path(file.name).stem
                file_name_list = file_name.replace("_", " ").replace("-", " ") \
                    .translate(str.maketrans('', '', string.punctuation)).split()
                add_to_dict(file_name_list, file_name)
                
                for line in openFile:  
                    word_list = line.replace("_", " ").replace("-", " ") \
                        .translate(str.maketrans('', '', string.punctuation)).split()
                    
                    if file_name not in fileDict:
                        fileDict[file_name] = 0
                    fileDict[file_name] += len(word_list)
                    
                    add_to_dict(word_list, file_name)

# BM25 with +1
def BM25():
    K = 1.2
    B = 0.75
    #Term Frequency (TF)
    BM_Scores = {}
    for file in wordDict[search_word_user]:   

        length_sum = 0
        for file2 in fileDict:
            length_sum += fileDict[file2]

        tf = wordDict[search_word_user][file] # Word frequancy in file
        d = fileDict[file]                    # document length
        documentAmount = len(fileDict)        # Total amount of documents
        nq = len(wordDict[search_word_user])  # Number of documents with word
        idf = math.log(((documentAmount- nq + 0.5)/(nq + 0.5)) +1) 
        avgdl = (length_sum / documentAmount) # average length of all documents

        score = (tf * (K + 1)) / (tf + K* (1 - B + B * (d / avgdl)))
        BM_Scores[file] = score * idf
    for file in BM_Scores:
        print(f"{file} BM SCORE: ", BM_Scores[file])


def call_rank_bm25():
    BM_list = []
    with os.scandir(folder) as files:
        for file in files:
            if file.is_file() and file.name.endswith(".txt"):
                with open(file.path, "r") as openFile:
                    corpus = openFile.read()
                    corpus = corpus.replace("_", " ").replace("-", " ") \
                            .translate(str.maketrans('', '', string.punctuation)).lower().split()
                    BM_list.append(corpus)

    print("BM LIST:", BM_list)
    bm25 = BM25Okapi(BM_list)
    query = "hello"
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    print("BM25 LIB scores", doc_scores)




BM25()

# Bugs to fix:
# Error when word dont exist