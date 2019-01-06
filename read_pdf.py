#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PyPDF2
from pprint import pprint
from pathlib import Path
from util import load_pickle, dump_pickle, unzip_lst, remove_duplicates


# In[ ]:


test_page = -1 # set to -1 to get all pages


# In[ ]:


def write_lines(filename, lines):
    """
    Write a list to a file line by line 
    """
    with open(filename, 'w', encoding="utf-8") as fp:
        for line in lines:
            print(line, file=fp)
    print("Done writing to file %s." % filename)


# In[ ]:


def group_lst(lst, num_grouped):
    num_elements = len(lst)
    num_groups = num_elements // num_grouped
    truncated_lst = lst[:(num_grouped * num_groups)]
    return [truncated_lst[i: (i + num_grouped)] 
            for i in range(0, num_elements, num_grouped)]


# In[ ]:


file = "words.pkl"

fp = Path(file)
if fp.is_file():
    pages = load_pickle(file)
else:
    pdf_file = open('/playpen/home/tongn/Word Frequency List of American English.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    start = 1906
    end = 2053
    pages = []
    for i in range(start, end):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        pages.append(page_content)
    dump_pickle(file, pages)


# In[ ]:


entries = []
bad_pages = []
for (i, page) in enumerate(pages):
    if test_page >= 0:
        i = test_page
        page = pages[test_page]
    
    if i == 0:
        header_len = 50
    else:
        header_len = 1
    page_split = pages[i].split('\n')[header_len:] # [header_len:] to get ride of page number, etc.
    filtered_page = [
        line for line in page_split 
        if (line.strip() != '') and not (len(line) == 1 and 'A' <= line <= 'Z')]
    
    max_iter = 6
    count = 0
    while (True):
        num_lines = len(filtered_page)
        for j in range(num_lines - 1):
            if (filtered_page[j].isdigit() and filtered_page[j + 1].isdigit()):
#                 print("correcting separate digits", filtered_page[j], filtered_page[j + 1])
                filtered_page[j: j + 2] = [filtered_page[j].strip() + filtered_page[j + 1].strip(), '']
#                 print("corrected:", filtered_page[j])
            try:
                if ((not filtered_page[j].isdigit())
                    and (not filtered_page[j] == '')
                    and (not filtered_page[j + 1].isdigit())
                    and (not filtered_page[j + 2].isdigit())):
#                     print("correcting separate word parts", filtered_page[j], filtered_page[j + 1])
                    filtered_page[j: j + 2] = [filtered_page[j].strip() + filtered_page[j + 1].strip(), '']
#                     print("corrected:", filtered_page[j])
            except:
                pass
        filtered_page = [line for line in filtered_page if line != '']
        if len(filtered_page) % 3 == 0 and count >= 2: # forced to iterate three times            
            print("Went through %d iterations" % (count + 1))
            break
        count += 1
        if count >= max_iter:
            print("Reached max iterations on page", i)
            bad_pages.append(i)
            break

    if i == 63: # on page 63, the word "I" will be filtered by 'A' <= 'I' <= 'Z'
        idx = filtered_page.index("11")
        filtered_page.insert(idx + 1, "I")
        bad_pages.remove(i)
    
    grouped = group_lst(filtered_page, 3)
    try:
        sorted(grouped, key=lambda entry: int(entry[0]))
    except:
        print("Can't sort on page", i)
        pprint(grouped)
        exit()
    entries.extend(grouped)
    
    if test_page > 0:
        pprint(grouped)
        break
    
if bad_pages == []:
    sorted_entries = sorted(remove_duplicates(entries), key=lambda entry: int(entry[0]))
    str_entries = ['\t'.join(entry) for entry in sorted_entries]
    write_lines("word_freq_list.txt", str_entries)
    print("Number of words:", len(str_entries))
    print("Supposed number of words:", sorted_entries[-1][0])
else:
    print("Bad pages:", bad_pages)

