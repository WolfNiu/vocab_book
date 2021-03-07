import simplejson
import json
import yaml
import jsonlines
from tqdm import tqdm
import os


def load_jsonl(input_path):
    """
    Read list of objects from a JSON lines file.
    """
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        buffer = []
        for i, line in enumerate(tqdm(f)):
            line = line.strip()
            buffer.append(line)
            if line == '}':
                string = ' '.join(buffer)
                entry = json.loads(string)
                entry['freq'] = int(entry['freq'])
                entry['use'] = int(entry['use'])
                data.append(entry)
                buffer = []

    print('Loaded {} records from {}'.format(len(data), input_path))
    return data

entries = load_jsonl('book_original.jsonl')
print(entries[0])

with open('./book_original.yml', 'w', encoding='utf-8') as fp_yaml:
    yaml.dump(entries, fp_yaml, default_flow_style=False, sort_keys=False)

"""
TODO: figure out how to dump yaml file with OrderedDict 
(https://stackoverflow.com/questions/31605131/dumping-a-dictionary-to-a-yaml-file-while-preserving-order/31609484)
"""