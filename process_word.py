#!/usr/bin/env python
# coding: utf-8

# In[10]:


"""
Todo:
    • debug and see why all_roots is [] most of the time!
"""

from bs4 import BeautifulSoup
import urllib3
import nltk
from util import read_lines, write_lines, dump_pickle, load_pickle
import re
from functools import reduce
from pprint import pprint
import itertools
import sys
from fuzzywuzzy import fuzz
from tqdm import tqdm
from pattern.en import lemma, comparative, superlative


# In[ ]:


debugging = False

base_url = "https://www.etymonline.com/"
# Todo: combine these two
match_reg_exp = r'href="/word/[a-z\*-]+"'
href_str = 'href="/word/'
offset_len = len(href_str)

fuzz_threshold = 73 # Lowest so far: "Kurdish" vs. "Kurd"


# In[ ]:


# string = '<a href="/word/-ship" class="crossreference">'
# find_all_occurances(match_reg_exp, string)


# In[ ]:


def get_content(url):
    if not isinstance(url, str):
        return None

    # Get content
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', url)
    except:
        print("Error in url:", url)
        return None
    content = response.data.decode("UTF-8")
    return content


# In[ ]:


def find_all_occurances(reg_exp, string):
    """Find all occurances of start & end indices of in a string based on reg_exp"""
    matches = [m for m in re.findall(reg_exp, string)]
    return matches


# In[ ]:


def extract_roots(matches):
    roots = [match[offset_len:(-1)] for match in matches]
    roots_no_duplicate = list(set(roots))
    return roots_no_duplicate


# In[ ]:


def find_top_search_result(word):
#     try:
    page = 0
    """we go through each page of the query"""
    while True:
        page_str = "" if page == 0 else "page=%d&" % page
        query_url = base_url + "search?" + page_str + "q=" + word
        query_content = get_content(query_url)
        if query_content is None:
            break
        
        if "No results were found" in query_content:
            break
        else:
            page += 1

        truncate_index = query_content.find("Trending Words")
        if truncate_index != -1:
            query_content = query_content[:truncate_index]

        word_start_indices = [m.end() for m in re.finditer(href_str, query_content)]
    #     print(word_start_indices)
        offsets = [
            query_content[word_start_index:].find('">') 
            for word_start_index
            in word_start_indices]
    #     print(query_content[word_start_indices[0]:])
    #     input("wait")
    #     print(offsets)
        for (word_start_index, offset) in zip(word_start_indices, offsets):
    #         if offset == -1:
    #             continue
            searched_word = query_content[word_start_index: (word_start_index + offset)]
    #         print(searched_word)
            if fuzz.ratio(word, searched_word) >= fuzz_threshold:
                url = base_url + "word/" + searched_word 
                return url # returning the first occurance
    return None
    
#         print(matches)
#         input("continue?")
        
#         top_url_start_index = query_content.find(href_str)
#         word_start_index = top_url_start_index + offset_len
#         top_url_end_offset = query_content[word_start_index:].find('">')
#         top_word = query_content[word_start_index: (word_start_index + top_url_end_offset)]
        
#         url = base_url + "word/" + top_word
#     except:
#         print("Warning: Didn't get top search result for", word)
#         return None
        
#         top_word = None
    
#     if top_word is None or (top_word is not None and fuzz.ratio(word, top_word) < fuzz_threshold):
#         url = base_url + "word/" + word
#         print("Warning: Didn't get top search result for", word)
#         return None
#     else:
#         return url


# In[4]:


