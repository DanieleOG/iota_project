import pysentiment as ps
import json
import pandas as pd
import zipfile
import pickle
import os 
from objective_facts.objective_facts import parse_insult

## direction
dir_path = os.path.dirname(os.path.realpath(__file__))

### setup
hiv4 = ps.HIV4()

dir_path2 = os.path.dirname(dir_path)
print dir_path2
## tagging
for count in range(1,5000) :
    try : 
        with open(dir_path2 + '/input/comments/'+str(count)+'.json','r') as df:
            comment = json.load(df)
            if comment.get('text') is not None :
                print count
                text = str(comment.get('text').encode('ascii', 'ignore'))

                ## Objective Facts
                date = comment.get('date')
                if date[3:6] in month : 
                    date = date[:3] + month_i[month.index(date[3:6])] + date[6:]
                else :
                    date = comment.get('date')
                tags = retrieve_tags(comment.get('tags'))

                d = {
                'date' : date, 
                'text' : text,
                }
                text = text.lower()
                d['insults'] = list(set([x.encode('utf8') for x in parse_insult(text)]))
                
                ## emotions
                tokens = hiv4.tokenize(text)
                dependencies = hiv4.dependencies(text)
                score = hiv4.get_emotions(tokens,dependencies)
                d.update(score)



                if count < 10 :
                    with open(dir_path2+'/output/guardian_comments/0/0/'+str(count)+'/'+str(count)+'.json','w') as data_file :
                        json.dump(d,data_file)
                elif 10 <= count < 100 : 
                    with open(dir_path2+'/output/guardian_comments/0/'+str(count)[0]+'/'+str(count)[1]+'/'+str(count)+'.json','w') as data_file :
                        json.dump(d,data_file)
                else : 
                    with open(dir_path2+'/output/guardian_comments/'+str(count)[0]+'/'+str(count)[1]+'/'+str(count)[2]+'/'+str(count)+'.json','w') as data_file :
                        json.dump(d,data_file)
    except :
        pass