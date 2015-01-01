import argparse
import os
import subprocess

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    albums = []
    for album in os.listdir('static'):
        try:
            os.listdir('static/' + album)
            os.listdir('static/' + album + '/thumbnails')
            albums.append(album)
        except OSError:
            pass
    return flask.render_template('index.html', albums=albums)

@app.route('/<album>')
def show_album(album):
    if album == 'favicon.ico': return ''
    pics = []
    try:
        for path in os.listdir('static/' + album):
            if path.rsplit('.', 1)[-1].lower() in ('jpg', 'jpeg'):
                pics.append(path)
    except OSError:
        flask.abort(404)
    pics.sort()
    albumname = album.replace('_', ' ')
    try:
        allsize = subprocess.check_output(['du', '-h', 'static/%s/archive.zip' % album]).split()[0]
    except subprocess.CalledProcessError:
        allsize = None
    return flask.render_template('album.html', album=album, albumname=albumname, allsize=allsize, pics=pics)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=args.debug)
