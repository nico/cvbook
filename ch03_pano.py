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

if False:
  # Overlay raw feature locations.
  is_left = H_12[0, 2] < 0
  pdelta = delta if not is_left else 0
  def draw_circle(c, r, col):
    t = arange(0, 1.01, .01) * 2 * pi
    x = r * cos(t) + c[0]
    y = r * sin(t) + c[1]
    plot(x, y, col, linewidth=2)
  for p in l[2]:
    draw_circle((p[0] + pdelta, p[1]), p[2], 'b')
  for p in l[1]:
    hp = array([p[0], p[1], 1])
    # fp are the points in im2, tp the points in im1, so H_12 maps
    # from im2 space to im1 space. Invert to go from im1 to im2.
    hp = dot(linalg.inv(H_12), hp)
    hp[0] /= hp[2]
    hp[1] /= hp[2]
    hp[0] += pdelta
    draw_circle(hp, p[2], 'g')


show()
