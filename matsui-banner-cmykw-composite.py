"""Compose the five ink bottles into the single CMYKW panel image.

They are the same physical 1Kg bottle photographed separately, so the ~7%
spread in their pixel heights is camera distance, not real size. Normalising
to a common bottle height and seating them all on one baseline makes them read
as one product set rather than five unrelated shots.
"""
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SRC = 'final_src'
# CMYKW order: cyan, magenta, yellow, black, white
ORDER = ['BLUE', 'RED', 'YELLOW', 'BLACK', 'WHITE']
BOTTLE_H = 1800          # normalised bottle height in the composite
GAP_FRAC = 0.09          # gap between bottles, as a fraction of mean width
PAD = 24                 # breathing room so shadows/edges are not clipped


def ink_crop(path):
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im.getchannel('A'))
    ys, xs = np.nonzero(a > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


bottles = []
for name in ORDER:
    im = ink_crop(f'{SRC}/{name}_FINAL.png')
    w = round(im.width * BOTTLE_H / im.height)
    bottles.append(im.resize((w, BOTTLE_H), Image.LANCZOS))

gap = round(np.mean([b.width for b in bottles]) * GAP_FRAC)
total_w = sum(b.width for b in bottles) + gap * (len(bottles) - 1) + PAD * 2
total_h = BOTTLE_H + PAD * 2

canvas = Image.new('RGBA', (total_w, total_h), (0, 0, 0, 0))
x = PAD
for b in bottles:
    canvas.paste(b, (x, PAD), b)      # bottoms already aligned: equal heights
    x += b.width + gap

canvas.save('prod_cmykw_new.png')
print(f'composite {canvas.size[0]}x{canvas.size[1]}  aspect {canvas.size[0]/canvas.size[1]:.3f}')
print('bottle widths:', [b.width for b in bottles], 'gap', gap)
