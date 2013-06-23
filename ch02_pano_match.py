import glob
import numpy
import sift

imlist = glob.glob('out/*.jpg')
siftlist = glob.glob('out/*.sift')

image_count = len(imlist)
matchscores = numpy.zeros((image_count, image_count))

for i in range(image_count):
  for j in range(i, image_count):
    print 'comparing', imlist[i], imlist[j]
    l1, d1 = sift.read_features_from_file(siftlist[i])
    l2, d2 = sift.read_features_from_file(siftlist[j])
    matches = sift.match_twosided(d1, d2)
    match_count = sum(matches > 0)
    matchscores[i, j] = match_count

for i in range(image_count):
  for j in range(i + 1, image_count):
    matchscores[j, i] = matchscores[i, j]

print matchscores
