import yaml
from pprint import pprint

with open('book.yml') as fp:
    x = yaml.safe_load(fp)
pprint(x)
