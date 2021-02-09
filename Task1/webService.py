import flask,os
from tqdm import tqdm
from flask import render_template,jsonify,request
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


@app.route('/allusers', methods=['GET'])
def allUsers():
    return jsonify(list(topTerms.keys()))


@app.route('/cloud', methods=['GET'])
def ug():
    return render_template('cloud.html')


@app.route('/users', methods=['GET'])
def cloud():
    return render_template('users.html')

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

if __name__ == '__main__':

    var = 'maildir'
    workDir = os.path.join('intermediary', var)
    path = os.path.join(workDir, 'vectorizedUsers.json')

    

    vectorUsers = gdb._loadFromFile(path)

    path = os.path.join(workDir, 'links.json')
    rawLinks = gdb._loadFromFile(path)

    rawNodes = gdb.getNodes(vectorUsers)
    links = formatLinks(rawLinks, rawNodes)

    nodes = {'nodes': [{'id': name} for name in rawNodes]}
    

    userGraph ={}
    userGraph.update(links)
    userGraph.update(nodes)

    topTerms = gdb.topUserTerms(vectorUsers, 10)
    app.run()
