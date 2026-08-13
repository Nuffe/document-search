import os
import string
import pathlib
import math
from rank_bm25 import BM25Okapi
import json
import hashlib




# TO DO:
# Add so the folder is a variable not hardcoded

# 5, make work with multiple file types
# 6, look into multiple search words

def compute_file_hash(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Make workable with JSON
def add_to_dict(word_list, file, wordDict):    
    for word in word_list:
        word = word.lower()
        if word not in wordDict:
            wordDict[word] = {}
        if file in wordDict[word]:
            # Counting amount, probebly add aditional variables later for ranking
            wordDict[word][file] += 1 
        else:
            wordDict[word][file] = 1

def get_index(folder):
    index = {}
    index["files"] = {}
    wordDict = {}
    with os.scandir(folder) as files:  # Differant in future with AWS
        for file in files:
            file_hash = compute_file_hash(file.path)
            file_name = pathlib.Path(file.name).stem
            index["files"][file_name] = {}
            index["files"][file_name]["hash"] = file_hash
            index["words"] = reverse_index(file, index, wordDict)
    return index

def reverse_index(file, index, wordDict):
    if file.is_file() and file.name.endswith(".txt"): # To do 5
        with open(file.path, "r") as openFile:  
            # Add the files name to the index
            file_name = pathlib.Path(file.name).stem
            file_name_list = file_name.replace("_", " ").replace("-", " ") \
                .translate(str.maketrans('', '', string.punctuation)).split()
            add_to_dict(file_name_list, file_name, wordDict)

            for line in openFile:  
                word_list = line.replace("_", " ").replace("-", " ") \
                    .translate(str.maketrans('', '', string.punctuation)).split()

                index["files"][file_name]["length"] = (len(word_list))                
                add_to_dict(word_list, file_name, wordDict)
    return wordDict

# BM25 with +1
# TO DO 6
def BM25(index, search_word_user):
    K = 1.2
    B = 0.75

    BM_Scores = {}
    length_sum = 0
    for file in index["files"]:
        length_sum += index["files"][file]["length"]         # Total length of all files
        BM_Scores[file] = 0

    if search_word_user not in index["words"]:
        return BM_Scores
  
    for file in index["words"][search_word_user]:   
        tf = index["words"][search_word_user][file] # Word frequancy in file
        d = index["files"][file]["length"]                      # document length
        documentAmount = len(index["files"])        # Total amount of documents
        nq = len(index["words"][search_word_user])  # Number of documents with word
        idf = math.log(((documentAmount- nq + 0.5)/(nq + 0.5)) +1) 
        avgdl = (length_sum / documentAmount) # average length of all documents

        score = (tf * (K + 1)) / (tf + K* (1 - B + B * (d / avgdl)))
        BM_Scores[file] = score * idf

        # Sorting, acending based on score
        BM_Scores = {k: v for k, v in sorted(BM_Scores.items(), key=lambda item: item[1], reverse=True)}

    return BM_Scores

# Compare exisiting BM25 to my own
def call_rank_bm25():
    BM_list = []
    with os.scandir("test-files") as files:
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


def run():
    index = get_index("test-files")
    #print("index \n __________\n",json.dumps(index, indent=4, sort_keys=True), "\n _____________")

    while(True):
        print("Input word to search: ")
        user_input = input().lower()
        if user_input == "":
            "no input breaking"
            break
        print("input:", user_input)
        print("BM score:", BM25(index, user_input))

run()