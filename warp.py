from scipy import ndimage
import homography
import numpy


def image_in_image(im1, im2, tp):
  '''Put im1 in im2 with an affine transform such that corners are at tp.
  
  tp is homogeneous and counterclockwise from the top left.'''
  m, n = im1.shape[:2]
  fp = numpy.array([[0, m, m, 0], [0, 0, n, n], [1, 1, 1, 1]])

  H = homograph.Haffine_from_points(tp, fp)
  im1_t = ndimage.affine_transform(
      im1, H[:2, :2], (H[0, 2], H[1, 2]), im2.shape[:2])
  alpha = im1_t > 0

  return (1 - alpha) * im2 + alpha * im1_t


def panorama(H, fromim, toim, padding=2400, delta=2400):
  is_color = len(fromim.shape) == 3

  def transf(p):
    # ndimage passes y in p[0] and x in p[1], so swap to multiply with H and
    # then swap back.
    p2 = numpy.dot(H, [p[1], p[0], 1])
    return p2[1] / p2[2], p2[0] / p2[2]

  if H[1, 2] < 0:  # fromim is on the right
    print 'warp right'
    if is_color:
      toim_t = numpy.hstack((toim, numpy.zeros(
          (toim.shape[0], padding, 3))))
      fromim_t = numpy.zeros(
          (toim.shape[0], toim.shape[1] + padding, toim.shape[2]))
      for col in range(3):
        fromim_t[:, :, col] = ndimage.geometric_transform(
            fromim[:, :, col], transf, (toim.shape[0], toim.shape[1] + padding),
            order=0)
    else:
      toim_t = numpy.hstack((toim, numpy.zeros((toim.shape[0], padding))))
      fromim_t = ndimage.geometric_transform(
          fromim, transf, (toim.shape[0], toim.shape[1] + padding), order=0)
  else:
    print 'warp left'
    H_delta = numpy.array([[1, 0, -delta], [0, 1, 0], [0, 0, 1]])
    H = numpy.dot(H, H_delta)

    if is_color:
      toim_t = numpy.hstack((numpy.zeros(
          (toim.shape[0], padding, 3)), toim))
      fromim_t = numpy.zeros(
          (toim.shape[0], toim.shape[1] + padding, toim.shape[2]))
      for col in range(3):
        print col
        fromim_t[:, :, col] = ndimage.geometric_transform(
            fromim[:, :, col], transf, (toim.shape[0], toim.shape[1] + padding),
            order=0)
    else:
      toim_t = numpy.hstack((numpy.zeros((toim.shape[0], padding)), toim))
      fromim_t = ndimage.geometric_transform(
          fromim, transf, (toim.shape[0], toim.shape[1] + padding), order=0)

  if is_color:
    alpha = ((fromim_t[:, :, 0] * fromim_t[:, :, 1] * fromim_t[:, :, 2]) > 0)
    for col in range(3):
      toim_t[:, :, col] = fromim_t[:, :, col] * alpha + \
                          toim_t[:, :, col]   * (1 - alpha)
  else:
    alpha = (fromim_t > 0) * 0.5 # XXX
    toim_t = fromim_t * alpha + toim_t * (1 - alpha)

  return toim_t
