import glob
import os

import sift
import tic

imname = glob.glob('out_corner/IMG_*.jpg')[1:3]
siftname = [os.path.splitext(im)[0] + '.sift' for im in imname]

tic.k('start')

l, d = {}, {}
for i in range(len(imname)):
  if not os.path.exists(siftname[i]):
    print 'sifting'
    sift.process_image(imname[i], siftname[i])
  l[i], d[i] = sift.read_features_from_file(siftname[i])

tic.k('loaded sifts')
