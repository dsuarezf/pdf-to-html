import logging
import os
import urllib
from subprocess import Popen, PIPE

from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Flask configuration workflow: it loads default config present in config.py and tries to override it by using an
# environment variable that points to an external config file
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_envvar('EXTRACT-TO-TEXT-SETTINGS', silent=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "Module extract-to-text running."


@app.route('/api/v1.0/documents/convert', methods=['POST'])
def extract_to_text():
    if request.method == 'POST':
        try:
            file = request.files['file']
        except:
            file = None
        try:
            url = request.form['url']
        except:
            url = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            return convert_input_to_html(file)
        elif url:
            file = urllib.urlopen(url)
            filename = url.split('/')[-1]
            filename = secure_filename(filename)
            return convert_input_to_html(file)
        else:
            return "File not supported."


def convert_input_to_html(file):
    logging.info("Converting file: %s", file.filename)
    basename, ext = os.path.splitext(file.filename)
    if ext.lower() == '.pdf':
        command = 'pdf2htmlEX --no-drm 1 %s/%s/%s --dest-dir %s/%s %s.html' % (
            app.root_path, app.config['UPLOAD_FOLDER'], file.filename, app.root_path, app.config['UPLOAD_FOLDER'],
            basename)

    else:
        logging.error("File extension not recognized: %s", file.filename)
        return "File not supported."

    logging.info("Executing %s", command)
    p = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    (output, stderr) = p.communicate()
    if p.returncode == 0:
        logging.info('%s pdf to html' % basename)
    else:
        logging.error(stderr)

    logging.debug(output)

    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=basename + ".html")


if __name__ == '__main__':
    # create the folders when setting up your app
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), mode=0o777, exist_ok=True)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=6000)