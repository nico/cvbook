from PIL import Image
import numpy
import stereo

im_l = numpy.array(Image.open('out_stereo1.ppm').convert('L'), 'f')
im_r = numpy.array(Image.open('out_stereo2.ppm').convert('L'), 'f')

steps = 12
start = 4
wid = 9

res = stereo.plane_sweep_ncc(im_l, im_r, start, steps, wid)

import scipy.misc
scipy.misc.imsave('out_depth.png', res)
