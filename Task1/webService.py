import flask,os
from tqdm import tqdm
from flask import render_template,jsonify,request,redirect,url_for
from flask import json
import graphDataBuilder as gdb
import mimetypes
mimetypes.add_type('application/javascript', '.mjs')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def homee():
    return render_template('index.html', name='john')


@app.route('/userGraphData', methods=['GET'])
def usGraphDa():
    # data = []
    # with open('Task1/static/miser.json','r') as f:
    #     data = json.load(f)
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


@app.route('/allUserClouds', methods=['GET'])
def allUserCloudData():
    # value = [{ 'word': "Running", 'size': "69" }, { 'word': "Surfing", 'size': "20" }, { 'word': "Climbing", 'size': "50" }, { 'word': "Kiting", 'size': "30" },{ 'word': "Sailing", 'size': "20" }, { 'word': "Snowboarding", 'size': "60" }]
    termKey = list(topTerms.keys())[0]
    return jsonify(topTerms[termKey])


@app.route('/allusers', methods=['GET'])
def allUsers():
    return jsonify(list(topTerms.keys()))


@app.route('/cloud', methods=['GET'])
def ug():
    return render_template('cloud.html')


@app.route('/users', methods=['GET'])
def userForce():
    return render_template('users.html', tcount=topCount)

@app.route('/clusters', methods=['GET'])
def clusters():
    return render_template("Clusters.html")


@app.route('/test', methods=['GET'])
def test():
    file = {
        'one': " man hi how are you hello hello hello hello hello hello okay bro",
        'two': "hey homie was poppin!"
    }
    return jsonify(topTerms)


@app.route('/topCount', methods=['GET','POST'])
def topCount():
    global topCount
    global userGraph
    print(request.args)
    topCount = int(request.args.get('count'))
    userGraph = getUserGraph(vectorUsers)
    return redirect(url_for('userForce'))


def formatLinks(lnks,nodes):
    # fmtd = dict.fromkeys(lnks.keys())
    fmtd = []
    added = set()
    nodes = set(nodes)

    for user,conn in tqdm(lnks.items(),desc='Formatting Links'):
        for rec in conn:
            if user == rec  or (user, rec) in added or (rec,user) in added:
                continue


            
            source = user.split('@')[0] if '@' in user else user
            nrec = rec.split('@')[0] if '@' in rec else rec

            if source not in nodes or nrec not in nodes:
                continue

            added.add((user, rec))

            fmtd.append({
                'source': source,
                'target': nrec,
                'value': lnks[user][rec]
                })

    return {"links":fmtd}

topCount = 500
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


def getUserGraph(vectorUsers):
    path = os.path.join(workDir, 'links.json')
    rawLinks = gdb._loadFromFile(path)

    # rawNodes = gdb.getNodes(vectorUsers)

    topNodes = topUsers(vectorUsers)
    links = formatLinks(rawLinks, topNodes)

    # nodes = {'nodes': [{'id': name} for name in rawNodes]}
    nodes = {'nodes': [{'id': name} for name in topNodes]}

    userGraph = {}
    userGraph.update(links)
    userGraph.update(nodes)
    return userGraph

if __name__ == '__main__':

    var = 'subset'
    workDir = os.path.join('intermediary', var)
    path = os.path.join(workDir, 'vectorizedUsers.json')

    

    vectorUsers = gdb._loadFromFile(path)
    userGraph = getUserGraph(vectorUsers)
    

    topTerms = gdb.topUserTerms(vectorUsers, 10)
    app.run()
