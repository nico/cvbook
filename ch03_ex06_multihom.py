from PIL import Image
from pylab import *
import cPickle as pickle
import glob
import os
import numpy

import homography
import sift
import tic
import warp

imname = glob.glob('out_corner/IMG_*.jpg')
siftname = [os.path.splitext(im)[0] + '.sift' for im in imname]

tic.k('start')

l, d = {}, {}
for i in range(len(imname)):
  l[i], d[i] = sift.read_or_compute(imname[i], siftname[i])

tic.k('loaded sifts')


if not os.path.exists('out_ch03_ex06_match.pickle'):
  matches = sift.match(d[1], d[0])
  pickle.dump(matches, open('out_ch03_ex06_match.pickle', 'wb'))
matches = pickle.load(open('out_ch03_ex06_match.pickle', 'rb'))

tic.k('matched')

ndx = matches.nonzero()[0]
fp = homography.make_homog(l[1][ndx, :2].T)
ndx2 = [int(matches[i]) for i in ndx]
tp = homography.make_homog(l[0][ndx2, :2].T)

tic.k('converted')

model = homography.RansacModel()

H1, inliers1 = homography.H_from_ransac(fp, tp, model)

tic.k('h1 computed')

# Remove inliers from first round, rerun ransac.
fp2 = numpy.delete(fp, inliers1, axis=1)
tp2 = numpy.delete(tp, inliers1, axis=1)
H2, inliers2 = homography.H_from_ransac(fp2, tp2, model)

tic.k('h2 computed')


im1 = array(Image.open(imname[0]).convert('L'))
im2 = array(Image.open(imname[1]).convert('L'))

tic.k('imloaded')

if len(im1.shape) == 2:
  gray()
imshow(im1)
inliers1_pts = tp[:2, inliers1]
plot(inliers1_pts[0], inliers1_pts[1], 'gx')

inliers2_pts = tp2[:2, inliers2]
plot(inliers2_pts[0], inliers2_pts[1], 'rx')

show()
