import json

def dump_jsonl(data, output_path, append=False):
    """
    Write list of objects to a JSON lines file.
    """
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, indent=4, ensure_ascii=False)
            f.write(json_record + '\n')
    print('Wrote {} records to {}'.format(len(data), output_path))

def load_jsonl(input_path):
    """
    Read list of objects from a JSON lines file.
    """
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.rstrip('\n|\r')))
    print('Loaded {} records from {}'.format(len(data), input_path))
    return data

from collections import OrderedDict
from pprint import pformat
from util import write_lines

# with open('book_backup.json', encoding='utf-8') as fp:
#     book = json.load(fp)
#
# for k, v in book.items():
#     v['roots'] = {}
#     v['exp'] = ''
#     v['figure'] = ''
#     v['related'] = []
#
# with open('book_backup.json', 'w', encoding='utf-8') as fp:
#     json.dump(book, fp, indent=2)
#
# with open('book.json', encoding='utf-8') as fp:
#     book = json.load(fp)
# for k, v in book.items():
#     if 'figure' not in 'v':
#         v['figure'] = ''
#     if 'related' not in 'v':
#         v['related'] = []
#     if 'exp' in v:
#         v['exp'] = v['exp'].encode('utf-8').decode('utf-8')
#     if 'figure' in v:
#         v['figure'] = v['figure'].encode('utf-8').decode('utf-8')
#
# with open('book.json', 'w', encoding='utf-8') as fp:
#     json.dump(book, fp, indent=2)

# data = []
# for k, v in book.items():
#     x = OrderedDict()
#     x['word'] = k
#     x.update(v)
#     # s = pformat(dict(x), sort_dicts=False)
#     data.append(x)
#
# dump_jsonl(data, 'book.jsonl')
# write_lines('book.jsonl', data)

# x = load_jsonl('book.jsonl')
# x[0]