replace_dict = {
    "researcher": ["research", "-er"],
    "ultimately": "ultimate",
    "ourselves": ["our", "self"],
    "fewer": "few",
    "playoff": ["play", "off"],
    "regulatory": "regulate",
    "officially": "official",
    "supplier": ["supply", "-er"],
    "closest": "close",
    "learner": ["learn", "-er"],
    "dioxide": ["di-", "oxide"],
    "nearest": "near",
    "technically": "technical",
    "setup": "set-up",
    "subscale": ["sub-", "scale"],
    "collaborative": "collaborate",
    "statewide": ["state", "wide"],
    "policymaker": ["policy", "make", "-er"],
    "linebacker": ["line", "back", "-er"],
    "fastest": "fast",
    "strangely": "strange",
    "brightly": "bright",
    "deepest": "deep",
    "nutritional": "nutrition",
    "northeastern": ["north", "eastern"],
    "wartime": ["war", "time"],
    "paid": "pay",
    "dealings": "deal",
    "onstage": ["on", "stage"],
    "doctoral": "doctor",
    "turnout": ["turn", "out"],
    "computerized": ["computer", "-ize"],
    "consciously": "conscious",
    "assistive": "assist",
    "redshift": ["red", "shift"],
    "superconducting": ["super", "conduct"],
    "wanderer": ["wander", "-er"],
    "dichotomous": "dichotomy",
    "stoplight": ["stop", "light"],
    "crisply": "crisp",
    "winemaker": ["wine", "maker"],
    "apologetically": "apologetic",
    "pilings": "piling",
    "intercut": ["inter-", "cut"],
    "descriptor": "describe",
    "governorship": ["governor", "-ship"],
    "songwriting": ["song", "write"],
    "generalizability": ["generalize", "-ability"],
    "walkie": "walk",
    "raiser": ["raise", "-er"],
    "redefinition": "redefine",
    "sauté": "saute",
    "curiously": "curious",
    "affective": "affect",
    "attacker": ["attack", "-er"],
    "gunfire": ["gun", "fire"],
    "goodwill": ["good", "will"],
    "spokesperson": ["speak", "person"],
    "midwestern": ["mid-", "western"],
    "federally": "federal",
    "rename": ["re-", "name"],
    "drugstore": ["drug", "store"],
    "cloning": "clone",
    "marketer": "market",
    "postseason": ["post-", "season"],
    "storyteller": ["story", "tell"],
    "uninsured": ["un-", "insure"],
    "buyout": ["buy", "out"],
    "scorer": ["score"],
    "insofar": ["in", "so", "far"],
    "midtown": ["mid-", "town"],
    "stakeholder": ["stake", "hold"],
    "cornerback": ["corner", "back"],
    "minivan": ["mini-", "van"],
    "Headnote": ["head", "note"],
    "cutback": ["cut", "back"],
    "preseason": ["pre-", "season"],
    "schoolteacher": ["school", "teach"],
    "roadway": ["road", "way"],
    "Peruvian": "Peru",
    "foothill": ["foot", "hill"],
    "backcountry": ["back", "country"],
    "exceedingly": "exceed",
    "rearview": ["rear", "view"],
    "spearhead": ["spear", "head"],
    "schoolchild": ["school", "child"],
    "backseat": ["back", "seat"],
    "peacekeeper": ["peace", "keep"],
    "newsroom": ["news", "room"],
    "bookshelf": ["book", "shelf"],
    "headset": ["head", "set"],
    "fieldwork": ["field", "work"],
    "campsite": ["camp", "site"],
    "rainforest": ["rain", "forest"],
    "songwriter": ["song", "write"],
    "lunchtime": ["lunch", "time"],
    "rescuer": ["rescue", "-er"],
    "fastball": ["fast", "ball"],
    "airwaves": ["air", "wave"],
    "Frenchman": ["French", "man"],
    "matchup": ["match", "up"],
    "cheekbone": ["cheek", "bone"],
    "preschooler": "preschool",
    "densely": "dense",
    "guidebook": ["guide", "book"],
    "airliner": "airline",
    "nonstick": ["non-", "stick"],
    "ethnically": "ethnic",
    "battleground": ["battle", "ground"],
    "untreated": ["un-", "treat"],
    "airway": ["air", "way"],
    "correctional": "correction",
    "experimenter": "experiment",
    "multimillion": ["multi-", "million"],
    "cameraman": ["camera", "man"],
    "airfield": ["air", "field"],
    "tabletop": ["table", "top"],
    "eagerness": "eager",
    "overestimate": ["over-", "estimate"],
    "stockholder": ["stock", "holder"],
    "painkiller": ["pain", "kill", "-er"],
    "observational": "observation",
    "budgetary": "budget",
    "unregulated": ["un-", "regulate"],
    "fiberglass": ["fiber", "glass"],
    "hotline": ["hot", "line"],
    "unease": ["un-", "ease"],
    "convincingly": "convince",
    "unspecified": ["un-", "specify"],
    "wearily": "weary",
    "wrapping": "wrap",
    "issuer": "issue",
    "mountaintop": ["mountain", "top"],
    "goddamned": ["god", "damn"],
    "printout": ["print", "out"],
    "grudgingly": "grudge",
    "developmentally": "development",
    "floorboard": ["floor", "board"],
    "democratically": "democrat",
    "terminally": "terminal",
    "mountainside": ["mountain", "side"],
    "biosolids": ["bio-", "solid"],
    "airlock": ["air", "lock"],
    "sculptural": "sculpture",
    "streetlight": ["street", "light"],
    "conspicuously": "conspicuous",
    "footwear": ["foot", "wear"],
    "Brazilian": "Brazil",
    "integrative": "integrate",
    "midterm": ["mid-", "term"],
    "eyeglass": ["eye", "glass"],
    "caseload": ["case", "load"],
    "whitetail": ["white", "tail"],
    "seawater": ["sea", "water"],
    "doorman": ["door", "man"],
    "schoolhouse": ["school", "house"],
    "riverbank": ["river", "bank"],
    "shyness": ["shy", "-ness"],
    "trailhead": ["trail", "head"],
    "caseworker": ["case", "worker"],
    "rationally": "rational",
    "outpace": ["out", "pace"], 
    "hummingbird": ["humming", "bird"],
    "salespeople": ["sale", "people"],
    "racetrack": ["race", "track"],
    "strikeout": ["strike", "out"],
    "treetop": ["tree", "top"],
    "skyward": ["sky", "-ward"],
    "warplane": ["war", "plane"],
    "cottonwood": ["cotton", "wood"],
    "stockbroker": ["stock", "broker"],
    "violator": "violate",
    "interagency": ["inter-", "agency"],
    "scoreboard": ["score", "board"],
    "resell": ["re-", "sell"],
    "cordless": ["cord", "-less"],
    "streetcar": ["street", "car"],
    "airfare": ["air", "fare"],
    "nightstand": ["night", "stand"],
    "evaluator": "evaluate",
    "jumpsuit": ["jump", "suit"],
    "coursework": ["course", "work"],
    "Panamanian": ["Panama", "-ian"],
    "subsystem": ["sub-", "system"],
    "factly": "fact",
    "digitally": "digital",
    "leaguer": "league",
    "largemouth": ["large", "mouth"],
    "uneasiness": ["uneasy", "-ness"],
    "barbershop": ["barber", "shop"],
    "worshiper": "worship",
    "curbside": ["curb", "side"],
    "airspace": ["air", "space"],
    "storybook": ["story", "book"],
    "schoolyard": ["school", "yard"],
    "weariness": ["weary", "-ness"],
    "citywide": ["city", "wide"],
    "Darwinian": ["Darwin", "-ian"],
    "experimentally": "experimental",
    "crewman": ["crew", "man"],
    "gunpoint": ["gun", "point"],
    "cornstarch": ["corn", "starch"],
    "moviegoer": ["movie", "go"],
    "untested": ["un-", "test"],
    "grandkid": ["grand-", "kid"],
    "intergovernmental": ["inter-", "governmental"],
    "bookseller": ["book", "sell", "-er"],
    "songbird": ["song", "bird"],
    "sportswriter": ["sport", "write", "-er"],
    "truckload": ["truck", "load"],
    "crosstalk": ["cross", "talk"],
    "framer": ["frame", "-er"],
    "graphical": "graphic",
    "schoolwork": ["school", "work"],
    "strangeness": ["strange", "-ness"],
    "tailback": ["tail", "back"],
    "headboard": ["head", "board"],
    "councilman": ["council", "man"],
    "snowboard": ["snow", "board"],
    "supremely": "supreme",
    "retest": ["re-", "test"],
    "crosswise": ["cross", "wise"],
    "riverboat": ["river", "boat"],
    "criminally": "criminal",
    "unrecognized": ["un-", "recognize"],
    "airstrike": ["air", "strike"],
    "carmaker": ["car", "make", "-er"],
    "wristwatch": ["wrist", "watch"],
    "actuator": "actuate",
    "reassign": ["re-", "assign"],
    "rater": ["rate", "-er"],
    "discriminant": ["discriminate", "-ant"],
    "uncooked": ["un-", "cook"],
    "insensitivity": ["in-", "sensitive", "-ity"],
    "redraw": ["re-", "draw"],
    "boldness": ["bold", "-ness"],
    "cropland": ["crop", "land"],
    "finisher": ["finish", "-er"],
    "teacup": ["tea", "cup"],
    "jihadist": ["jihad", "-ist"],
    "hardcover": ["hard", "cover"],
    "dryness": ["dry", "-ness"],
    "soundbite": ["sound", "bite"],
    "digitize": ["digit", "-ize"],
    "friendliness": ["friend", "-ness"],
    "snugly": "snug",
    "underfunded": ["under", "fund"],
    "feathery": "feather",
    "conservatively": "conservative",
    "saltwater": ["salt", "water"],
    "chairmanship": ["chairman", "-ship"],
    "darkroom": ["dark", "room"],
    "radiologist": ["radiology", "-ist"],
    "coveralls": ["cover", "all"],
    "vacationer": ["vacation", "-er"],
    "infighting": ["in", "fighting"],
    "demographer": ["demography", "-er"],
    "preoperative": ["pre-", "operative"],
    "scorecard": ["score", "card"],
    "unraveled": "unravel",
    "upriver": ["up", "river"],
    "connectedness": ["connected", "-ness"],
    "pillowcase": ["pillow", "case"],
    "floodwaters": ["flood", "water"],
    "pancreatic": "pancrea",
    "floodplain": ["flood", "plain"],
    "newsman": ["news", "man"],
    "unscrew": ["un-", "screw"],
    "unopened": ["un-", "open", "-ed"],
    "handset": ["hand", "set"],
    "manhunt": ["man", "hunt"],
    "supplementation": ["supplement", "-ation"],
    "playback": ["play", "back"],
    "goodnight": ["good", "night"],
    "storeroom": ["store", "room"],
    "cooperatively": ["cooperative", "-ly"],
    "quarterfinal": ["quarter", "final"],
    "wiretap": ["wire", "tap"],
    "tightness": ["tight", "-ness"],
    "undersecretary": ["under-", "secretary"],
    "earphone": ["ear", "phone"],
    "washcloth": ["wash", "cloth"],
    "nakedness": ["naked", "-ness"],
    "vastness": ["vast", "-ness"],
    "brainchild": ["brain", "child"],
    "reconstructive": ["re-", "constructive"],
    "approvingly": ["approve", "-ing", "-ly"],
    "speechwriter": ["speech", "writer"],
    "startlingly": ["startle", "-ing", "-ly"],
    "backpacker": ["backpack", "-er"],
    "defenseman": ["defense", "man"],
    "junkyard": ["junk", "yard"],
    "Christmastime": ["Christmas", "time"],
    "nightlife": ["night", "life"],
    "jetliner": ["jet", "line", "-er"],
    "criminalize": ["criminal", "-ize"],
    "unhook": ["un-", "hook"],
    "divisional": ["division", "-al"],
    "undemocratic": ["un-", "democratic"],
    "downwind": ["down", "wind"],
    "escaping": ["escape", "-ing"],
    "paintbrush": ["paint", "brush"],
    "schoolmate": ["school", "mate"],
    "rockfish": ["rock", "fish"],
    "workbench": ["work", "bench"],
    "drumbeat": ["drum", "beat"],
    "Shakespearean": ["Shakespear", "-ean"],
    "colonizer": ["colonize", "-er"],
    "counterweight": ["counter-", "weight"],
    "Newtonian": ["Newton", "-ian"],
    "Sicilian": ["Sicily", "-ian"],
    "endoscopic": ["endoscopy", "-ic"],
    "airflow": ["air", "flow"]
}

