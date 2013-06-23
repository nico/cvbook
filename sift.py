from PIL import Image
import numpy
import os

def process_image(imagename, resultname,
                  params='--edge-thresh 10 --peak-thresh 5'):
  if not imagename.endswith('pgm'):
    im = Image.open(imagename).convert('L')
    im.save('out_tmp.pgm')
    imagename = 'out_tmp.pgm'

  # Assumes that vlfeat's sift binary is in PATH.
  cmd = ' '.join(['sift', imagename, '--output=' + resultname, params])
  os.system(cmd)


def read_features_from_file(filename):
  '''Returns feature locations, descriptors.'''
  f = numpy.loadtxt(filename)
  return f[:, :4], f[:, 4:]


def plot_features(im, locs, circle=False):
  import pylab
  def draw_circle(c, r):
    t = numpy.arange(0, 1.01, .01) * 2 * numpy.pi
    x = r * numpy.cos(t) + c[0]
    y = r * numpy.sin(t) + c[1]
    pylab.plot(x, y, 'b', linewidth=2)
  pylab.imshow(im)
  if circle:
    for p in locs:
      draw_circle(p[:2], p[2])
  else:
    plot(locs[:, 0], locs[:, 1], 'ob')
  pylab.axis('off')
