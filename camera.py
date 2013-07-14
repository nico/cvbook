import numpy

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
