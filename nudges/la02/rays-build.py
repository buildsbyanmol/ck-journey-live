"""Build assets/la02/rays.png — glow.png re-centred on the burst's radial centre
inside a square canvas, so the layer can be rotated about its own centre.

The move is a pure INTEGER translation, so at rotation 0 the rendered pixels are
identical to today's static glow layer (no resampling, no fidelity loss).

  burst radial centre in glow.png ....... (177, 160)  → design (177, 475)
  canvas ................................ 432 x 432, centre (216, 216)
  offset ................................ (+39, +56)
  design box ............................ (-39, 259) 432 x 432
  alpha 1-2/255 tail dropped ............ 0.93 % of the emitted light, ≤2/255
                                          alpha, so that the support fits inside
                                          the inscribed circle (max r 214 < 216)
                                          and nothing clips when it spins.
"""
import numpy as np
from PIL import Image

SRC = '/Users/maulika/Desktop/contextual nudge/cashkaro-nudges/assets/la02/glow.png'
DST = '/Users/maulika/Desktop/contextual nudge/cashkaro-nudges/assets/la02/rays.png'
N = 432
OFF = (39, 56)
CUT = 3  # drop alpha < 3/255

src = np.array(Image.open(SRC).convert('RGBA'))
src = src.copy()
src[..., 3] = np.where(src[..., 3] < CUT, 0, src[..., 3])
out = np.zeros((N, N, 4), dtype=np.uint8)
out[OFF[1]:OFF[1] + src.shape[0], OFF[0]:OFF[0] + src.shape[1]] = src
img = Image.fromarray(out)
img.save(DST, optimize=True)

al = out[..., 3]
ys, xs = np.nonzero(al > 0)
r = np.hypot(xs - (N / 2 - 0.5), ys - (N / 2 - 0.5))
print('rays.png %dx%d  content r max %.1f (inscribed %d)  alpha max %d' % (N, N, r.max(), N // 2, al.max()))
