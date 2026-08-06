# document-search
Plan/thought:
Input: a directory of files together with a word or words to look for
read through the files and make a index (probably reverse) of each unique word linking them to files
search word then gets a list or lists of files
- [x] Integrate file name words in search?
- [x] Need to normalise words (work on both caps and not, and remove puncuations) 
    - [x] Search split and search filename aswell, but use - and _ instead of whitesapce. Different split  
- Ranking the files somehow, future work (word count related to total words and other things)
- connecting it to flask, make UI, try out REST
- AWS option?, learn that and incorporate this project? 
