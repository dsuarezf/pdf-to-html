"""PDF To HTML Server.

This module is Flask application serving a RESTFul API to convert PDF files in HTML5 files.

"""
import logging
import os
import urllib
from subprocess import Popen, PIPE

from flask import Flask, request, send_from_directory, after_this_request
from werkzeug.utils import secure_filename

# Logging configuration
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Flask configuration workflow: it loads default config present in config.py and
# tries to override it by using an environment variable that points to an external config file
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_envvar('PDF-TO-HTML-SETTINGS', silent=True)


def allowed_file(filename):
    """Checks if the file belongs to the list of allowed extensions."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Health check endpoint"""
    return "service pdf-to-html running"


@app.route('/api/v1.0/documents/convert', methods=['POST'])
def extract_to_text():
    """It extracts parameters from the HTTP request and route to the appropriate method"""

    @after_this_request
    def remove_file(response): # pylint: disable=unused-variable
        """Removes temporary files once they are converted and sent"""
        for a_file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], a_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except OSError:
                pass
        return response

    if request.method == 'POST':

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            return convert_input_to_html(file)

        url = request.form['url']
        if url:
            file = urllib.request.urlopen(url)
            filename = url.split('/')[-1]
            filename = secure_filename(filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            return convert_input_to_html(file)

        return "File format not supported"
    return "Method not supported"


def convert_input_to_html(file):
    """Use command line Linux tools to convert PDF files into HTML5"""
    logging.info("Converting file: %s", file.filename)
    basename, ext = os.path.splitext(file.filename)
    if ext.lower() == '.pdf':
        command = 'pdf2htmlEX --no-drm 1 %s/%s/%s --dest-dir %s/%s %s.html' % (
            app.root_path, app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename), app.root_path, app.config['UPLOAD_FOLDER'],
            basename)

    else:
        logging.error("File format not supported: %s", file.filename)
        return "File format not supported"

    logging.info("Executing %s", command)
    pipe = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    (output, stderr) = pipe.communicate() # pylint: disable=unused-variable
    if pipe.returncode == 0:
        logging.info('%s pdf to html', basename)
    else:
        logging.error(stderr)

    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=basename + ".html")


if __name__ == '__main__':
    # create the folders when setting up your app
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), mode=0o777, exist_ok=True)
    app.run()
