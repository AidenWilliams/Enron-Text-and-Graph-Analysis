import flask,os
from tqdm import tqdm
import numpy as np
from flask import render_template,jsonify,request,redirect,url_for

import graphDataBuilder as gdb
import dependancyManager as dm
import clustering as cl

import mimetypes
mimetypes.add_type('application/javascript', '.mjs')


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('userForce'))

@app.route('/userGraphData', methods=['GET'])
def usGraphDa():
    return jsonify(userGraph)


@app.route('/userCloudData', methods=['GET'])
def userCloudData():
    user = request.args.get('user')
    userTerms = topUserTerms.get(user)

    wordList = []
    for key, value in userTerms.items():
        wordList.append({'word':key,'size':value})
    return jsonify(wordList)



@app.route('/cloud', methods=['GET'])
def userCloud():
    code = int(request.args.get('code'))
    user = userGraph['nodes'][code]['id']

    return render_template('cloud.html', user=user)

@app.route('/users', methods=['GET'])
def userForce():
    return render_template('users.html', tcount=topCount,ecount=topEdges)

@app.route('/clusters', methods=['GET'])
def clusters():
    return render_template("Clusters.html",kcount=clusterCount,ucount=usersToCluster)


@app.route('/userGraphPreferences', methods=['GET','POST'])
def topCount():
    global topCount
    global userGraph
    global topEdges
    if request.args.get('users') is not None and request.args.get('users')!='':
        topCount = int(request.args.get('users'))
    if request.args.get('edges') is not None and request.args.get('edges')!='':
        topEdges = int(request.args.get('edges'))
    links = dm.getLinks()
    userGraph = getUserGraph(links)
    return redirect(url_for('userForce'))


@app.route('/clusterGraphData', methods=['GET'])
def clusterGraph():
    print(clusterDataCsv)
    return clusterDataCsv

# @app.route('/clusterCount', methods=['GET', 'POST'])
# def cluserCount():
#     global clusterCount
    
#     clusterCount = int(request.args.get('count'))
#     reCluster()
#     return redirect(url_for('clusters'))



# @app.route('/userClusterCount', methods=['GET', 'POST'])
# def userCluster():
#     global usersToCluster
#     usersToCluster = int(request.args.get('count'))
#     reCluster()
#     return redirect(url_for('clusters'))


@app.route('/clusterGraphPreferences', methods=['GET', 'POST'])
def clusterPrefs():
    global clusterCount
    global userGraph
    global usersToCluster
    if request.args.get('users') is not None and request.args.get('users') != '':
        usersToCluster = int(request.args.get('users'))
    if request.args.get('clusters') is not None and request.args.get('clusters') != '':
        clusterCount = int(request.args.get('clusters'))
        
    reCluster()
    return redirect(url_for('clusters'))
    

@app.route('/clusterCloudData', methods=['GET'])
def clusterCloudData():
    global topClustTerms
    clusterID = int(request.args.get('cluster'))
    clusterTerms = topClustTerms.get(clusterID)

    wordList = []
    for key, value in clusterTerms.items():
        wordList.append({'word': key, 'size': value})
    return jsonify(wordList)


@app.route('/clusterCloud', methods=['GET'])
def clusterCloud():
    code = int(request.args.get('code'))
    # user = 'Cluster '+str(code)

    return render_template('cloud.html', cluster=code)

def topUsers(rawLinks,tc = None,chop=True):
    global topCount
    count = topCount
    if tc is not None:
        count = tc


    userTotals = {}
    for user, others in rawLinks.items():
        total = sum(others.values())
        userTotals[user] = total

    sortedUsers = {k: v for k, v in sorted(userTotals.items(), key=lambda item: item[1])}
    topUsers = list(reversed(list(sortedUsers)))[:count]

    if chop:
        nodes = [user.split('@')[0] for user in topUsers]
    else:
        nodes = topUsers
    return nodes


def getUserGraph(rawLinks):

    topNodes = topUsers(rawLinks)
    links = gdb.formatLinks(rawLinks, topNodes,topEdges)

    nodes = {'nodes': [{'id': name} for name in topNodes]}

    userGraph = {}
    userGraph.update(links)
    userGraph.update(nodes)
    return userGraph


# def topEdges(rawLinks):

def reCluster():
    global clusterDataCsv
    global topClustTerms
    # print('clister count',clusterCount)
    # print('uysers clust count',usersToCluster)
    clusterDataRaw = cl.startCluster(k=clusterCount, userCount=usersToCluster)
    topClustTerms = cl.getTopClusterTerms(clusterDataRaw, topNPercentWords)
    clusterDataCsv = cl.clusterDataToCsv(clusterDataRaw)

if __name__ == '__main__':    
    topCount = 80
    topEdges = 100
    clusterCount = 20
    usersToCluster = 150
    topNPercentWords = 20

    app.config["DEBUG"] = True

    links = dm.getLinks()
    userGraph = getUserGraph(links)

    vectorUsers = dm.getuvec()
    topUserTerms = gdb.topTerms(vectorUsers, topNPercentWords)

    clusterDataRaw = cl.startCluster(k=clusterCount, userCount=usersToCluster)
    topClustTerms = cl.getTopClusterTerms(clusterDataRaw, topNPercentWords)
    # print(topClustTerms)
    clusterDataCsv = cl.clusterDataToCsv(clusterDataRaw)


    # app.run(host='0.0.0.0',port=5000)
    app.run()
