import glob
import os
import sift

for f in glob.glob('out/*.jpg'):
  print 'processing', f
  base = os.path.splitext(os.path.basename(f))[0]
  sift.process_image(f, os.path.join('out', base + '.sift'))
