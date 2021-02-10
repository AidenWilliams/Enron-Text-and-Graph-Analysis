import flask,os
from tqdm import tqdm
from flask import render_template,jsonify,request,redirect,url_for

import graphDataBuilder as gdb
import dependancyManager as dm

import mimetypes
mimetypes.add_type('application/javascript', '.mjs')


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('userForce'))

@app.route('/userGraphData', methods=['GET'])
def usGraphDa():
    return jsonify(userGraph)

@app.route('/userCloudData', methods=['GET'])
def userCloudData():
    # value = [{ 'word': "Running", 'size': "69" }, { 'word': "Surfing", 'size': "20" }, { 'word': "Climbing", 'size': "50" }, { 'word': "Kiting", 'size': "30" },{ 'word': "Sailing", 'size': "20" }, { 'word': "Snowboarding", 'size': "60" }]
    user = request.args.get('user')
    userTerms = topTerms.get(user)
    # print('returning',value)

    wordList = []
    for key, value in userTerms.items():
        wordList.append({'word':key,'size':value})
    return jsonify(wordList)

@app.route('/cloud', methods=['GET'])
def ug():
    code = int(request.args.get('code'))
    user = userGraph['nodes'][code]['id']

    return render_template('cloud.html', user=user)

@app.route('/users', methods=['GET'])
def userForce():
    return render_template('users.html', tcount=topCount)

@app.route('/clusters', methods=['GET'])
def clusters():
    return render_template("Clusters.html")


@app.route('/topCount', methods=['GET','POST'])
def topCount():
    global topCount
    global userGraph
    # print(request.args)
    topCount = int(request.args.get('count'))
    links = dm.getLinks()
    userGraph = getUserGraph(links)
    return redirect(url_for('userForce'))


@app.route('/topEdges', methods=['GET', 'POST'])
def topEdges():
    global topEdges
    global userGraph
    # print(request.args)
    topCount = int(request.args.get('count'))
    links = dm.getLinks()
    userGraph = getUserGraph(links)
    return redirect(url_for('userForce'))


def formatLinks(lnks,nodes):
    # fmtd = dict.fromkeys(lnks.keys())
    fmtd = []
    added = set()
    nodes = set(nodes)
    
    edgeTotals = {}
    # counts = {}
    bestEdges = {}
    for user,contacts in tqdm(lnks.items(),desc='Sorting Edges'):
        edgeTotals[user] = 0
        # counts[user] = 0
        for contact in contacts:
            edgeTotals[user] += lnks[user][contact]
            # counts[user]+=1

        sortedEdges = {k: v for k, v in sorted(edgeTotals.items(), key=lambda item: item[1])}
        bestEdges[user] = set(list(reversed(list(sortedEdges)))[:topEdges])
    

    for user, conn in tqdm(lnks.items(), desc='Formatting Links'):
        for rec in conn:
            if user == rec  or (user, rec) in added or (rec,user) in added:
                continue
            if rec not in bestEdges[user]:
                continue
            
            source = user.split('@')[0] if '@' in user else user
            nrec = rec.split('@')[0] if '@' in rec else rec

            if source not in nodes or nrec not in nodes:
                continue

            added.add((user, rec))


            value = min(20,lnks[user][rec])

            fmtd.append({
                'source': source,
                'target': nrec,
                'value': value
                })

    return {"links":fmtd}

topCount = 80
topEdges = 100
def topUsers(rawLinks):
    global topCount
    userTotals = {}
    for user, others in rawLinks.items():
        total = sum(others.values())
        userTotals[user] = total

    sortedUsers = {k: v for k, v in sorted(userTotals.items(), key=lambda item: item[1])}
    topUsers = list(reversed(list(sortedUsers)))[:topCount]
    nodes = [user.split('@')[0] for user in topUsers]
    return nodes


def getUserGraph(rawLinks):

    topNodes = topUsers(rawLinks)
    links = formatLinks(rawLinks, topNodes)

    nodes = {'nodes': [{'id': name} for name in topNodes]}

    userGraph = {}
    userGraph.update(links)
    userGraph.update(nodes)
    return userGraph


# def topEdges(rawLinks):


if __name__ == '__main__':

    # var = 'maildir'
    # workDir = os.path.join('intermediary', var)
    # path = os.path.join(workDir, 'vectorizedUsers.json')
    

    links = dm.getLinks()
    userGraph = getUserGraph(links)

    vectorUsers = dm.getuvec()
    topTerms = gdb.topUserTerms(vectorUsers, 20)
    app.run(host='0.0.0.0',port=6969)
