import os
import string
import pathlib


folder = "test-files"
search_word = "text".lower()
mainDict = {}


def add_to_dict(line_array, file):
    for word in line_array:
        word = word.lower()
        if word not in mainDict:
            mainDict[word] = {}
        if file.name in mainDict[word]:
            mainDict[word][file.name] += 1
        else:
            mainDict[word][file.name] = 1


with os.scandir(folder) as files:
    for file in files:
        if file.is_file() and file.name.endswith(".txt"):
            with open(file.path, "r") as file:
                for line in file:   
                    split_line = line.translate(str.maketrans('', '', string.punctuation)).split()
                    add_to_dict(split_line, file)

                #Same to file name as for each line
                file_name = pathlib.Path(file.name).stem
                file_name = file_name.replace("_", " ").replace("-", " ").split() #File names use - and _ instead of whitespace
                add_to_dict(file_name, file)


print(f"Searched word: {search_word}")
print("Files:")
for file in mainDict.get(search_word, {}):
    print(f"{file}, appears {mainDict[search_word][file]} times")


