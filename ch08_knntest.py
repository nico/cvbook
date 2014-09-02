from numpy import array, vstack
import cPickle as pickle
from pylab import *

import imtools
import knn

"""After ch08_makepoints.py has created test data, this trains a kNN classifer
and tests how it does."""

# Load training data.
with open('points_normal.pkl') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)
model = knn.KnnClassifier(labels, vstack((class_1, class_2)))

# Load test data.
with open('points_normal_test.pkl') as f:
  class_1 = pickle.load(f)
  class_2 = pickle.load(f)
  labels = pickle.load(f)

#n = class_1.shape[0]
#n_correct = 0
#for i in range(n):
#  if model.classify(class_1[i]) == labels[i]: n_correct += 1
#  if model.classify(class_2[i]) == labels[n + i]: n_correct += 1
#print 'percent correct:', 100 * n_correct / float(2 * n)

def classify(x, y, model=model):
  return array([model.classify([xx, yy]) for (xx, yy) in zip(x, y)])
imtools.plot_2d_boundary([-6, 6, -6, 6], [class_1, class_2], classify, [1, -1])
show()
