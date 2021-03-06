#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports for compatibility between Python 2&3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six.moves import xrange

import numpy as np
import pickle
from itertools import groupby
import csv
from pathlib import Path
import jsonlines
from nltk.tokenize import word_tokenize
import logging
from gensim.models import KeyedVectors
import itertools
from collections import namedtuple
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options
import sys
from fake_useragent import UserAgent


# In[2]:


# def get_driver(browser="chrome", headless=False, extensions=None, proxy=None, user_agent=None):
#     if browser == "chrome":
#         options = ChromeOptions()
#         if headless:
#             options.add_argument("-headless")
#         if extensions is not None:
#             if not isinstance(extensions, list):
#                 extensions = [extensions]
#             for ext in extensions:
#                 options.add_extension(ext)
#         driver = webdriver.Chrome(chrome_options=options)
#     elif browser == "firefox":
#         profile = webdriver.FirefoxProfile()
#         if headless:
#             options = FirefoxOptions()
#             options.add_argument("--headless")
#         else:
#             options = None
#         if proxy is not None:
#             ip = proxy['ip']
#             port = int(proxy['port'])
#             profile.set_preference("network.proxy.type", 1)
#             profile.set_preference("network.proxy.http", ip)
#             profile.set_preference("network.proxy.http_port", port)
#             profile.set_preference("network.proxy.ssl", ip)
#             profile.set_preference("network.proxy.ssl_port", port)
#         if user_agent is not None:
#             profile.set_preference("general.useragent.override", user_agent)
#
#         profile.update_preferences()
#
#         driver = webdriver.Firefox(
#             firefox_profile=profile,
#             firefox_options=options,
#             executable_path='./geckodriver',
#             proxy=proxy)
#     elif browser == "safari":
#         driver = webdriver.Safari()
#     else:
#         print(f"Error: unknown browser {browser}")
#         raise
#
#     return driver


def get_chromedriver_path():
    platform = sys.platform
    if platform == 'darwin':
        os = 'mac'
    elif platform == 'linux':
        os = 'linux'
    else:
        print("Unrecognized os")
        raise
    print(f'Identified os as {os.capitalize()}.\n')
    chromedriver_path = f'./chromedriver_{os}64'
    return chromedriver_path


def get_driver(headless=False):
    executable_path = get_chromedriver_path()
    user_agent = UserAgent(verify_ssl=False)

    options = Options()
    options.add_argument('--no-sandbox') # for Linux
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'user-agent={user_agent.random}')

    if headless:
        options.add_argument("-headless")
    driver = webdriver.Chrome(
        executable_path=executable_path,
        options=options)

#     driver.implicitly_wait(15)
    return driver

# In[1]:


def split_lst(lst, delimiter, keep_delimiter=True):
    """
    Split list into sublists based on a delimiter
    """
    if keep_delimiter:
        append = [delimiter]
    else:
        append = []
    sublists = [list(y) + append
                for x, y 
                in itertools.groupby(lst, lambda z: z == delimiter) 
                if not x]
    return sublists


# In[ ]:


def split_lst(lst, delimiter):
    """
    Split list into sublists based on a delimiter
    Last modified: 12/4/17
    """
    sublists = [list(y) + [delimiter]
                for x, y 
                in groupby(lst, lambda z: z == delimiter) 
                if not x]
    return sublists


# In[ ]:


def build_dict(lst1, lst2=[]):
    """
    Build dictionary based on one or two lists.
    Args:
        lst1
        lst2
    Returns:
        two dictionaries, the second one is the reverse of the first
    """
    if lst2 == []:
        key2val = {i: val for (i, val) in enumerate(lst1)}
        val2key = {val: i for (val, i) in enumerate(lst1)}
    else:
        assert len(lst1) == len(lst2), (
            "Error in building dictionary: "
            "the two lists do not have the same length")
        key2val = {key: val for (key, val) in zip(lst1, lst2)}
        val2key = {val: key for (key, val) in zip(lst1, lst2)}
        
    return (key2val, val2key)


# In[2]:


def build_index2token(lst, reverse=False):
    if reverse:
        dictionary = {val: i for (i, val) in enumerate(lst)}
    else:
        dictionary = {i: val for (i, val) in enumerate(lst)}
    return dictionary


# In[3]:


def have_duplicates(lst):
    """
    Note: Each element in lst needs to be hashable! (i.e., list of lists won't work)
    """
    return len(set(lst)) < len(lst)


# In[4]:


def exists(path):
    fp = Path(path)
    return fp.is_file()


# In[5]:


def load_word2vec_model():
    """
    Load word embedding model
    """
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', 
        level=logging.INFO)
    model_path = '/playpen/home/tongn/GoogleNews-vectors-negative300.bin'
    model = KeyedVectors.load_word2vec_format(fname=model_path, binary=True)
    return model


# In[6]:


