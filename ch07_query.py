import cPickle as pickle

import imtools
import sift
import imagesearch

"""After ch07_buildindex.py has built an index in test.db, this program can
query it.
"""

imlist = imtools.get_imlist('/Users/thakis/Downloads/ukbench/first1000')
imcount = len(imlist)
featlist = [imlist[i][:-3] + 'sift' for i in range(imcount)]

with open('vocabulary.pkl', 'rb') as f:
  voc = pickle.load(f)

src = imagesearch.Searcher('test.db', voc)

locs, descr = sift.read_features_from_file(featlist[0])
imwords = voc.project(descr)

print 'ask using a histogram...'
print src.candidates_from_histogram(imwords)[:10]

print 'try a query...'
print src.query(imlist[0])[:10]
