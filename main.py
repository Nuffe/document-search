import os
import string
import pathlib


folder = "test-files"

print("Word to search:")
search_word_user = input().lower()
search_word_hard = "text".lower()
mainDict = {}


def add_to_dict(word_line, file):
    word_list = word_line.replace("_", " ").replace("-", " ") \
    .translate(str.maketrans('', '', string.punctuation)).split() 
    for word in word_list:
        word = word.lower()
        if word not in mainDict:
            mainDict[word] = {}
        if file.name in mainDict[word]:
            # Counting amount, probebly add aditional variables later for ranking
            mainDict[word][file.name] += 1 
        else:
            mainDict[word][file.name] = 1


with os.scandir(folder) as files:
    for file in files:
        if file.is_file() and file.name.endswith(".txt"):
            with open(file.path, "r") as file:
                for line in file:   
                    add_to_dict(line, file)

                #Same to file name as for each line
                file_name = pathlib.Path(file.name).stem
                add_to_dict(file_name, file)


print(f"Searched word: {search_word_user}")
print("Files:")
for file in mainDict.get(search_word_user, {}):
    print(f"{pathlib.Path(file).stem}, {search_word_user} appears {mainDict[search_word_user][file]} times")


