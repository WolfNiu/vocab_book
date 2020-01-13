"""
entry: word --> pos, frequency, importance, meaning, sentence, [root], explanation, related_forms
root: root --> pie (which may itself has a parent)
pie: pie --> meaning, intro (optional)
related_forms: [word --> sentence, hint]
"""

from collections import OrderedDict, namedtuple
from util import load_pickle

class Dictionary(object):
    def __init__(self):
        pass

    @property
    def pie2meaning(self):
        if not hasattr(self, '_pie2meaning'):
            file = 'pie2meaning.pkl'
            if os.path.exists(file):
                self._pie2meaning = load_pickle(file)
            else:
                self._pie2meaning = {}
        return self._pie2meaning

if __name__ == '__main__':
    while True:
        cmd = input('')
        if cmd == 'exit':
            break

