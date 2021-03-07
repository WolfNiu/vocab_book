from tqdm import tqdm
import json
import os
from util import get_driver, read_lines, dump_pickle

URL = "https://www.collinsdictionary.com/us/dictionary/english/"
XPATH = {
    "pos": '//span[@class="gramGrp pos"]',
    "meaning": '//div[@class="def"]',
    "sent": '//div[@class="cit type-example quote"]',
}

lines = read_lines('sorted_importance.txt')

driver = get_driver(headless=True)
if os.path.exists('book.json'):
    with open('book.json') as fp:
        dictionary = json.load(fp)
else:
    dictionary = {}

for i, line in enumerate(tqdm(lines)):
    word, freq, use = line.split()[:3]
    if word not in dictionary:
        dictionary[word] = {
            'freq': freq,
            'use': use,
        }
        driver.get(URL + word.lower())
        for key, xpath in XPATH.items():
            try:
                text = driver.find_element_by_xpath(xpath).text
                dictionary[word][key] = text
            except Exception as e:
                # print(e)
                pass
    if i % 100 == 99:
        with open('book.json', 'w') as fp:
            json.dump(dictionary, fp)

with open('book.json', 'w') as fp:
    json.dump(dictionary, fp)

driver.quit()
