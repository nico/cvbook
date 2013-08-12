import numpy
from scipy.ndimage import filters

def plane_sweep_ncc(im_l, im_r, start, steps, wid):
  '''Find disparity image using normalized cross-correlation.'''

  m, n = im_l.shape  # Must match im_r.shape.

  mean_l = numpy.zeros(im_l.shape)
  mean_r = numpy.zeros(im_l.shape)
  s = numpy.zeros(im_l.shape)
  s_l = numpy.zeros(im_l.shape)
  s_r = numpy.zeros(im_l.shape)

  dmaps = numpy.zeros((m, n, steps))

  filters.uniform_filter(im_l, wid, mean_l)
  filters.uniform_filter(im_r, wid, mean_r)

  norm_l = im_l - mean_l
  norm_r = im_r - mean_r

  for disp in range(steps):
    filters.uniform_filter(numpy.roll(norm_l, -disp - start) * norm_r, wid, s)
    filters.uniform_filter(numpy.roll(norm_l, -disp - start) *
                           numpy.roll(norm_l, -disp - start), wid, s_l)
    filters.uniform_filter(norm_r * norm_r, wid, s_r)

    dmaps[:, :, disp] = s / numpy.sqrt(s_l * s_r)

  return numpy.argmax(dmaps, axis=2)
