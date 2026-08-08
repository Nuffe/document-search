import os
import string
import pathlib


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
for file in wordDict[search_word_user]:   
    print("file loop: ", file)
    TF = wordDict[search_word_user][file]
    print("Term frequency:", TF)

    print("Length of document: ", fileDict[file])
    d = fileDict[file]
    print("amount of documents with file: ", len(wordDict[search_word_user]))
    avgdl = len(wordDict[search_word_user])


  #  avgdl = (d / len[wordDict[search_word_user]])
    score = (TF / (TF + k * (1-b+b*(d/avgdl ))))
    print("SCORE: ", score)


print(f"Searched word: {search_word_user}")
print("Files:")
for file in wordDict.get(search_word_user, {}):
    print(f"{file}, {search_word_user} appears {wordDict[search_word_user][file]}/{fileDict[file]} words")
