import subset, convert
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


@app.route("/fontconvert", methods=["POST"])
def handleFontConvert():
    try:
        base64str = request.form.get('value')
        subsetChars = request.form.get('subset')
        is_otf = str(request.form.get('isOTF')).lower() == 'true'
        print(subsetChars + "\n")

        if is_otf:
            base64str = convert.convert_otf_to_ttf(base64str)

        res = subset.subset_font(base64str, subsetChars)
        return make_response(jsonify(res))
    except Exception as e:
        print(e)
        return make_response("Error occured")


@app.route("/hello", methods=["GET"])
def handleHello():
    try:
        name = request.args.get('name')
        return make_response("hello " + name + "!\n")
    except Exception as e:
        print(e)
        return make_response("The world is ending")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9097)