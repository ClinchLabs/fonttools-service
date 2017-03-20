import base64
import json
import os
import subset
from logger import log
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

log.info("starting subset service..")

@ app.route("/subset", methods = ["POST"])
def makeSubset():
    try:
        return make_response(jsonify(
            subset = subset.subsetFont(request.json['font'], request.json['text'])
        ), 200)
    except:
        log.warn("subsetting font went wrong", request)
        return make_response(jsonify(error = "subsetting went wrong"), 500)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 9097)
