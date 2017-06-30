import pysentiment as ps
from pycorenlp import StanfordCoreNLP
import json
import pandas as pd
from objective_facts.objective_facts import objective_facts, parse_insult,retrieve_tags
from keywords_extraction import rake
import operator
from analytical_emotional.analytics import affective_vs_analytic, count_punctuation, me_in_text
from naiveBayesClassifier.classifier import Classifier
import zipfile
import pickle
import os 

## direction
dir_path = os.path.dirname(os.path.realpath(__file__))

### setup
hiv4 = ps.HIV4()
scnlp = StanfordCoreNLP('http://localhost:9000')

with open(dir_path+'/naiveBayesClassifier/newsclassifier.pkl', 'rb') as df:
    newsClassifier = pickle.load(df)

rake_object = rake.Rake(dir_path + "/keywords_extraction/SmartStoplist.txt")


### Changement of Date
month = ['Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_i = ['01','02','03','04','05','06','07','08','09','10','11','12']

dir_path2 = os.path.dirname(dir_path)
print dir_path2
## tagging
for count in range(1,10000) :
    try : 
        with open(dir_path2 + '/input/guardian_articles/'+str(count)+'.json','r') as df:
            article = json.load(df)
            if article.get('text') is not None :
                print count
                text = str(article.get('text').encode('ascii', 'ignore'))

                ## Objective Facts
                date = article.get('date')
                if date[3:6] in month : 
                    date = date[:3] + month_i[month.index(date[3:6])] + date[6:]
                else :
                    date = article.get('date')
                tags = retrieve_tags(article.get('tags'))

                d = {
                'date' : date, 
                'title': article.get('title').encode('utf8'), 
                'author': article.get('author'),
                'text' : text,
                'tags' : list(set([x.encode('utf8') for x in tags])),
                'locations' : list(set([x.encode('utf8') for x in objective_facts(text)[0]])),
                'dates' : list(set([x.encode('utf8') for x in objective_facts(text)[3]])),
                'people' : list(set([x.encode('utf8') for x in objective_facts(text)[2]])),
                'organisations' : list(set([x.encode('utf8') for x in objective_facts(text)[1]]))
                }
                text = text.lower()
                d['insults'] = list(set([x.encode('utf8') for x in parse_insult(text)]))
                
                ## emotions
                tokens = hiv4.tokenize(text)
                dependencies = hiv4.dependencies(text)
                score = hiv4.get_emotions(tokens,dependencies)
                d.update(score)

                ## Sections
                if 'url' in article.keys() : 
                    url =  article.get('url')
                    d.update({'url' : url})

                    if 'opinion' in url :
                        d.update({'section' : 'opinion'})
                    if 'business' in url :
                        d.update({'section' : 'business'})
                    if 'politics' in url :
                        d.update({'section' : 'politics'})
                    if 'world' in url :
                        d.update({'section' : 'world'})
                    else :
                        d.update({'section' : 'other'})

                ## Affective vs Analytical
                d.update({'analytical vs affective' : affective_vs_analytic(text)})
                d.update(me_in_text(text))
                d.update(count_punctuation(text))

                ## Theme classification
                keywords = rake_object.run(text)
                keys = []
                if len(keywords) > 15 : 
                    l = 15
                else :
                    l = len(keywords)

                for i in range(l) :
                    keys.append(keywords[i][0])

                classification = newsClassifier.classify(' '.join(keys)) 
                if classification[0][1] == 0 :
                    d.update({'theme' : 'not dertimined'})
                else : 
                    if classification[1][1] / (classification[0][1] + 0.000000001) > 0.1 :
                        d.update({'theme' : classification[0][0] + ' ' + classification[1][0]})
                    else :
                        d.update({'theme' : classification[0][0]})

                if count < 10 :
                    with open(dir_path2+'/output/guardian_articles/0/0/'+str(count)+'/'+str(count)+'.json','w') as data_file :
                        json.dump(d,data_file)
                elif 10 <= count < 100 : 
                    with open(dir_path2+'/output/guardian_articles/0/'+str(count)[0]+'/'+str(count)[1]+'/'+str(count)+'.json','w') as data_file :
                        json.dump(d,data_file)
                else : 
                    with open(dir_path2+'/output/guardian_articles/'+str(count)[0]+'/'+str(count)[1]+'/'+str(count)[2]+'/'+str(count)+'.json','w') as data_file :
                        json.dump(d,data_file)
    except :
        pass