#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# !jupyter nbconvert --to script util.ipynb


# In[1]:


from util import read_lines, write_lines, get_driver
from tqdm import tqdm
import random
from nltk import FreqDist
from collections import defaultdict


# In[ ]:


def get_vocab(file):
    lines = read_lines(file)
#     lines = random.sample(lines, 30)
    entries = []
    vocab = set()
    for line in lines:
        split = line.split("\t")
        assert len(split) == 3
        entries.append(split)
        vocab.add(split[1]) # there could be repeated word with different pos tags
    return entries, vocab


# In[ ]:


entries, vocab = get_vocab("word_freq_list.txt")

driver = get_driver(headless=True)
base_url = "https://www.etymonline.com/word/"


# In[ ]:


def get_roots(word):
    url = base_url + word
    driver.get(url)
    
    print("current url:", url)

    related_entries = driver.find_elements_by_xpath(
        "//a[@target='_self']")
    related_words = [
        entry.get_attribute('title').split()[-1] 
        for entry in related_entries]
    related_roots = [
        word for word in related_words 
        if word.startswith('*') and word.endswith('-')]
    if related_roots == []:
        candidate_lemmas = [
            related_word for related_word in related_words
            if (not related_word.startswith('-')
                and not related_word.endswith('-')
                and related_word[:(-1)] in word
                and len(related_word) < len(word))]
        if candidate_lemmas != []:
            related_roots = get_roots(
                max(candidate_lemmas, key=len)) # get the longest one
    
    return related_roots   


# In[ ]:


root_dict = {}
for word in tqdm(vocab):
    print(word)
    try:
        roots = get_roots(word)
        root_dict[word] = roots
    except:
        print(f"Couldn't find word {word}.")
        continue


# In[ ]:


lines = []
for entry in entries:
    line = '\t'.join(
        entry + [', '.join(root_dict[entry[1]])])
    lines.append(line)
write_lines('word_freq_list_with_roots.txt', lines)
driver.quit()

