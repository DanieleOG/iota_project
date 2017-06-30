from naiveBayesClassifier.trainedData import TrainedData
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import RegexpTokenizer

stop = set(stopwords.words('english'))

class Trainer():

    """docstring for Trainer"""
    def __init__(self):
        #super(Trainer, self).__init__()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.data = TrainedData()

    def train(self, text, className):
        """
        enhances trained data using the given text and class
        """
        self.data.increaseClass(className)

        tokens = self.tokenizer.tokenize(text)
        tokens = [token for token in tokens if token not in stop]
        tokens = [x[0] for x in nltk.pos_tag(tokens) if 'VB' not in x[1] or 'DT' not in x[1] or 'IN' not in x[1] or 'W' not in x[1]]

        for token in tokens:
            self.data.increaseToken(token, className)
