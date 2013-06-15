import numpy
import os

from PIL import Image


def get_imlist(path):
  """Returns a list of filenames for all jpg images in a directory."""
  return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def imresize(im, sz):
  """Resize an image array using PIL."""
  pil_im = Image.fromarray(numpy.uint8(im))
  return numpy.array(pil_im.resize(sz))


def histeq(im, bin_count=256):
  """Histogram equalization of a grayscale image."""
  imhist, bins = numpy.histogram(im.flatten(), bin_count, normed=True)
  cdf = imhist.cumsum()
  cdf = 255 * cdf / cdf[-1]  # normalize

  im2 = numpy.interp(im.flatten(), bins[:-1], cdf)
  return im2.reshape(im.shape), cdf


def compute_average(imlist):
  """Compute the average of a lsit of images."""
  avg = numpy.array(Image.open(imlist[0]), 'f')
  count = 1
  for name in imlist[1:]:
    try:
      avg += numpy.array(Image.open(name))
      count += 1
    except:
      print name + '...skipped'
  avg /= count
  return numpy.array(avg, 'uint8')
