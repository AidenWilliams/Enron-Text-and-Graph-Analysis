import math
from tqdm import tqdm



def topTerms(vUsers, n,chop=True):
    topTerms = {}
    for user, vec in tqdm(vUsers.items(), desc='Top Terms'):
        if chop:
            user = user.split('@')[0]
        topTerms[user]= {}
        sortedTerms = {k: v for k, v in sorted(vec.items(), key=lambda item: item[1])}

        cutoff = math.ceil(n/100*len(vec))
        cutoff = min(450,cutoff)

        for key, value in list(reversed(list(sortedTerms.items())))[:cutoff]:
            topTerms[user][key] = value
    return topTerms


def getNodes(vUsers):
    return [user.split('@')[0] for user in vUsers.keys()]


def formatLinks(lnks, nodes, topEdges):

    fmtd = []
    added = set()
    nodes = set(nodes)


    cutoff = {}
    edgeTotals = {}
    for user, contacts in lnks.items():
        edgeTotals[user] = 0
        for contact in contacts:
            edgeTotals[user] += lnks[user][contact]


    for user, conn in tqdm(lnks.items(), desc='Formatting Links'):

        if topEdges != 100:
            cutoff = int(topEdges/100*len(conn))
            conn = dict(
                sorted(conn.items(), key=lambda x: x[1], reverse=True)[:cutoff])

        for rec in conn:
            if user == rec or (user, rec) in added or (rec, user) in added:
                continue

            source = user.split('@')[0] if '@' in user else user
            nrec = rec.split('@')[0] if '@' in rec else rec

            if source not in nodes or nrec not in nodes:
                continue

            added.add((user, rec))

            value = min(20, lnks[user][rec])

            fmtd.append({
                'source': source,
                'target': nrec,
                'value': value//5
            })

    return {"links": fmtd}


