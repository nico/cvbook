from PIL import Image
from pylab import *
import cPickle as pickle
import glob
import os

import homography
import sift
import tic
import warp


imname = glob.glob('out_Photos/IMG_*.jpg')
siftname = [os.path.splitext(im)[0] + '.sift' for im in imname]

tic.k('start')

l, d = {}, {}
for i in range(len(imname)):
  if not os.path.exists(siftname[i]):
    print 'sifting'
    sift.process_image(imname[i], siftname[i])
  l[i], d[i] = sift.read_features_from_file(siftname[i])


tic.k('loaded')

matches = {}
if not os.path.exists('out_ch03_pano.pickle'):
  for i in range(len(imname) - 1):
    matches[i] = sift.match(d[i + 1], d[i])
  pickle.dump(matches, open('out_ch03_pano.pickle', 'wb'))
matches = pickle.load(open('out_ch03_pano.pickle', 'rb'))

tic.k('matched')

def convert_points(j):
  ndx = matches[j].nonzero()[0]
  fp = homography.make_homog(l[j + 1][ndx, :2].T)
  ndx2 = [int(matches[j][i]) for i in ndx]
  tp = homography.make_homog(l[j][ndx2, :2].T)
  return fp, tp

model = homography.RansacModel()

fp, tp = convert_points(1)

tic.k('converted')

H_12 = homography.H_from_ransac(fp, tp, model)[0]

tic.k('homogd')

# ...

delta = 600
im1 = array(Image.open(imname[1]))#.convert('L'))
im2 = array(Image.open(imname[2]))#.convert('L'))

tic.k('imloaded')

im_12 = warp.panorama(H_12, im1, im2, delta, delta)

tic.k('warpd')

if len(im1.shape) == 2:
  gray()
imshow(array(im_12, "uint8"))
show()
