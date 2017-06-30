import json
import os 

## direction
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path+'/liwc.json','r') as df : 
	data = json.load(df)

words = [d.get('word') for d in data]

def affective_vs_analytic(text) :
	affective = 0
	analytic = 0
	text = text.split(" ")
	for word in text :
		if word in words : 
			idx = words.index(word)
			catesgories = data[idx].get('cat')
			if 'affect' in catesgories or 'percept' in catesgories or 'negemo' in catesgories\
			or 'posemo' in catesgories or 'feel' in catesgories: 
				affective += 1
			if 'funct' in catesgories or 'insight' in catesgories or 'cogmech' in catesgories\
			or 'quant' in catesgories or 'cause' in catesgories : 
				analytic += 1
	return (affective - analytic)/ (affective + analytic + 0.00000000000001)


def count_punctuation(text) :
	text = text.split(" ")
	exclamation = 0
	interogation = 0
	suspens = 0
	for word in text :
		if word == '?' :
			interogation += 1
		if word == '!' :
			exclamation += 1
		if word == '...' :
			suspens += 1
	return {'nb_exclamation' : exclamation, 'nb_interogation' : interogation, 'nb_suspens' : suspens }

def me_in_text(text) :
	pronouns = ["I", "me", "my", "mine", "myself", "us", "our", "ours", "ourself", "ourselves"]
	for pronoun in pronouns : 
		if pronoun in text :
			return {'point of view' : 'True'}
	return {'point of view' : 'False'}


	 

