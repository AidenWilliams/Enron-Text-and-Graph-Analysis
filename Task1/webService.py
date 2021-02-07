import flask
from flask import render_template,jsonify
from flask import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', name='john')


@app.route('/data', methods=['GET'])
def data():
    value = [{ 'word': "Running", 'size': "69" }, { 'word': "Surfing", 'size': "20" }, { 'word': "Climbing", 'size': "50" }, { 'word': "Kiting", 'size': "30" },{ 'word': "Sailing", 'size': "20" }, { 'word': "Snowboarding", 'size': "60" }]
    return jsonify(value)


@app.route('/clusters', methods=['GET'])
def clusters():
    return render_template("Clusters.html")


app.run()
