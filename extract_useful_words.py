#!/usr/bin/env python
# coding: utf-8

# In[1]:


from util import get_driver, read_lines, write_lines, dump_pickle, load_pickle
from pprint import pprint
from tqdm import tqdm
from collections import OrderedDict
import os


# In[2]:


driver = get_driver(browser='chrome', headless=True)


# In[3]:


entries = read_lines('roots.txt')
vocab = OrderedDict()
for entry in tqdm(entries):
    lst = entry.split()
    word = lst[1]
    # Ignore same word with different pos tag
    if word not in vocab:
        vocab[word] = [lst[0]] + lst[2:]


# In[4]:


def get_num_related(word, verbose=False):
    driver.get(f'https://www.merriam-webster.com/thesaurus/{word}')
    
    hwords = driver.find_element_by_xpath("//h1[@class='hword']")
    if hword.text != word: # if the word is not the main entry
        print(f"Couldn't find main entry for {word}.")
        print(f"The main entry shown is {hword.text}\n")
        return 0
    
    elems = driver.find_elements_by_xpath(
        '//a[starts-with(@href, "/dictionary/")]')    
    related_words = [
        elem.text.strip()
        for elem in elems]
    
    if verbose:
        print(len(related_words))
        print(related_words[1:-1])
    
    in_vocab_words = [
        related_word
        for related_word in set(related_words[1:-1])
        if all([(token in vocab) 
                for token 
                in related_word.replace('(', '').replace(')', '').split()])]
    num_related = len(in_vocab_words)
    
    if verbose:
        print("")
        print(num_related)
        print(in_vocab_words)
    
    
    return num_related


# In[ ]:


intermediate_file = 'intermediate_importance.pkl'
if os.path.exists(intermediate_file):
    new_vocab = load_pickle(intermediate_file)
    print(f"Loaded intermediate .pkl file with {len(new_vocab)} entries")
else:
    new_vocab = OrderedDict()


# In[ ]:


for i, (word, lst) in tqdm(enumerate(list(vocab.items()))):
    if word in new_vocab:
        continue
    try:
        num_related = get_num_related(word)
    except:
        num_related = -1
    new_vocab[word] = [lst[0], str(num_related)] + lst[2:]
    
    if i % 25 == 0 and i > 0: # store intermediate result every ? iterations
        dump_pickle("intermediate_importance.pkl", new_vocab)
        updated_entries = [
            '\t'.join([k] + v) 
            for k, v in new_vocab.items()] 
        write_lines('importance.txt', updated_entries)

updated_entries = [
    '\t'.join([k] + v) 
    for k, v in new_vocab.items()] 
write_lines('importance.txt', updated_entries)
    
driver.close()


# In[ ]:





# In[ ]:




