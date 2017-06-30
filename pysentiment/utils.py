'''
This module contains methods to tokenize sentences.
'''
import abc
import re
import nltk


class BaseTokenizer(object):

    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def tokenize(self, text):
        pass


class Tokenizer(BaseTokenizer):

    def __init__(self):
        self._stemmer = nltk.PorterStemmer()
        self._stopset = self.get_stopset()
        
    def tokenize(self, text):
        tokens = []
        for t in nltk.regexp_tokenize(text.lower(), '[a-z]+'):
            t = self._stemmer.stem(t)
            if not t in self._stopset:
                tokens.append(t)
        return tokens
        
    def get_stopset(self):
        from pysentiment.base import STATIC_PATH
        files = ['Currencies.txt', 'DatesandNumbers.txt', 'Generic.txt', 'Geographic.txt',
                 'Names.txt']
        stopset = set()
        for f in files:
            fin = open('%s/%s'%(STATIC_PATH, f), 'rb')
            for line in fin.readlines():
                line = line.decode(encoding='latin-1')
                match = re.search('(\w+)', line)
                if match == None:
                    continue
                word = match.group(1)
                stopset.add(self._stemmer.stem(word.lower()))
            fin.close()
        return stopset
