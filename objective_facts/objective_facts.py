import pysentiment as ps
from pycorenlp import StanfordCoreNLP
import json
import pandas as pd
import os 

## direction
dir_path = os.path.dirname(os.path.realpath(__file__))

scnlp = StanfordCoreNLP('http://localhost:9000')

insults = []
with open(dir_path+'/insults.csv','r') as data_file :
    for line in data_file.readlines() :
        line = line.replace('\r','').replace('\n','')
        insults.append(line)

##################################### objective facts #####################################
def objective_facts(text) :
    locations = []
    organizations = []            
    people = []            
    dates = []
    output = scnlp.annotate(text, properties={'annotators': 'ner','outputFormat': 'json'})
    sentences = output[u'sentences']
    for sentence in sentences : 
        tokens = sentence.get(u'tokens')
        for i in range(0,len(tokens)) :
            if tokens[i].get('ner') == 'LOCATION' :
                if tokens[i-1].get('ner') == 'LOCATION' :
                    locations[len(locations)-1] += ' '+tokens[i].get('originalText')
                else :
                    locations.append(tokens[i].get('originalText'))
            if tokens[i].get('ner') == 'ORGANIZATION' :
                if tokens[i-1].get('ner') == 'ORGANIZATION' :
                    organizations[len(organizations)-1] += ' '+tokens[i].get('originalText')
                else :
                    organizations.append(tokens[i].get('originalText'))
            if tokens[i].get('ner') == 'PERSON' :
                if tokens[i-1].get('ner') == 'PERSON' :
                    people[len(people)-1] += ' '+tokens[i].get('originalText')
                else :
                    people.append(tokens[i].get('originalText'))
            if tokens[i].get('ner') == 'DATE':
                if  tokens[i-1].get('ner') == 'DATE' :
                    dates[len(dates)-1] += ' '+tokens[i].get('originalText')
                else :
                    dates.append(tokens[i].get('originalText'))
    return [locations,organizations,people,dates]

def retrieve_tags(tag):
    tags = []
    if tag is not None :
        for t in tag :
            if isinstance(t, dict):
                tags.append(t.get(u'label'))
            else : 
                tags = tag  
    return tags

def parse_insult(text) :
    insults_retrieved =[]
    for insult in insults:
        if ' '+insult+' ' in text :
            insults_retrieved.append(insult)
    return insults_retrieved
