import glob
import os
import sift

for f in glob.glob('out/*.jpg'):
  base = os.path.splitext(os.path.basename(f))[0]
  sift = os.path.join('out', base + '.sift')
  if os.path.exists(sift): continue

  print 'processing', f
  sift.process_image(f, sift)
