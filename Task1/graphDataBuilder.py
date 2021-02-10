#build graphable data by using the data given in previous step
import os,json,math
from tqdm import tqdm
# import dependancyManager as dm

# def _loadFromFile(path):
#     print('loading from file')
#     with open(path) as f:
#         return json.load(f)


def topUserTerms(vUsers, n):
    topTerms = {}
    for user, vec in tqdm(vUsers.items(), desc='Top User Terms'):
        user = user.split('@')[0]
        topTerms[user]= {}
        sortedTerms = {k: v for k, v in sorted(vec.items(), key=lambda item: item[1])}

        cutoff = math.ceil(n/100*len(vec))
        # print(cutoff)
        for key, value in list(reversed(list(sortedTerms.items())))[:cutoff]:
            topTerms[user][key] = value
    return topTerms

def getNodes(vUsers):
    return [user.split('@')[0] for user in vUsers.keys()]


