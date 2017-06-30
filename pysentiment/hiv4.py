import pandas as pd
from pysentiment.base import STATIC_PATH, BaseDict


class HIV4(BaseDict):
    '''
    Dictionary class for Harvard IV-4. 
    See also http://www.wjh.harvard.edu/~inquirer/
    
    The terms for the dictionary are stemmed by the default tokenizer.
    '''
    
    PATH = '%s/HIV-4.csv' % STATIC_PATH
    
    def init_dict(self):
        data = pd.read_csv(self.PATH,sep=';',low_memory=False)
        for category in ['Positiv', 'Negativ','Affil','Hostile','Strong','Weak','Active','Passive','Pleasur','Pain','Virtue','Vice','Ovrst','Undrst','PowGain','PowLoss','RspGain','RspLoss','Anger','Fear','Sadness','Joy','Surprise','Anticipation','Trust','Disgust','RcEthic', 'RcRelig']:
            terms = data['Entry'][data[category] == category]

########################## Comparisons ##########################
            if category == 'Positiv':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._posset.add(t[0])
            elif category == 'Negativ':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._negset.add(t[0])

            elif category == 'Affil':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._affset.add(t[0])
            elif category == 'Hostile':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._hosset.add(t[0])

            elif category == 'Strong':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._strset.add(t[0])
            elif category == 'Weak':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._weaset.add(t[0])

            elif category == 'Active':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._actset.add(t[0])
            elif category == 'Passive':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._passet.add(t[0])

            elif category == 'Pleasur':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._pleset.add(t[0])
            elif category == 'Pain':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._paiset.add(t[0])

            elif category == 'Virtue':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._virset.add(t[0])
            elif category == 'Vice':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._vicset.add(t[0])

            elif category == 'Ovrst':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._ovtset.add(t[0])
            elif category == 'Undrst':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._udtset.add(t[0])

########################## Emotions ##########################
            elif category == 'Anger':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._angset.add(t[0])
            elif category == 'Fear':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._feaset.add(t[0])
            elif category == 'Sadness':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._sadset.add(t[0])
            elif category == 'Joy':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._joyset.add(t[0])
            elif category == 'Surprise':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._surset.add(t[0])
            elif category == 'Anticipation':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._antset.add(t[0])
            elif category == 'Trust':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._truset.add(t[0])
            elif category == 'Disgust':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._disset.add(t[0])

########################## Rectitude ##########################
            elif category == 'RcEthic':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._rceset.add(t[0])
            elif category == 'RcRelig':
                for t in terms:
                    t = self.tokenize(t)
                    if len(t) > 0:
                        self._rcrset.add(t[0])