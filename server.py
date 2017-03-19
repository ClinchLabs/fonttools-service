import base64
import json
import os
import subset

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/subset", methods=["POST"])
def makeSubset():
    try:
        result = subset.subsetFont(request.json['font'], request.json['text'])
    except:
        result = "subsetting font went wrong"

    print(result)
    return jsonify(result=result)

if __name__ == "__main__":
    app.run()
