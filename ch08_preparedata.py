"""Splits the hand dataset into train and test folders."""

import os, shutil

s = '/Users/thakis/Downloads/Marcel-Test'
d = 'out_hands'

# Intentionally ignore the MiniTrieschGallery folder.
ls = ['A', 'B', 'C', 'Five', 'Point', 'V']
train = []
test = []
for l in ls:
  imgdir = os.path.join(s, l, 'uniform')
  imgs = [os.path.join(imgdir, f) for f in os.listdir(imgdir)]
  train += imgs[::2]
  test += imgs[1::2]

shutil.rmtree(d)

def md(p):
  try: os.makedirs(p)
  except: pass
md(os.path.join(d, 'train'))
md(os.path.join(d, 'test'))

for p in train: os.symlink(p, os.path.join(d, 'train', os.path.basename(p)))
for p in test: os.symlink(p, os.path.join(d, 'test', os.path.basename(p)))
