import base64
import tempfile

from fontTools import ttx
from fontTools.ttLib import TTFont, newTable
from fontTools.subset import Subsetter, Options, save_font
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
import uuid
import os

# default approximation error, measured in UPEM
MAX_ERR = 1.0

# default 'post' table format
POST_FORMAT = 2.0

# assuming the input contours' direction is correctly set (counter-clockwise),
# we just flip it to clockwise
REVERSE_DIRECTION = True


def convert_otf_to_ttf(otf_bytes: bytes) -> bytes:

    # tmp folder
    with tempfile.TemporaryDirectory() as tmp:

        tmp_input_font_name = os.path.join(tmp, 'source.otf')
        tmp_output_ttf = os.path.join(tmp, 'target.ttf')

        with open(tmp_input_font_name, "wb") as f:
            f.write(otf_bytes)
            f.close()

        # we always work from a TTFont Object (also takes OTF)
        font = TTFont(tmp_input_font_name)

        # convert the font to ttf
        ttf_font = otf_to_ttf(font)

        # save font can also convert to woff!
        save_font(ttf_font, tmp_output_ttf, Options())

        ttf_bytes = open(tmp_output_ttf, "rb").read()

        return ttf_bytes


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
