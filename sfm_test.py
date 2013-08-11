import unittest

from pylab import *
import numpy

import camera
import homography
import sfm

class SfmTest(unittest.TestCase):
  def testComputeFundamental(self):
    points = homography.make_homog(loadtxt('house.p3d').T)

    P = hstack((eye(3), array([[0], [0], [0]])))
    cam = camera.Camera(P)
    x = cam.project(points)

    r = [0.05, 0.1, 0.15]
    rot = camera.rotation_matrix(r)
    cam.P = dot(cam.P, rot)
    cam.P[:, 3] = array([1, 0, 0])
    x2 = cam.project(points)

    K, R, t = cam.factor()
    expectedE = dot(sfm.skew(t), R)
    expectedE /= expectedE[2, 2]

    E = sfm.compute_fundamental(x2[:8], x[:8])

    self.assertEqual(expectedE.shape, E.shape)
    self.assertTrue(numpy.allclose(expectedE, E))


if __name__ == '__main__':
  unittest.main()
