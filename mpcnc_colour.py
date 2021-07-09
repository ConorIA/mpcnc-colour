'''
# MPCNC Colourizer
See how your MPCNC might look based on your colour choices. 
'''

import streamlit as st
from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale

## Adapted from: https://stackoverflow.com/a/12310820
def image_tint(img, tint='#ffffff'):
    #img.load()

    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")  # tint color's overall luminosity
    if not tl: tl = 1  # avoid division by zero
    tl = float(tl)  # compute luminosity preserving tint factors
    sr, sg, sb = map(lambda tv: tv/tl, (tr, tg, tb))  # per component adjustments

    # create look-up tables to map luminosity to adjusted tint
    # (using floating-point math only to compute table)
    luts = (list(map(lambda lr: int(lr*sr + 0.5), range(256))) +
            list(map(lambda lg: int(lg*sg + 0.5), range(256))) +
            list(map(lambda lb: int(lb*sb + 0.5), range(256))))
    l = grayscale(img)  # 8-bit luminosity version of whole image
    if Image.getmodebands(img.mode) < 4:
        merge_args = (img.mode, (l, l, l))  # for RGB verion of grayscale
    else:  # include copy of src image's alpha layer
        a = Image.new("L", img.size)
        a.putdata(img.getdata(3))
        merge_args = (img.mode, (l, l, l, a))  # for RGBA verion of grayscale
        luts += range(256)  # for 1:1 mapping of copied alpha values

    return Image.merge(*merge_args).point(luts)

st.header("MPCNC colourizer")
st.write("A quick and dirty app to see how your MPCNC might look based on your colour choices.")

st.sidebar.header("Colours")

colA = st.sidebar.color_picker("Colour A", "#000000")
colB = st.sidebar.color_picker("Colour B", "#8E2626")

st.sidebar.header("TO DO")
st.sidebar.write("""
- Fix colourize code for bright colours, e.g. white

Know how to fix it? Help at:
https://github.com/ConorIA/mpcnc-colour
""")

colourA = Image.open("coloura_bw.png")
tintA = image_tint(colourA, colA)

colourB = Image.open("colourb_bw.png")
tintB = image_tint(colourB, colB)

primo = Image.open("Primo-scaled.jpg")
primo.paste(tintA, mask=tintA)
primo.paste(tintB, mask=tintB)

st.image(primo)
