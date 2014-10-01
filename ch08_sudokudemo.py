import numpy
import os
from PIL import Image

import sudoku

SUDOKU_PATH = '/Users/thakis/Downloads/data/sudoku_images/sudokus/'
imname = os.path.join(SUDOKU_PATH, 'sudoku17.jpg')
vername = os.path.join(SUDOKU_PATH, 'sudoku17.sud')

im = numpy.array(Image.open(imname).convert('L'))

x = sudoku.find_sudoku_edges(im, axis=0)
y = sudoku.find_sudoku_edges(im, axis=1)

print x
print y
