import numpy

def compute_fundamental(x1, x2):
  '''Computes the fundamental matrix from corresponding points x1, x2 using
  the 8 point algorithm.'''

  n = x1.shape[1]
  if x2.shape[1] != n:
    rause ValueError('Number of points do not match.')

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
