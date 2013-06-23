import os
import urllib, urlparse
import json

URL = 'http://www.panoramio.com/map/get_panoramas.php?' \
      'order=popularity&set=public&size=medium&' \
      'from=0&to={n}&minx={minx}&miny={miny}&maxx={maxx}&maxy={maxy}'

url = URL.format(
    n=20, minx=-77.037564, miny=38.896662, maxx=-77.035564, maxy=38.898662)

j = json.loads(urllib.urlopen(url).read())
imurls = [im['photo_file_url'] for im in j['photos']]

for url in imurls:
  image = urllib.URLopener()
  base = os.path.basename(urlparse.urlparse(url).path)
  image.retrieve(url, os.path.join('out', base))
  print 'downloading', url
