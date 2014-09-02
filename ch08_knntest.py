from numpy import vstack
import cPickle as pickle

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

print model.classify(class_1[0])
