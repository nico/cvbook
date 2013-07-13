import glob
import os

import sift
import tic

imname = glob.glob('out_corner/IMG_*.jpg')[1:3]
siftname = [os.path.splitext(im)[0] + '.sift' for im in imname]

tic.k('start')

l, d = {}, {}
for i in range(len(imname)):
  l[i], d[i] = sift.read_or_compute(imname[i], siftname[i])

tic.k('loaded sifts')
