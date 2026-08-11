import os
import string
import pathlib
import math
from rank_bm25 import BM25Okapi
import json
import hashlib

folder = "test-files"

print("Word to search:")
search_word_user = input().lower()
wordDict = {}
fileDict = {}

# TO DO:
# Add so the folder is a variable not hardcoded
# Load, must check if new files have been added, 
        # Variable of loaded files? to know when more then previously saved are present?
        # Json having a list of files within the index?
        # Save to check if files already have index (hash), append to JSON and only run on new files?
# 5, make work with multiple file types
# 6, look into multiple search words

def compute_file_hash(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        # Read the file in chunks of 8192 bytes
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def load_index():
    print("LOADING INDEX...")
    # if file dont exist run save_index
    # otherwise load it and set variabls right

def save_index():
    print("SAVING INDEX")
    # Runs reverse_index and saves to Json

# Make workable with JSON
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


def load_files():
    with os.scandir(folder) as files:  # Differant in future with AWS
        for file in files:
            file_hash = compute_file_hash(file.path)
            file_name = pathlib.Path(file.name).stem
            fileDict[file_name] = {}
            fileDict[file_name]["hash"] = file_hash
            reverse_index(file)

def reverse_index(file):
    if file.is_file() and file.name.endswith(".txt"): # To do 5
        with open(file.path, "r") as openFile:  

            # Add the files name to the index
            file_name = pathlib.Path(file.name).stem
            file_name_list = file_name.replace("_", " ").replace("-", " ") \
                .translate(str.maketrans('', '', string.punctuation)).split()
            add_to_dict(file_name_list, file_name)

            for line in openFile:  
                word_list = line.replace("_", " ").replace("-", " ") \
                    .translate(str.maketrans('', '', string.punctuation)).split()

                fileDict[file_name]["length"] = (len(word_list))                
                add_to_dict(word_list, file_name)


# BM25 with +1
# TO DO 6
def BM25():
    K = 1.2
    B = 0.75

    BM_Scores = {}
    length_sum = 0
    for file in fileDict:
        length_sum += fileDict[file]["length"]         # Total length of all files
        BM_Scores[file] = 0

    if search_word_user not in wordDict:
        return BM_Scores
  
    for file in wordDict[search_word_user]:   
        tf = wordDict[search_word_user][file] # Word frequancy in file
        d = fileDict[file]["length"]                      # document length
        documentAmount = len(fileDict)        # Total amount of documents
        nq = len(wordDict[search_word_user])  # Number of documents with word
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



load_files()
print(json.dumps(wordDict, indent=4, sort_keys=True))
print(json.dumps(fileDict, indent=4, sort_keys=True))

score = BM25()
print("SCORE:", score)