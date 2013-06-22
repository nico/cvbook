from scipy.ndimage import filters
import matplotlib
import numpy

def compute_harris_response(im, sigma=3):
  """Compute harris image for each pixel in a graylevel."""

  imx = numpy.zeros(im.shape)
  filters.gaussian_filter(im, sigma, (0, 1), imx)
  imy = numpy.zeros(im.shape)
  filters.gaussian_filter(im, sigma, (1, 0), imy)

  Wxx = filters.gaussian_filter(imx*imx, sigma)
  Wxy = filters.gaussian_filter(imx*imy, sigma)
  Wyy = filters.gaussian_filter(imy*imy, sigma)

  Wdet = Wxx*Wyy - Wxy**2
  Wtr = Wxx + Wyy

  # Use Noble's measure (see wikipedia)
  return 2 * Wdet / (Wtr + 0.000001)


def get_harris_points(harrisim, min_dist=10, threshold=0.1):
  """Return corners from a harris image."""

  corner_threshold = harrisim.max() * threshold
  harrisim_t = (harrisim > corner_threshold) * 1

  coords = numpy.array(harrisim_t.nonzero()).T
  candidate_values = [harrisim[c[0], c[1]] for c in coords]

  index = numpy.argsort(candidate_values)

  allowed_locations = numpy.zeros(harrisim.shape)
  allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 1

  filtered_coords = []
  for i in index:
    if allowed_locations[coords[i, 0], coords[i, 1]] == 1:
      filtered_coords.append(coords[i])
      allowed_locations[(coords[i, 0] - min_dist):(coords[i, 0] + min_dist),
                        (coords[i, 1] - min_dist):(coords[i, 1] + min_dist)] = 0
  return filtered_coords


def plot_harris_points(image, filtered_coords):
  """Plot corners found in an image."""
  import pylab
  pylab.figure()
  pylab.gray()
  pylab.imshow(image)
  pylab.plot([p[1] for p in filtered_coords],
             [p[0] for p in filtered_coords], '*')
  pylab.axis('off')
  pylab.show()
