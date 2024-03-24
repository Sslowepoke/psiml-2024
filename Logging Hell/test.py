words = {'a' : 3, 
         'b' : 4,
         'd' : 2,
         'c' : 2}
# if len(traverse_dir.words) <= 5:
sorted_words = dict(sorted(words.items()))
word_list =  sorted(sorted_words, key = sorted_words.get, reverse=True)
print(*word_list[0:5], sep=', ')