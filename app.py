import os
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
import subprocess

MODELS = set(['la_muse', 'rain_princess', 'udnie'])
UPLOAD_FOLDER = './upload'
RESULT_FOLDER = './result'
MODELS_FOLDER = './models'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODELS_FOLDER'] = MODELS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET'])


@app.route('/version',methods=['GET'])
def version():
	return "neural-art:v1.0.0"

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            return 'No file'
        file = request.files['image']
        model = request.form.get('model')

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
        	app.config['EVALUATE_COMMAND'] =  ( "python evaluate.py --allow-different-dimensions  \
        			--checkpoint %s/%s.ckpt --in-path %s --out-path %s" 
        	% (app.config['MODELS_FOLDER'], model, app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER']))
        	
        	result_success = subprocess.check_output(app.config['EVALUATE_COMMAND'], shell=True)
        except subprocess.CalledProcessError as e:
            return "An error occurred while evaluate"

        return send_from_directory(app.config['RESULT_FOLDER'],
                               filename)
    return '''Upload new File</title>'''
