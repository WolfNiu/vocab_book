"""
TODO:
1. When citing word exchanges, it is better to present the alignment. Design this!
2. Each PIE root or letter-exchange rule should have its own (initial) explanation!

entry: word --> pos, frequency, importance, meaning, sentence, [root], explanation, related_forms
roots (OrderedDict): root --> pie (which may itself has a parent)
pie: pie --> meaning, intro (optional)
related_forms: [word --> sentence, hint]
"""
import os
from collections import OrderedDict
from util import load_pickle


class Entry(object):
    def __init__(self,
                 word, frequency, importance, sentence,
                 pos=None,
                 meaning=None,
                 part2root=None,
                 explanations=None,
                 figures=None,
                 related_forms=[]):
        self.word = word
        self.pos = pos
        self.frequency = frequency
        self.importance = importance
        self.meaning = meaning
        self.sentence = sentence
        self.part2root = part2root # An OrderDict()
        self.explanations = explanations
        self.figures = figures
        self.related_forms = related_forms

    def _get_root_line(self):
        root_line = ''
        for root, pie in self.root2pie.items():
            root_line += f'({root}'


    def __repr__(self):
        root_line = self._get_root_line()
        lines = [
            'word',
            '------------------------',
            f'{self.meaning}',
            f'{self.sentence}',
            root_line,
            self.explanation,
        ]
            'Related forms:'

        )
        return '\n'.join(lines)

    @property
    def root_dict(self):
        if not hasattr(self, '_root_dict'):
            self._root_dict =
        return self._root2pie

class Dictionary(object):
    def __init__(self):
        pass

    @property
    def words(self):
        if not hasattr(self, '_words'):
            pass
        return self._words

    @property
    def root2root(self):
        """
        root --> root
        """
        if not hasattr(self, '_root_dict'):
            file = 'root_dict.pkl'
            if os.path.exists(file):
                self._root_dict = load_pickle(file)
            else:
                self._root_dict = {}
        return self._root_dict

    @property
    def root2meaning_exp(self):
        """
        root --> meaning, explanation
        """

    @property
    def exchange_dict(self):
        """
        frozenset(exchangable_letters) --> explanation
        """
        if not hasattr(self, '_exchange_dict'):
            file = 'exchange_dict.pkl'
            if os.path.exists(file):
                self._exchange_dict = load_pickle(file)
            else:
                self._exchange_dict = {}
        return self._exchange_dict

if __name__ == '__main__':
    while True:
        cmd = input('')
        if cmd == 'exit':
            break
