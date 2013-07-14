from pylab import *
import camera

import homography

points = homography.make_homog(loadtxt('house.p3d').T)

P = hstack((eye(3), array([[0], [0], [-10]])))
cam = camera.Camera(P)
x = cam.project(points)

figure()
plot(x[0], x[1], 'k.')
show()
