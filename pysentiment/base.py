import abc
import os
import json
from pysentiment.utils import Tokenizer
from math import exp

from nltk.parse.stanford import StanfordDependencyParser
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

os.environ['STANFORD_PARSER'] = dir_path+'/../stanford-parser-full-2015-04-20/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = dir_path+'/../stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'

dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


STATIC_PATH = os.path.dirname(__file__)+'/lexicons_sub'

anew_path = '%s/anew.json' % STATIC_PATH

with open(anew_path,'r') as data_file :
    anew = json.load(data_file)

class BaseDict(object):

    __metaclass__ = abc.ABCMeta

    EPSILON = 1e-6
    
    def __init__(self, tokenizer=None):

        ### comparisons
        self._posset = set()
        self._negset = set()

        self._affset = set()
        self._hosset = set()

        self._strset = set()
        self._weaset = set()

        self._actset = set()
        self._passet = set()

        self._pleset = set()
        self._paiset = set()

        self._virset = set()
        self._vicset = set()

        self._ovtset = set()
        self._udtset = set()

        ### Rectitude
        self._rceset = set()
        self._rcrset = set()

        ### Emotions & trust, anticipation, suprise
        self._angset = set()
        self._truset = set()
        self._sadset = set()
        self._joyset = set()
        self._antset = set()
        self._disset = set()
        self._feaset = set()
        self._surset = set()

        if tokenizer is None:
            self._tokenizer = Tokenizer()
        else:
            self._tokenizer = tokenizer
        self.init_dict()
        
        assert len(self._posset) > 0 and len(self._negset) > 0
        
    def tokenize(self, text):
        return self._tokenizer.tokenize(text)

    def dependencies(self,text) :
        sentences = text.split('. ')
        neg_dependencies = []
        for s in sentences : 
            result = dep_parser.raw_parse(s+'.')
            dep = result.next()
            res = list(dep.triples())
            for r in res :
                if 'neg' in r[1] :
                    if 'RB' not in r[0][1] :
                        neg_dependencies.append(r[0][0])
                    if 'RB' not in r[1][1] :
                        neg_dependencies.append(r[1][0])
        return neg_dependencies

    @abc.abstractmethod
    def init_dict(self):
        pass
    
    def _get_score(self, term, list1,list2):
        if term in list1 :
            return +1
        elif term in list2:
            return -1
        else:
            return 0

    def _get_esperance(self,liste) :
        liste = [0.125*(x - 1) for x in liste]
        return sum(liste)/(len(liste)+self.EPSILON)

    def _pola(self,liste,s=False) :
        pos = sum([s for s in liste if s > 0])
        neg = sum([s for s in liste if s < 0]) * -1
        return [(pos-neg) * 1.0 / ((pos+neg)+self.EPSILON), (pos+neg) * 1.0 / (len(liste) +self.EPSILON)]

    def _get_intensity(self,liste,terms, dependencies) : 
        score_wea_str = [self._get_score(t,self._strset,self._weaset) for t in terms if t in liste]
        score_act_pass = [self._get_score(t,self._actset,self._passet) for t in terms if t in liste]
        score_ovt_udt = [self._get_score(t,self._ovtset,self._udtset) for t in terms if t in liste]
        arousal_neg = [anew.get(t).get('arousal_mean') for t in terms if t in anew.keys() and t in liste and t in dependencies]
        arousal_pos = [anew.get(t).get('arousal_mean') for t in terms if t in anew.keys() and t in liste and t not in dependencies]

        s_wea_str = self._pola(score_wea_str)[0]
        s_ovt_udt = self._pola(score_ovt_udt)[0]
        s_act_pass = self._pola(score_act_pass)[0]
        arousal = (len(arousal_pos)*self._get_esperance(arousal_pos) - self._get_esperance(arousal_neg)*len(arousal_neg))/(len(arousal_pos+arousal_neg) + self.EPSILON)

        intensity = float((s_wea_str + s_ovt_udt + s_act_pass + 3)*0.083 + 0.5*arousal) # weight 0.5 arousal, weight .5 for 3 others and changement of interval -1,1 to 0,1 so 0.5(x+1)

        return intensity

    def get_emotions(self, terms, dependencies):
        assert isinstance(terms, list) or isinstance(terms, tuple)

        ############################## Calculate Polarity & Subjectivity #####################################


        s_pos_neg = self._pola([self._get_score(t,self._posset,self._negset) for t in terms ])[0] # positive vs negative
        s_aff_hos = self._pola([self._get_score(t,self._affset,self._hosset) for t in terms ])[0] # affiliation vs hostility
        s_vir_vic = self._pola([self._get_score(t,self._virset,self._vicset) for t in terms ])[0] # virtue vs vice
        s_ple_pai = self._pola([self._get_score(t,self._pleset,self._paiset) for t in terms ])[0] # pleasure vs pain

        valence = self._get_esperance([anew.get(t).get('valence_mean') for t in terms if t in anew.keys()])

        kind_emotions = (s_pos_neg + s_aff_hos + s_ple_pai +s_vir_vic + valence)*0.25

        s_sub = self._pola([self._get_score(t,self._posset,self._negset) for t in terms ])[1]
        
        #################################### Calculate Intensity ############################################
        for liste in [self._angset, self._sadset,self._joyset,self._disset,self._feaset,self._truset, self._antset, self._surset] :
            
            intensity= self._get_intensity(liste,terms,dependencies)

            if liste == self._angset :
                anger_nw = len([t for t in terms if t in liste])
                if anger_nw < 1 :
                    anger = 0
                else : 
                    anger = intensity
                
            if liste == self._sadset :
                sadness_nw = len([t for t in terms if t in liste])
                if sadness_nw < 1 : 
                    sadness = 0
                else : 
                    sadness = intensity
                
            if liste == self._joyset :
                joy_nw = len([t for t in terms if t in liste])
                if joy_nw < 1 : 
                    joy = 0
                else : 
                    joy = intensity
                
            if liste == self._disset :
                disgust_nw = len([t for t in terms if t in liste])
                if disgust_nw < 1 :
                    disgust = 0
                else : 
                    disgust = intensity
                
            if liste == self._feaset :
                fear_nw = len([t for t in terms if t in liste])
                if fear_nw < 1 :
                    fear = 0
                else : 
                    fear = intensity
                
            if liste == self._truset :
                trust_polarity = self._pola([self._get_score(t,self._posset,self._negset) for t in terms if t in self._truset])
                if trust_polarity < 0 : 
                    trust = -1*intensity
                else :
                    trust = intensity

            if liste == self._antset :
                anticipation_nw = len([t for t in terms if t in liste])
                if anticipation_nw < 1 :
                    anticipation = 0
                else : 
                    anticipation = intensity
                
            if liste == self._surset :
                surprise_nw = len([t for t in terms if t in liste])                
                if surprise_nw < 1 : 
                    surprise = 0
                else :
                    surprise = intensity

        ############################### Principal Emotion & Intensity ###############################
        emotions_int = [anger,sadness,joy,disgust,fear]
        emotions_str = ['anger','sadness','joy','disgust','fear']
        emotions_nbw = [anger_nw,sadness_nw,joy_nw,disgust_nw,fear_nw]
        emotions_nbw1, emotions_int = (list(t) for t in zip(*sorted(zip(emotions_nbw, emotions_int),reverse=True)))
        emotions_nbw, emotions_str = (list(t) for t in zip(*sorted(zip(emotions_nbw, emotions_str),reverse=True)))

        principal_emotion = ''
        if 20 >= emotions_nbw[0] >= 10 :
            if emotions_nbw[0] - emotions_nbw[1] > 5 :
                principal_emotion = emotions_str[0]
                intensity = emotions_int[0]
            else :
                if (emotions_str[0] == 'fear' and emotions_str[1] == 'disgust') or \
                (emotions_str[0] == 'disgust' and emotions_str[1] == 'fear') : 
                    maxi,mini = max(emotions_int[1],emotions_int[0]), min(emotions_int[1],emotions_int[0])
                    if float(mini/(maxi+self.EPSILON)) > 0.3 : 
                        principal_emotion = 'shame'
                        intensity = mini

                elif (emotions_str[0] == 'joy' and emotions_str[1] == 'fear') or \
                (emotions_str[0] == 'fear' and emotions_str[1] == 'joy') : 
                    maxi,mini = max(emotions_int[1],emotions_int[0]), min(emotions_int[1],emotions_int[0])
                    if float(mini/(maxi+self.EPSILON)) > 0.3 : 
                        principal_emotion = 'guilt'
                        intensity = mini

                elif (emotions_str[0] == 'joy' and emotions_str[1] == 'anger') or \
                (emotions_str[0] == 'anger' and emotions_str[1] == 'joy') : 
                    maxi,mini = max(emotions_int[1],emotions_int[0]), min(emotions_int[1],emotions_int[0])
                    if float(mini/(maxi+self.EPSILON)) > 0.3 : 
                        principal_emotion = 'pride'
                        intensity = mini
                else : 
                    if emotions_int[0] > emotions_int[1] :
                        principal_emotion = emotions_str[0]
                        intensity = emotions_int[0]
                    else :
                        principal_emotion = emotions_str[1]
                        intensity = emotions_int[1]

        if emotions_nbw[0] > 20 :
            if emotions_nbw[0] - emotions_nbw[1] > 10 : 
                principal_emotion = emotions_str[0]
                intensity = emotions_int[0]
            else :
                if (emotions_str[0] == 'fear' and emotions_str[1] == 'disgust') or \
                (emotions_str[0] == 'disgust' and emotions_str[1] == 'fear') : 
                    maxi,mini = max(emotions_int[1],emotions_int[0]), min(emotions_int[1],emotions_int[0])
                    if float(mini/(maxi+self.EPSILON)) > 0.3 : 
                        principal_emotion = 'shame'
                        intensity = mini

                elif (emotions_str[0] == 'joy' and emotions_str[1] == 'fear') or \
                (emotions_str[0] == 'fear' and emotions_str[1] == 'joy') : 
                    maxi,mini = max(emotions_int[1],emotions_int[0]), min(emotions_int[1],emotions_int[0])
                    if float(mini/(maxi+self.EPSILON)) > 0.3 : 
                        principal_emotion = 'guilt'
                        intensity = mini

                elif (emotions_str[0] == 'joy' and emotions_str[1] == 'anger') or \
                (emotions_str[0] == 'anger' and emotions_str[1] == 'joy') : 
                    maxi,mini = max(emotions_int[1],emotions_int[0]), min(emotions_int[1],emotions_int[0])
                    if float(mini/(maxi+self.EPSILON)) > 0.3 : 
                        principal_emotion = 'pride'
                        intensity = mini
                else : 
                    if emotions_int[0] > emotions_int[1] :
                        principal_emotion = emotions_str[0]
                        intensity = emotions_int[0]
                    else :
                        principal_emotion = emotions_str[1]
                        intensity = emotions_int[1]
                
        if 10 >= emotions_nbw[0] >= 5 : 
            emotions_int, emotions_str = (list(t) for t in zip(*sorted(zip(emotions_int, emotions_str),reverse=True)))
            principal_emotion = emotions_str[0]
            intensity = emotions_int[0]
        
        if 5 > emotions_nbw[0] > 0 :
            if emotions_nbw[1] == 0:
                principal_emotion = emotions_str[0]
                intensity = emotions_int[0]

            else :
                principal_emotion = 'Mixed Emotions'
                intensity = float(sum(emotions_int)/len(emotions_int))

        if emotions_nbw[0] == 0:
            principal_emotion = 'Neutral'
            intensity = 0


        return {'subjectivity': s_sub,
                'principal emotion' : principal_emotion,
                'intensity' : intensity,
                'anger': anger,
                '# words anger' : anger_nw,
                'trust': trust,
                'sadness': sadness,
                '# words sadness' : sadness_nw,
                'joy': joy,
                '# words joy' : joy_nw,
                'disgust': disgust,
                '# words disgust' : disgust_nw,
                'fear': fear,
                '# words fear' : fear_nw,
                'anticipation' : anticipation,
                '# words anticipation' : anticipation_nw,
                'surprise' : surprise,
                '# words surprise' : surprise_nw
                }
