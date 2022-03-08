from flask import Flask, after_this_request, jsonify
import json


app = Flask(__name__)

@app.route("/")
def hello_world():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    jsonResp = {'jack': 4098, 'sape': 4139}
    print(jsonResp)
    return jsonify(jsonResp)
    
if __name__ == "__main__":
    app.run(debug=True)