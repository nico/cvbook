from PIL import Image
from pylab import *
from scipy.ndimage import measurements, morphology
import numpy

im = array(Image.open('board.jpeg').convert('L'))
im = 1 * (im < 128)
gray()

subplot(1, 3, 1)
title('original')
imshow(im)

subplot(1, 3, 2)
im_close = morphology.binary_closing(im, ones((5, 5)), iterations=2)
title('closing')
imshow(im_close)

subplot(1, 3, 3)
im_open = morphology.binary_opening(im, ones((5, 5)), iterations=2)
title('opening')
imshow(im_open)

labels_close, obj_count_close = measurements.label(im_close)
labels_open, obj_count_open = measurements.label(im_open)

print obj_count_close, 'object on closing image'
print obj_count_open, 'object on opening image'

show()
