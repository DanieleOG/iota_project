#!/usr/bin/python
# -*- coding: ascii -*-

from naiveBayesClassifier.tokenizer import Tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier
import numpy as np
import re
import itertools
from collections import Counter
import nltk
from pprint import pprint
import pickle
from nltk.tokenize import RegexpTokenizer
import rake
import os 

## direction
dir_path = os.path.dirname(os.path.realpath(__file__))

rake_object = rake.Rake(dir_path+'/../keywords_extraction/SmartStoplist.txt')
tokenizer = RegexpTokenizer(r'\w+')

def clean_str(string):

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels():

    # Load data from files
    crime_examples = list(open("data_nlp/crime.txt",'r').readlines())
    crime_examples = [s.strip() for s in crime_examples]
    discrimination_examples = list(open("data_nlp/discrimination.txt",'r').readlines())
    discrimination_examples = [s.strip() for s in discrimination_examples]
    business_examples = list(open("data_nlp/business.txt",'r').readlines())
    business_examples = [s.strip() for s in business_examples]
    economy_examples = list(open("data_nlp/economy.txt",'r').readlines())
    economy_examples = [s.strip() for s in economy_examples]
    banking_examples = list(open("data_nlp/banking.txt",'r').readlines())
    banking_examples = [s.strip() for s in banking_examples]
    climate_examples = list(open("data_nlp/energy.txt",'r').readlines())
    climate_examples = [s.strip() for s in climate_examples]
    medical_examples = list(open("data_nlp/health.txt",'r').readlines())
    medical_examples = [s.strip() for s in medical_examples]
    sex_examples = list(open("data_nlp/sex.txt",'r').readlines())
    sex_examples = [s.strip() for s in sex_examples]
    media_examples = list(open("data_nlp/media.txt",'r').readlines())
    media_examples = [s.strip() for s in media_examples]
    military_examples = list(open("data_nlp/military.txt",'r').readlines())
    military_examples = [s.strip() for s in military_examples]
    trade_examples = list(open("data_nlp/trade.txt",'r').readlines())
    trade_examples = [s.strip() for s in trade_examples]
    money_examples = list(open("data_nlp/money1.txt",'r').readlines()) + list(open("data_nlp/money2.txt",'r').readlines())
    money_examples = [s.strip() for s in money_examples]
    elections_examples = list(open("data_nlp/elections.txt",'r').readlines()) + list(open("data_nlp/election_uk.txt",'r').readlines())
    elections_examples = [s.strip() for s in elections_examples]
    education_examples = list(open("data_nlp/education.txt",'r').readlines())
    education_examples = [s.strip() for s in education_examples]
    justice_examples = list(open("data_nlp/justice.txt",'r').readlines())
    justice_examples = [s.strip() for s in justice_examples]
    EU_examples = list(open("data_nlp/EU.txt",'r').readlines())
    EU_examples = [s.strip() for s in EU_examples]

    # Split by words
    x_text = crime_examples + discrimination_examples + business_examples + economy_examples + banking_examples\
    + climate_examples + medical_examples + sex_examples + media_examples + military_examples + trade_examples +\
    money_examples + elections_examples + education_examples + justice_examples + EU_examples
    x_text = [clean_str(sent) for sent in x_text]
    x_text = [' '.join([k[0] for k in rake_object.run(text) if k[1] > 1]) for text in x_text]
    
    # Generate labels
    crime_labels = ['crime' for _ in crime_examples]
    discrimination_labels = ['discrimination' for _ in discrimination_examples]
    business_labels = ['money' for _ in business_examples]
    economy_labels = ['money' for _ in economy_examples]
    banking_labels = ['money' for _ in banking_examples]
    climate_labels = ['energy' for _ in climate_examples]
    medical_labels = ['health' for _ in medical_examples]
    sex_labels = ['sex' for _ in sex_examples]
    media_labels = ['media' for _ in media_examples]
    military_labels = ['military' for _ in military_examples]
    trade_labels = ['money' for _ in trade_examples]
    money_labels = ['money' for _ in money_examples]
    elections_labels = ['elections' for _ in elections_examples]
    education_labels = ['education' for _ in education_examples]
    justice_labels = ['justice' for _ in justice_examples]
    EU_labels = ['EU' for _ in EU_examples]


    y = np.concatenate([crime_labels, discrimination_labels, business_labels, economy_labels,\
        banking_labels, climate_labels, medical_labels, sex_labels, media_labels,\
        military_labels, trade_labels, money_labels, elections_labels, education_labels, justice_labels, EU_labels], 0)
    return [x_text, y]

newsTrainer = Trainer()

newsSet = load_data_and_labels()
for i in range(len(newsSet[0])):
	newsTrainer.train(newsSet[0][i], newsSet[1][i])

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

newsClassifier = Classifier(newsTrainer.data)

save_object(newsClassifier, 'newsclassifier.pkl')

