from PIL import Image
from pylab import *
import sift
#import imtools

im1 = array(Image.open('board.jpeg').convert('L'))
sift.process_image('board.jpeg', 'out_sift.txt')
l1, d1 = sift.read_features_from_file('out_sift.txt')

figure()
gray()
sift.plot_features(im1, l1, circle=True)
show()
