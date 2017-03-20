import base64
import json
import os
import subset
import health
from logger import log
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

log.info("starting subset service..")

@app.route("/subset", methods = ["POST"])
def handleSubset():
    try:
        return make_response(jsonify(
            subset = subset.subsetFont(request.json['font'], request.json['text'])
        ), 200)
    except:
        log.warn("subsetting font went wrong", request)
        return make_response(jsonify(error = "subsetting went wrong"), 500)

@app.route("/health", methods = ["GET"])
def handleHealth():
    memory, uptime, cpu = health.getHealth()
    return make_response(jsonify(
        uptime = uptime,
        cpu = cpu,
        memory = memory
    ), 200)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 9097)
