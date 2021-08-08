import tempfile

from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options, save_font, parse_unicodes
import os
import base64


def subset_font(font_bytes: bytes, subset: str):

    # tmp folder
    with tempfile.TemporaryDirectory() as tmp:

        tmp_input_font_name = os.path.join(tmp, 'source.ttf')
        tmp_output_font_woff = os.path.join(tmp, 'target.woff')
        tmp_output_font_woff2 = os.path.join(tmp, 'target.woff2')

        with open(tmp_input_font_name, "wb") as f:
            f.write(font_bytes)
            f.close()

        # open the font with fontTools
        font = TTFont(tmp_input_font_name)

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
        save_font(font, tmp_output_font_woff, options)

        subsettedFont = base64.b64encode(open(tmp_output_font_woff, "rb").read()).decode('utf8')

        options.flavor = "woff2"
        subsetter = Subsetter(options=options)
        subsetter.populate(unicodes=subsets)
        subsetter.subset(font)
        save_font(font, tmp_output_font_woff2, options)

        subsettedFont2 = base64.b64encode(open(tmp_output_font_woff2, "rb").read()).decode('utf8')

        return {"woff": subsettedFont, "woff2": subsettedFont2}