import argparse
import os
import subprocess

import imaging


def prepare_album(path):
    os.chdir(path)
    if not os.path.isdir('thumbnails'):
        os.mkdir('thumbnails')
    photos = []
    for p in os.listdir('.'):
        try:
            (prefix, ext) = p.rsplit('.', 1)
            if ext.lower() in ('jpg', 'jpeg'):
                print "Generating thumbnail for", p
                size = imaging.generate_sizes(p, [(280, 210, {'crop': True})], 'jpg')[0]
                os.rename('%s_%dx%d.jpg' % (prefix, size[0], size[1]),
                          'thumbnails/%s' % p)
                photos.append(p)
        except ValueError:
            pass
    if photos:
        subprocess.check_call(['zip', 'archive.zip'] + photos)
    else:
        print "WARNING: no photos found"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="path to directory containing the album's photos")
    args = parser.parse_args()
    prepare_album(args.path)
