import os


folder = "test-files"

with os.scandir(folder) as files:
    for file in files:
        if file.is_file() and file.name.endswith(".txt"):
            with open(file.path, "r") as file:
                for line in file:   
                    print(line.split())

