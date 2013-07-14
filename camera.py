import numpy
import scipy.linalg

class Camera(object):
  '''Represents a pin-hole camera.'''

  def __init__(self, P):
    self.P = P
    self.K = None  # Calibration matrix.
    self.R = None  # Rotation matrix.
    self.t = None  # Translation vector.
    self.c = None  # Camera center.

  def project(self, X):
    x = numpy.dot(self.P, X)
    for i in range(3):
      x[i] /= x[2]
    return x

def rotation_matrix(a):
  '''Returns a rotation matrix around the axis of a, by an angle that's equal
  to the length of a in radians.'''
  R = numpy.eye(4)
  R[:3, :3] = scipy.linalg.expm([[0, -a[2], a[1]],
                                 [a[2], 0, -a[0]],
                                 [-a[1], a[0], 0]])
  return R

