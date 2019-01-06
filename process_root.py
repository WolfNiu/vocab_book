#!/usr/bin/env python
# coding: utf-8

# In[10]:


"""
Todo:
    • Extract all roots from web/source and rank them. Write book in this ranked order.
"""

from bs4 import BeautifulSoup
import urllib3
import nltk
from util import read_lines
import re


# In[2]:


word = [
    "*pa-",
]
num_words_per_level = 2000


# In[3]:


def get_text(word):
    base_url = "https://www.etymonline.com/word/"
    url = base_url + word
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")
    text = soup.get_text(" ")
    
    main_entry_str = "Advertisement"
    main_entry_index = text.find(main_entry_str) + len(main_entry_str) + 1
    
    if word[0] == "*" and word[-1] == "-":
        end_str = "See all related words"
    else:
        end_str = "Share Advertisement"
        
    start_str = "Related Entries"
    index = text.find(start_str)
    start_index = index + len(start_str) + 1
    end_index = text.find(end_str) - 1

    main_entry = text[main_entry_index: (index - 1)]
    related_words = text[start_index: end_index].split()
    
    return (main_entry, related_words)


# In[6]:


(main_entry, related_words) = get_text(word[0])

print(main_entry)
print("")
print(related_words)


# In[7]:


content = read_lines("word_freq_list.txt")
word_dict = {}
for line in content:
    split = line.split("\t")
    assert len(split) == 3
    word_dict[split[1]] = (int(split[0]), split[2])
print("Done building word dictionary.")


# In[8]:


vocab = list(word_dict.keys())
shared_words = list(set(related_words).intersection(vocab))
sorted_words = sorted(
    shared_words, key=lambda word: word_dict[word])


# In[17]:


print(word[0])
print(main_entry)
print("------------------------------------")

level_count = 0
for shared_word in sorted_words:
    (entry, related_words) = get_text(shared_word)
    level = word_dict[shared_word][0] // num_words_per_level + 1
    if level > level_count and level <= 10:
        print("Level %d:" % level)
        print("==========")
        level_count = level

    print(shared_word, word_dict[shared_word])

    formatted_entry = re.sub(r"(%s \([a-z]+\.[a-z]*\))" % shared_word, r"\n\n\1", entry)
    
#     start_indcies = [
#         m.start() for m in re.finditer((r"%s \([a-z]+\.[a-z]*\)" % shared_word), entry)]
#     for start_index in start_indcies[1:]:
#         entry[(start_index - 1): start_index] = "\n\n"

    print(formatted_entry)
    print("")
    print(related_words)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    


# In[ ]:




