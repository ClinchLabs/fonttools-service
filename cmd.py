import json
import requests
import subset
import convert
import click


@click.command()
@click.option('-u', '--font-url', help='TTF or OTF file as base64 string')
@click.option('-t', '--font-type', help='TTF or OTF')
@click.option('-s', '--subsets', help='List of unicode/unicode-ranges as 4-digit hex')
def convert_and_subset(font_url: str,
            font_type: str,
            subsets: str):
    """Convert and subset FFT/OTF font to WOFF and WOFF2"""
    font_bytes = requests.get(font_url).content
    subset_chars = subsets

    if font_type.lower() == 'otf':
        font_bytes = convert.convert_otf_to_ttf(font_bytes)

    res = subset.subset_font(font_bytes, subset_chars)
    print(json.dumps(res))
    exit(0)


if __name__ == '__main__':
    convert_and_subset()
