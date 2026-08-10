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

# Look into BM25
# b = 0.75 k = 1.2
# Term frequencey (TF) = wordDic[word][file]
# d = fileDict[file]
# avgdl = ((for each something) fileDict[file]/file count)
# IDF, N = number of files and Nt = len(wordDict[word])


k = 1.2
b = 0.75
#Term Frequency (TF)
BM_Scores = {}
for file in wordDict[search_word_user]:   
    print("file loop: ", file)

    TF = wordDict[search_word_user][file]
    print("Term frequency:", TF)

    print("Length of document: ", fileDict[file])
    d = fileDict[file]

    documentAmount = len(fileDict)
    print("amount of documents in search", documentAmount)

    print("amount of documents with file: ", len(wordDict[search_word_user]))
    NQ = len(wordDict[search_word_user])

    IDF = math.log(((documentAmount-NQ+0.5)/(NQ+0.5))+1)
    print("IDF POINT: ", IDF)

    length_sum = 0
    for file2 in fileDict:
        length_sum += fileDict[file2]

    avgdl = length_sum / documentAmount
    print("avgdl: ", avgdl)

    score = (TF * (k + 1)) / (TF + k * (1 - b + b * (d / avgdl)))
    print(f"BM25 score: {score} * {IDF}: ", score * IDF)
    BM_Scores[file] = score * IDF


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

for file in BM_Scores:
    print(f"{file} BM SCORE: ", BM_Scores[file])

