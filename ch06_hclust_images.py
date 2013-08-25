import hcluster
import imtools
from PIL import Image
from pylab import *

imlist = imtools.get_imlist('/Users/thakis/Downloads/data/flickr-sunsets-small')

# extract histogram as feature vector (8 bins per color channel)
features = zeros([len(imlist), 512])
for i, f in enumerate(imlist):
  im = array(Image.open(f))

  h, edges = histogramdd(im.reshape(-1, 3), 8, normed=True,
                         range=[(0,255), (0, 255), (0, 255)])
  features[i] = h.flatten()

tree = hcluster.hcluster(features)
hcluster.draw_dendrogram(tree, imlist, filename='out_sunset.png')
