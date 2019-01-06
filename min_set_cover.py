#!/usr/bin/env python
# coding: utf-8

# In[13]:


from util import read_lines, write_lines
from nltk import FreqDist
from collections import defaultdict
from dlx import DLX


# In[4]:


lines = read_lines("word_freq_list_with_roots.txt")

all_roots = []
entries = []
for line in lines:
    split = line.split('\t')
    if len(split) == 4:
        roots = split[-1].split(', ')
        all_roots.extend(roots)
        split[-1] = roots
    else:
        roots = []
        split.append(roots)
    entries.append(split)

dist = dict(FreqDist(all_roots).most_common())
vocab_roots = list(dist.keys())
root2idx = {root: idx for idx, root in enumerate(vocab_roots)}

root2entries = defaultdict(list)
for entry in entries:
    roots = entry[-1]
    for root in roots:
        root2entries[root].append(entry)

# for root in dist:
#     print(root)
#     print("")
#     print(root2entries[root])
#     input("wait")


# In[10]:


def genInstance(labels, rows) :
    columns = []
    indices_l = {}
    for i in range(len(labels)) :
        label = labels[i]
        indices_l[label] = i
        columns.append(tuple([label,0]))
    return labels, rows, columns, indices_l

def solveInstance(instance) :
    labels, rows, columns, indices_l = instance
    instance = DLX(columns)
    indices = {}
    for l, i in zip(rows, range(len(rows))) :
        h = instance.appendRow(l, 'r'+str(i))
        indices[str(hash(tuple(sorted(l))))] = i
    sol = instance.solve()
    lst = list(sol)
    selected = []
    for i in lst[0] :
        l = instance.getRowList(i)
        l2 = [indices_l[label] for label in l]
        idx = indices[str(hash(tuple(sorted(l2))))]
        selected.append(idx)
    return selected

def printColumnsPerRow(instance, selected) :
    labels, rows, columns, indices_l = instance
    print('covered columns per selected row')
    for s in selected :
        A = []
        for z in rows[s-1] :
            c, _ = columns[z]
            A.append(c)
        print(s, A)

def printInstance(instance) :
    labels, rows, columns, indices_l = instance
    print('columns')
    print(labels)
    print('rows')
    print(rows)


# In[11]:


labels = vocab_roots
rows = [
    [root2idx[root] 
     for root in entry[-1]]
    for entry in entries
    if entry[-1] != []]


# In[ ]:


# labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
# rows = [[0,3,6],[0,3],[3,4,6],[2,4,5],[1,2,5,6],[1,6]]
instance = genInstance(labels, rows)
selected = solveInstance(instance)
printInstance(instance)
printColumnsPerRow(instance, selected)

