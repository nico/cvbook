import numpy

def compute_fundamental(x1, x2):
  '''Computes the fundamental matrix from corresponding points x1, x2 using
  the 8 point algorithm.'''

  n = x1.shape[1]
  if x2.shape[1] != n:
    raise ValueError('Number of points do not match.')

  # FIXME: normalize!
  A = numpy.zeros((n, 9))
  for i in range(n):
    A[i] = [x1[0, i] * x2[0, i],  x1[0, i] * x2[1, i],  x1[0, i] * x2[2, i],
            x1[1, i] * x2[0, i],  x1[1, i] * x2[1, i],  x1[1, i] * x2[2, i],
            x1[2, i] * x2[0, i],  x1[2, i] * x2[1, i],  x1[2, i] * x2[2, i],
           ]

  # Solve A*f = 0 using least squares.
  U, S, V = numpy.linalg.svd(A)
  F = V[-1].reshape(3, 3)

  # Constrain F to ranke 2 by zeroing out last singular value.
  U, S, V = numpy.linalg.svd(F)
  S[2] = 0
  F = numpy.dot(U, numpy.dot(numpy.diag(S), V))
  return F


def compute_right_epipole(F):
  '''Returns e with F * e = 0 (call with F.T for left epipole).'''
  U, S, V = numpy.linalg.svd(F)
  e = V[-1]  # S is diag([l1, l2, 0]). e's scale is arbitrary.
  return e / e[2]


def plot_epipolar_line(im, F, x, epipole=None, show_epipole=True):
  '''Plot the epipole and epipolar line F*x = 0.'''
  import pylab

  m, n = im.shape[:2]
  line = numpy.dot(F, x)

  t = numpy.linspace(0, n, 100)
  lt = numpy.array([(line[2] + line[0] * tt) / (-line[1]) for tt in t])

  ndx = (lt >= 0) & (lt < m)
  pylab.plot(t[ndx], lt[ndx], linewidth=2)

  if show_epipole:
    if epipole is None:
      epipole = compute_right_epipole(F)
    pylab.plot(epipole[0] / epipole[2], epipole[1] / epipole[2], 'r*')
