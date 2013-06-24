import numpy


def normalize(points):
  for row in points:
    row /= points[-1]
  return points


def make_homog(points):
  return numpy.vstack((points, numpy.ones((1, points.shape[1]))))


def H_from_points(fp, tp):
  '''Find H such that H * fp = tp'''
  if fp.shape != tp.shape:
    raise RuntimeError('number of points do not match')

  # condition:
  # -from
  m = numpy.mean(fp[:2], axis=1)
  maxstd = numpy.max(numpy.std(fp[:2], axis=1)) + 1e-9
  C1 = numpy.diag([1/maxstd, 1/maxstd, 1])
  C1[0, 2] = -m[0] / maxstd
  C1[1, 2] = -m[1] / maxstd
  fp = numpy.dot(C1, fp)

  # -to
  m = numpy.mean(tp[:2], axis=1)
  maxstd = numpy.max(numpy.std(tp[:2], axis=1)) + 1e-9
  C2 = numpy.diag([1/maxstd, 1/maxstd, 1])
  C2[0, 2] = -m[0] / maxstd
  C2[1, 2] = -m[1] / maxstd
  tp = numpy.dot(C2, tp)

  correspondences_count = fp.shape[1]
  A = numpy.zeros((2 * correspondences_count, 9))
  for i in range(correspondences_count):
    A[2 * i    ] = [-fp[0][i], -fp[1][i], -1, 0, 0, 0,
                    tp[0][i]  * fp[0][i], tp[0][i] * fp[1][i], tp[0][i]]
    A[2 * i + 1] = [0, 0, 0, -fp[0][i], -fp[1][i], -1,
                    tp[1][i]  * fp[0][i], tp[1][i] * fp[1][i], tp[1][i]]

  U, S, V = numpy.linalg.svd(A)
  H = V[8].reshape((3, 3))

  # decondition
  H = numpy.dot(numpy.linalg.inv(C2), numpy.dot(H, C1))
  return H / H[2, 2]
