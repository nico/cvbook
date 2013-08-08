from PIL import Image
from pylab import *
import sift
import sys
#import imtools

imname = 'board.jpeg'
if len(sys.argv) > 1:
  imname = sys.argv[1]

sift.process_image(imname, 'out_sift.txt')
l1, d1 = sift.read_features_from_file('out_sift.txt')

im1 = array(Image.open(imname).convert('L'))
print 'image size {}, {} features'.format(im1.shape, len(l1))

figure()
gray()
sift.plot_features(im1, l1, circle=False)
show()
