# Clinch wrapper for "fonttools"
- Converts from OTF to TTF.
- Subsets TTF to WOFF/WOFF2

## Usage
```
python cmd.py --font-url <URL-TO-FONT> --font-type <OTF/TTF> --subsets <RANGE-OF-UNICODE-CHARACTERS>
```

## Input
- **--font-url**: Full url to the font (Example `https://s3.amazonaws.com/test_realtime/a_client_styles/10/BebasNeue-Regular.otf`).
- **--font-type**: The given font file type (Options: `OTF` or `TTF`).
- **--subsets**: List of ranges of unicode characters (Example: `0020-007F,0600,0605,0608`)

## Output
Json containing woff/woff2 as the key, and thier coresponding font file data as base 64.

Example:
```
{
    "woff": "dmdkZnRndmVydHZlcnR2ZXJ0dm...",
    "woff2: "ZG1ka1puUm5kbVZ5ZEhabGNuUj..."
}
```
