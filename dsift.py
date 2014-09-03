import numpy
import os
from PIL import Image
import sift
import scipy.io as sio

def process_image_dsift(imname, resultname, size=20, steps=10,
                        force_orientation=False, resize=None):
  """Process an image with densely sampled sift descriptors and save the
  results in a file. Optional input: size of features, steps between locations,
  forcing computation of descriptor orientation (False means all are oriented
  upward), tuple for resizing the image."""
  im = Image.open(imname).convert('L')
  if resize is not None:
    im = im.resize(resize)
  m, n = im.size

  if not imname.endswith('pgm'):
    im.save('out_tmp.pgm')
    imname = 'out_tmp.pgm'

  scale = size / 3.0
  x, y = numpy.meshgrid(range(steps, m, steps), range(steps, n, steps))
  xx, yy = x.flatten(), y.flatten()
  frame = numpy.array([xx, yy, scale * numpy.ones(xx.shape[0]),
                               numpy.zeros(xx.shape[0])])
  numpy.savetxt('out_tmp.frame', frame.T, fmt='%03.3f')

  cmd = ['sift', imname, '--output=' + resultname,
         '--read-frames=out_tmp.frame']
  if force_orientation:
    cmd += ['--orientations']
  os.system(' '.join(cmd))

  # Re-write as .mat file, which loads faster.
  f = numpy.loadtxt(resultname)
  sio.savemat(resultname + '.mat', {'f':f}, oned_as='row')
