from fontTools import ttx
from fontTools.ttLib import TTFont, newTable
from fontTools.subset import Subsetter, Options, save_font
from cu2qu.pens import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from logger import log
import uuid
import os

# default approximation error, measured in UPEM
MAX_ERR = 1.0

# default 'post' table format
POST_FORMAT = 2.0

# assuming the input contours' direction is correctly set (counter-clockwise),
# we just flip it to clockwise
REVERSE_DIRECTION = True

def convertFont(base64, type):
    options = Options()

    # tmp file names
    tmpInputFontName = tmpFileName("." + type)
    tmpOutputTtf = tmpFileName(".ttf")
    tmpOutputWoff = tmpFileName(".woff")

    # remove data header from base64
    # now we have a clean input source
    fontbase64 = base64.split(",")[1]
    with open(tmpInputFontName, "wb") as f:
        fontinput = f.write(fontbase64.decode('base64'))
        f.close()

    # we always work from a TTFont Object (also takes OTF)
    font = TTFont(tmpInputFontName)

    ttfOptions = Options()
    # export the font as woff for web use
    woffOptions = Options()
    woffOptions.with_zopfli = True
    woffOptions.flavor = "woff"

    if type == 'otf':
        # convert the font to ttf
        ttfFont = otf_to_ttf(font)
        # save font can also convert to woff!
        save_font(ttfFont, tmpOutputTtf, ttfOptions)
        save_font(ttfFont, tmpOutputWoff, woffOptions)
    elif type == 'ttf':
        save_font(font, tmpOutputTtf, ttfOptions)
        save_font(font, tmpOutputWoff, woffOptions)
    else:
        return { 'error': 'please give a valid type' }

    ttfBase64 = toBase64(tmpOutputTtf)
    woffBase64 = toBase64(tmpOutputWoff)

    #cleanup files
    cleanUp([tmpInputFontName, tmpOutputWoff, tmpOutputTtf])

    return { 'woff': woffBase64, 'ttf': ttfBase64 }

def otf_to_ttf(ttFont, post_format=POST_FORMAT, **kwargs):
    assert ttFont.sfntVersion == "OTTO"
    assert "CFF " in ttFont

    glyphOrder = ttFont.getGlyphOrder()

    ttFont["loca"] = newTable("loca")
    ttFont["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder = glyphOrder
    glyf.glyphs = glyphs_to_quadratic(ttFont.getGlyphSet(), **kwargs)
    del ttFont["CFF "]

    ttFont["maxp"] = maxp = newTable("maxp")
    maxp.tableVersion = 0x00010000
    maxp.maxZones = 1
    maxp.maxTwilightPoints = 0
    maxp.maxStorage = 0
    maxp.maxFunctionDefs = 0
    maxp.maxInstructionDefs = 0
    maxp.maxStackElements = 0
    maxp.maxSizeOfInstructions = 0
    maxp.maxComponentElements = max(
        len(g.components if hasattr(g, 'components') else [])
        for g in glyf.glyphs.values())

    post = ttFont["post"]
    post.formatType = post_format
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = glyphOrder

    ttFont.sfntVersion = "\000\001\000\000"
    return ttFont

def glyphs_to_quadratic(glyphs, max_err=MAX_ERR, reverse_direction=REVERSE_DIRECTION):
    quadGlyphs = {}
    for gname in glyphs.keys():
        glyph = glyphs[gname]
        ttPen = TTGlyphPen(glyphs)
        cu2quPen = Cu2QuPen(ttPen, max_err, reverse_direction=reverse_direction)
        glyph.draw(cu2quPen)
        quadGlyphs[gname] = ttPen.glyph()

    return quadGlyphs

#delete files
def cleanUp(files):
    for file in files:
        os.unlink(file)

def toBase64(filePath):
    return open(filePath, "rb").read().encode("base64")

# creates a tmp file name with uuid
def tmpFileName(type):
    return ".tmp/" + str(uuid.uuid4()) + type
