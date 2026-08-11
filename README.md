# document-search
Plan/thought:
Input: a directory of files together with a word or words to look for
read through the files and make a index (probably reverse) of each unique word linking them to files
search word then gets a list or lists of files
- [x] Integrate file name words in search?
- [x] Need to normalise words (work on both caps and not, and remove puncuations) 
    - [x] Search split and search filename aswell, but use - and _ instead of whitesapce. Different split  
- [x]Ranking the files (BM25)
- [] Save indexing into file (thinking session style for AWS later)
    if multiple searches in one session, dont want to rebuild index each time.
    and if restarting program still within index i want to load exisitng index from file.
    (JSON?) 


Future:
- connecting it to flask, make UI, try out REST
- AWS option?, learn that and incorporate this project? 