"""
Why are there two "mm"s?
"""
abbreviations = [
    "PM", "mm", "PC", "GI", "IQ", "HMO", "GDP", "PhD", "DJ", 
    "MBA", "ANOVA", "mmm", "MP", "IPO", "APR", "ICU", "mm", "MRI",
    "CPA", "CFC", "ADHD"
]

special_words = [
    "mike",
    "IPod",
    "y''all",
    "Qaeda", # Al-Qaeda 是“基地”组织
    "Chechen",
    "Salvadoran",
    "shh",
    "ahh",
    "Likert",
    "Astrodome",
    "laissez", # "laissez faire" means "A policy of governmental non-interference in economic affairs"
    "naw",
]


# In[ ]:


def find_roots(word):
    all_roots = [word]
    if word in abbreviations + special_words:
        return all_roots
    
    if word in replace_dict.keys():
        word = replace_dict[word]
    
    words = word if isinstance(word, list) else [word]
    
    roots_lst = []
    for word in words:    
        word_url = base_url + "word/" + word
        content = get_content(word_url)
        if content is None or "Error 404 (Not Found)" in content: # if we haven't found the word
            url = base_url + "word/" + lemma(word)
            content = get_content(url)
            if content is None or "Error 404 (Not Found)" in content:
                url = find_top_search_result(word)
                if url is None:
                    if (word[(-3):] == "est" and superlative(word[:(-3)]) == word): # if it is in superlative form
                        url = find_top_search_result(word[:(-3)])
                    elif (word[(-2):] == "er" and comparative(word[:(-2)]) == word):
                        url = find_top_search_result(word[:(-2)])
                    else:
                        print("Warning: Didn't get top search result for", word)
                content = get_content(url)
                if content is None or "Error 404 (Not Found)" in content:
                    continue

        # Truncate content
        related_entries_index = content.find("Related Entries")
        content_truncate = content[:related_entries_index]

        matches = find_all_occurances(match_reg_exp, content_truncate) # here content is a byte string

        roots = extract_roots(matches)
        roots.append(word) # the word itself is obviously a related word
        roots_lst.append(roots)

    all_roots += list(set(itertools.chain(*roots_lst)))
    return list(set(all_roots))


