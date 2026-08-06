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
        if file.name in wordDict[word]:
            # Counting amount, probebly add aditional variables later for ranking
            wordDict[word][file.name] += 1 
        else:
            wordDict[word][file.name] = 1


with os.scandir(folder) as files:
    for file in files:
        if file.is_file() and file.name.endswith(".txt"):
            with open(file.path, "r") as openFile:  
                #Same to file name as for each line
                file_name = pathlib.Path(file.name).stem
                add_to_dict(file_name, file)
                
                for line in openFile:  
                    word_list = line.replace("_", " ").replace("-", " ") \
                         .translate(str.maketrans('', '', string.punctuation)).split()
                    if file_name not in fileDict:
                        fileDict[file_name] = 0
                    fileDict[file_name] += len(word_list)
                    add_to_dict(word_list, openFile)


print(f"Searched word: {search_word_user}")
print("Files:")
for file in wordDict.get(search_word_user, {}):
    print(f"{pathlib.Path(file).stem}, {search_word_user} appears {wordDict[search_word_user][file]}/{fileDict[pathlib.Path(file).stem]} words")
