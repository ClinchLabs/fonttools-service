from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options, save_font, parse_unicodes
from flask import Flask, jsonify
import uuid
import os
import base64


def tmpFileName(type):
    return ".tmp/" + str(uuid.uuid4()) + type


def subset_font(base64str, subset):
    # tmp file names
    tmpInputFontName = tmpFileName(".ttf")
    tmpOutputFontWoff = tmpFileName(".woff")
    tmpOutputFontWoff2 = tmpFileName(".woff2")

    with open(tmpInputFontName, "wb") as f:
        f.write(base64.b64decode(base64str))
        f.close()

    # open the font with fontTools
    font = TTFont(tmpInputFontName)

    options = Options()
    options.desubroutinize = True

    # export the font as woff for web use
    # subsets = subset.split(",")

    # print(subsets.length)
    options.with_zopfli = True
    options.flavor = "woff"
    subsetter = Subsetter(options=options)
    subsets = parse_unicodes(subset)
    subsetter.populate(unicodes=subsets)
    subsetter.subset(font)
    save_font(font, tmpOutputFontWoff, options)

    subsettedFont = base64.b64encode(open(tmpOutputFontWoff, "rb").read()).decode('utf8')

    options.flavor = "woff2"
    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=subsets)
    subsetter.subset(font)
    save_font(font, tmpOutputFontWoff2, options)

    subsettedFont2 = base64.b64encode(open(tmpOutputFontWoff2, "rb").read()).decode('utf8')

    os.unlink(tmpOutputFontWoff)
    os.unlink(tmpOutputFontWoff2)
    os.unlink(tmpInputFontName)

    return {"woff": subsettedFont, "woff2": subsettedFont2}