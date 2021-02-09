import flask,os
from flask import render_template,jsonify,request
import graphDataBuilder as gdb
import mimetypes
mimetypes.add_type('application/javascript', '.mjs')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', name='john')


@app.route('/userCloudData', methods=['GET'])
def userCloudData():
    # value = [{ 'word': "Running", 'size': "69" }, { 'word': "Surfing", 'size': "20" }, { 'word': "Climbing", 'size': "50" }, { 'word': "Kiting", 'size': "30" },{ 'word': "Sailing", 'size': "20" }, { 'word': "Snowboarding", 'size': "60" }]
    user = request.args.get('user')
    value = topTerms.get(user)
    return jsonify(value)


@app.route('/users', methods=['GET'])
def data():
    return jsonify(list(topTerms.keys()))


@app.route('/usersGraph', methods=['GET'])
def ug():
    return render_template('users.html')


@app.route('/force', methods=['GET'])
def frc():
    return render_template('force.html')


@app.route('/clusters', methods=['GET'])
def clusters():
    return render_template("Clusters.html")




if __name__ == '__main__':

    var = 'subset'
    workDir = os.path.join('intermediary', var)
    path = os.path.join(workDir, 'vectorizedUsers.json')

    vectorUsers = gdb._loadFromFile(path)
    topTerms = gdb.topUserTerms(vectorUsers, 10)
    app.run()
