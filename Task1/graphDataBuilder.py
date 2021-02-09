#build graphable data by using the data given in previous step
import os,json,math
from tqdm import tqdm
from docProcessor import getStats

def _loadFromFile(path):
    print('loading from file')
    with open(path) as f:
        return json.load(f)


def topUserTerms(uVec,n):
    topTerms = {}
    for user,vec in tqdm(uVec.items(),desc='Top User Terms'):
        user = user.split('@')[0]
        topTerms[user]= {}
        sortedTerms = {k: v for k, v in sorted(vec.items(), key=lambda item: item[1])}

        cutoff = math.ceil(n/100*len(vec))
        # print(cutoff)
        for key,value in list(reversed(list(sortedTerms.items())))[:cutoff]:
            topTerms[user][key] = value*10
    return topTerms

def getNodes(vUsers):
    return [user.split('@')[0] for user in vUsers.keys()]



if __name__ == '__main__':
    
    var = 'subset'
    workDir = os.path.join('intermediary', var)
    path = os.path.join(workDir, 'vectorizedUsers.json')

    vectorUsers = _loadFromFile(path)
    topTerms = topUserTerms(vectorUsers,10)

    someNames = list(vectorUsers.keys())[:10]
    # someName = someNames[:5]
    for someName in someNames:
        print(topTerms[someName])
