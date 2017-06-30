from nltk.parse.stanford import StanfordDependencyParser
import os 

os.environ['STANFORD_PARSER'] = '/users/claire/documents/iota/tools/stanford-parser-full-2015-04-20/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '/users/claire/documents/iota/tools/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'

dep_parser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")


def dependencies(text) :
    text = text.encode('utf8')
    sentences = text.split('.')
    neg_dependencies = []
    for s in sentences : 
        result = dep_parser.raw_parse(s)
        dep = result.next()
        res = list(dep.triples())
        for r in res :
            if 'neg' in r[1] :
                if 'RB' not in r[0][1] :
                    neg_dependencies.append(r[0][0])
                if 'RB' not in r[1][1] :
                    neg_dependencies.append(r[1][0])
    return neg_dependencies

print dependencies('THE Internet is the wave of the future, the technology that changes everything. Just dont try to get a job in it. The United States government has released new employment numbers for the last several years, showing there were 933,000 more jobs than previously thought. A handful of them  6,300, to be exact  were in Internet companies, including publishing and broadcasting. But that did not alter the trend. The charts show the gains, or losses, in jobs in the six years since President Bush took office. Over all, there were 4.8 million more jobs in January than in January 2001. That is a 3.6 percent gain. The increase is smaller than in previous administrations, but it came at a time that unemployment was already low and the labor force was not expanding as rapidly as in the past. One chart shows the combined categories of publishing and broadcasting, both traditional and Internet-based. Over all, employment is down 11 percent. In those six years, employment in traditional paper-based publishing is down 13 percent. Broadcasting employment is off 3 percent. The traditional industries, between them, have shed 148,000 workers. Did the Internet make up the difference? Just the opposite. Internet publishing and broadcasting now employs 36,600 people, and that figure is down 29 percent from six years ago. A larger Internet-related area covers Internet service providers, search portals and data processing. It now has 385,000 workers, down 25 percent over the last six years. The places to look for jobs in Mr. Bushs six years have been less in line with the new economy, although the category of business and technical consulting  an area that has included many of those proclaiming the Internet to be the future  has done very well. It is up 29 percent since the inauguration of the first president with a masters degree in business administration. That increase is even more than the gain for residential construction, which is up 28 percent, although that sector has slipped 2 percent since peaking last March. History indicates it could get worse. From a 1988 peak to a post-recession low in 1992, employment in residential construction fell 28 percent. Nonresidential construction has been growing at a good pace for the last couple of years, but for the entire Bush administration it has grown less than the economy as a whole. The long-term decline of manufacturing has accelerated in the Bush administration. It took more than two decades, after the peak in 1979, for the United States to shed almost 2.5 million jobs. In the last six years, almost 3 million more have gone. Still, with 14.1 million jobs, manufacturing employs more people than either health care or education, two areas that have grown rapidly in recent years.')