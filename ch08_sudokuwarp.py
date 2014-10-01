import os
from PIL import Image
from pylab import *
from scipy import ndimage

import homography
import tic



SUDOKU_PATH = '/Users/thakis/Downloads/data/sudoku_images/sudokus/'
imname = os.path.join(SUDOKU_PATH, 'sudoku8.jpg')

im = array(Image.open(imname).convert('L'))

# Ask user for corners.
figure()
imshow(im)
gray()
x = ginput(4)

# top left, top right, bottom right, bottom left
fp = array([array([p[1], p[0], 1]) for p in x]).T
tp = array([[0, 0, 1], [0, 1000, 1], [1000, 1000, 1], [1000, 0, 1]]).T
H = homography.H_from_points(tp, fp)

def warpfcn(x):
  x = array([x[0], x[1], 1])
  xt = dot(H, x)
  xt = xt / xt[2]
  return xt[0], xt[1]

tic.k('starting warp')
im_g = ndimage.geometric_transform(im, warpfcn, (1000, 1000))
tic.k('warped')

figure()
imshow(im_g)
show()