def pad(input_seqs, sequence_lengths, pad_token=0, pad_len=None):
    """
    Pad a batch to max_sequence_length along the second dimension
    Args:
        • input_seqs: a list of sequences
        • sequence_lengths: a list of sequence length
        • pad_token: token used for padding
        • pad_len: maximum lengths to be padded to
    Returns:
        • padded
    """
    if pad_len:
        max_length = pad_len
    else:
        max_length = max(sequence_lengths)
    padded = [input_seq + [pad_token] * (max_length - sequence_length) 
              for (input_seq, sequence_length)
              in zip(input_seqs, sequence_lengths)]
    return padded


# In[7]:


def unzip_lst(lst):
    """
    unzip a list of tuples/lists to multiple lists
    """
    unzipped = list(zip(*lst))
    unzipped_lsts = [list(tp) for tp in unzipped]
    return unzipped_lsts

def zip_lsts(lsts):
    """
    zip a list of lists
    """
    lengths = [len(lst) for lst in lsts]
    assert len(list(set(lengths))) == 1 # assert that the lsts have the same lengths
    zipped_lst = [list(tp) for tp in list(zip(*lsts))]
    return zipped_lst


# In[8]:


def load_pickle(filename):
    with open(filename, "rb") as fp:
        lst = pickle.load(fp)
    print("Done loading %s." % filename)
    return(lst)

def load_pickles(filenames):
    lsts = []
    for filename in filenames:
        lsts.append(load_pickle(filename))
    return lsts

def dump_pickle(filename, lst):
    with open(filename, "wb") as fp:
        pickle.dump(lst, fp)
        print("Done dumping %s." % filename)

def dump_pickles(filenames, lsts):
    for (filename, lst) in zip(filenames, lsts):
        dump_pickle(filename, lst)


# In[9]:


def read_lines(filename):
    """
    Load a file line by line into a list
    """
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    print("Done reading file", filename)
    
    return [line.strip() for line in lines]

def write_lines(filename, lines, mode='w'):
    """
    Write a list to a file line by line 
    """
    with open(filename, mode, encoding="utf-8") as fp:
        for line in lines:
            print(line, file=fp)
    action = 'writing' if mode == 'w' else 'appending'
    print(f"Done {action} to file {filename}.")


# In[10]:


def last_occurance_index(string, char):
    return string.rfind(char)


# In[11]:


def exists(path):
    fp = Path(path)
    return fp.is_file()


# In[12]:


def read_jsonl(path):
    data = []
    with jsonlines.open(path) as reader:
        for obj in reader:
            data.append(obj)
    print("Done reading", path)
    return data


# In[13]:


def tokenize(sent):
    return (word_tokenize(sent))


# In[14]:


def prepend(sents, token_index):
    assert [] not in sents # verify that there is no empty list in "sents"
    assert isinstance(sents[0], list)
    prepended = [[token_index] + sent for sent in sents]
    return prepended 

def append(sents, token_index):
    assert [] not in sents
    assert isinstance(sents[0], list)
    appended = [sent + [token_index] for sent in sents]
    return appended


# In[15]:


def decode2string(index2token, indices, end_token="END_TOKEN", remove_END_TOKEN=False):
    """
    Decode a list of indices to string.
    Args:
        index2token: a dictionary that maps indices to tokens
        indices: a list of indices that correspond to tokens
        remove_END_TOKEN: boolean indicating whether to remove the "END_TOKEN" (optional)
    Returns:
        the decoded string
    """
    decoded = [index2token[index] for index in indices]
    while True:
        if remove_END_TOKEN == True and decoded != []:
            if decoded[-1] == end_token:
                del decoded[-1]
            else:
                break
        else:
            break
    return (' ').join(decoded)


# In[16]:


def group_lst(lst, num_grouped):
    num_elements = len(lst)
    num_groups = num_elements // num_grouped
    truncated_lst = lst[:(num_grouped * num_groups)]
    return [truncated_lst[i: (i + num_grouped)] 
            for i in xrange(0, num_elements, num_grouped)]


# In[17]:


def shuffle(lst1, lst2):
    """
    Shuffle two lists without changing their correspondences
    Args:
        lst1: list 1
        lst2: list 2
    Returns:
        The two shuffled lists
    """
    combined = list(zip(lst1, lst2))
    np.random.shuffle(combined)
    (shuffled_lst1, shuffled_lst2) = zip(*combined)
    return [list(shuffled_lst1), list(shuffled_lst2)]


# In[ ]:


def remove_duplicates(lst):
    """
    Remove duplicates from a list
    list element can be of any type (including list)
    
    Caution: the returned list is automatically sorted!
    """
    lst.sort()
    lst_without_duplicates = [x for (x, _) in groupby(lst)]
    num_removed = len(lst) - len(lst_without_duplicates)
    print("Removed %d duplicates!" % num_removed)
    return lst_without_duplicates

