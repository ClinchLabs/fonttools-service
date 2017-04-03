from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options, save_font
import uuid
import os

def tmpFileName(type):
    return ".tmp/" + str(uuid.uuid4()) + type

def subsetFont(base64, subset):
    # tmp file names
    tmpInputFontName = tmpFileName(".ttf")
    tmpOutputFontName = tmpFileName(".woff")

    # remove data header from base64
    fontbase64 = base64.split(",")[1]

    with open(tmpInputFontName, "wb") as f:
        fontinput = f.write(fontbase64.decode('base64'))
        f.close()

    # open the font with fontTools
    font = TTFont(tmpInputFontName)

    options = Options()
    options.desubroutinize = True

    # export the font as woff for web use
    options.with_zopfli = True
    options.flavor = "woff"

    subsetter = Subsetter(options=options)
    subsetter.populate(text=subset)
    subsetter.subset(font)

    save_font(font, tmpOutputFontName, options)

    subsettedFont = open(tmpOutputFontName, "rb").read().encode("base64")

    os.unlink(tmpOutputFontName)
    os.unlink(tmpInputFontName)

    return { 'subset': subsettedFont }