# In[ ]:


"""
There are repeated words in word_freq_list, what do we do about it?
"""

word_freq_lst = read_lines("edited_word_freq_list.txt")

if debugging:
    start = 15000
    end = 1000000
    print("Debugging mode on: only process words between index %d and %d" % (start, end))
    word_freq_lst = word_freq_lst[start:end]

word_roots_dict = {}
for i in tqdm(range(len(word_freq_lst))):
    split = word_freq_lst[i].split("\t")
    assert len(split) == 3
    word = split[1]
    if "-" in word: # if it is a compound word with "-"
        roots = list(
            set(list(itertools.chain(*([find_roots(subword) for subword in word.split("-")])))))
    else:
        roots = find_roots(word)
    
#     if word in roots:
#         roots.remove(word)

    word_roots_dict[word] = roots


# In[ ]:


def replace_roots_recursive():
    changed = False
    for word in list(word_roots_dict.keys()):
        roots = word_roots_dict[word]
        for i in reversed(range(len(roots))):
            part = roots[i]
            if "-" not in part and "*" not in part: # we shouldn't extract related words of roots
                try:
                    word_roots_dict[word][i: (i + 1)] = word_roots_dict[part]
                    word_roots_dict[word] = list(set(word_roots_dict[word]))
                    changed = True
                except:
                    pass
    return changed

max_iter = 5
for i in range(max_iter):
    changed = replace_roots_recursive()
    if not changed:
        print("Nothing changed after %d iterations." % i)
        break


# In[ ]:


# word_roots_dict = load_pickle("word_roots_dict.pkl")
str_lines = []
for line in list(word_roots_dict.items()):
    str_lines.append(line[0] + "\t" + ", ".join(line[1]))
write_lines("word_roots_dict.txt", str_lines)
dump_pickle("word_roots_dict.pkl", word_roots_dict)


# In[ ]:


all_roots = list(itertools.chain(*list(word_roots_dict.values())))
freq_dist = nltk.FreqDist(all_roots).most_common()
write_lines("root_freq_dist.txt", freq_dist)
dump_pickle("root_freq_dist.pkl", freq_dist)
# print(freq_dist)


# In[ ]:




