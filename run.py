from os import listdir, makedirs
from os.path import isfile, join, abspath, path

import logging
from flask import Flask
from flask import render_template
from flask import send_from_directory
from werkzeug.contrib.fixers import ProxyFix

from log_downloader import LogDownloader
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filename='logs/all.log', level=logging.DEBUG)

app = Flask(__name__)

if not path.exists('/logs/'):
    makedirs('/logs/')

if not path.exists('/files/'):
    makedirs('/files/')


@app.route("/")
def hello():
    logging.info('somebody saw files')
    files = [f for f in listdir('files') if isfile(join('files', f))]
    dates = [file.split('.')[0] for file in files]
    return render_template('files.html', dates=dates)


@app.route("/download/<date>/")
def download_file(date):
    filename = str(date) + '.gz'
    logging.info('somebody downloaded file ' + filename)
    return send_from_directory(abspath('files'), filename, as_attachment=True)

if __name__ == "__main__":
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
    # app.run('0.0.0.0', port=8888)

