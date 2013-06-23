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


def match(desc1, desc2):
  desc1 = numpy.array([d / numpy.linalg.norm(d) for d in desc1])
  desc2 = numpy.array([d / numpy.linalg.norm(d) for d in desc2])

  dist_ratio = 0.6
  desc1_size = desc1.shape

  matchscores = numpy.zeros((desc1_size[0], 1), 'int')
  desc2t = desc2.T
  for i in range(desc1_size[0]):
    dotprods = numpy.dot(desc1[i, :], desc2t)
    dotprods = 0.9999 * dotprods
    indx = numpy.argsort(numpy.arccos(dotprods))

    if (numpy.arccos(dotprods)[indx[0]] <
        dist_ratio * numpy.arccos(dotprods)[indx[1]]):
      matchscores[i] = int(indx[0])

  return matchscores


def match_twosided(desc1, desc2):
  matches_12 = match(desc1, desc2)
  #return matches_12  # XXX doesn't seem to make things worse?
  matches_21 = match(desc2, desc1)

  ndx_12 = matches_12.nonzero()[0]
  for n in ndx_12:
    if matches_21[int(matches_12[n])] != n:
      matches_12[n] = 0
  return matches_12


def appendimages(im1, im2):
  return numpy.concatenate((im1, im2), axis=1)


def plot_matches(im1, im2, locs1, locs2, matchscores, show_below=True):
  import pylab
  im3 = appendimages(im1, im2)
  if show_below:
    im3 = numpy.vstack((im3, im3))

  pylab.imshow(im3)
  cols1 = im1.shape[1]
  for i, m in enumerate(matchscores):
    if m > 0:
      pylab.plot([locs1[i, 0], locs2[m, 0] + cols1],
                 [locs1[i, 1], locs2[m, 1]], 'c')
  pylab.axis('off')
