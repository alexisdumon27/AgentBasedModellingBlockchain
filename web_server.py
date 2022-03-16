from flask import Flask, after_this_request, jsonify, request
import json
import os

app = Flask(__name__)

filename = os.path.join(app.static_folder, 'orderBookData.JSON')
print (filename)

@app.route("/")
def sendUpdatedData():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "orderBookData.JSON")
    data = json.load(open(json_url))
    return jsonify(data)

@app.route("/transactions")
def sendTransactionData():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "transactionData.JSON")
    data = json.load(open(json_url))
    return jsonify(data)

@app.route("/wealth")
def sendwealthData():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "wealthiestAgentsData.JSON")
    data = json.load(open(json_url))
    return jsonify(data)

@app.route("/distribution")
def sendDistributionData():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "wealthDistributionData.JSON")
    data = json.load(open(json_url))
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)