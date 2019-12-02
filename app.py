import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from face_rec import *
import pickle
import json
import base64


UPLOAD_FOLDER = '/tmp/upload'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

reg = Register()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/predict", methods=['POST'])
def predict():
    # try:
        data = request.data
        frame = pickle.loads(base64.b64decode(data))
        result = Predict.get_predictions(frame, reg)
        serialized = pickle.dumps(result)
        return base64.b64encode(serialized)
    # except:
    #     return ''


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uploaded_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_file)
            reg.register_user(request.form.get('name'), uploaded_file)
            print(reg.get_known_faces()[1])
            return redirect(url_for('register'))
    return """
    <!doctype html>
    <title>Register a user</title>
    <h1>Register a user</h1>
    <form action="/register" method=post enctype=multipart/form-data>
      <label>Name : </label> <input type='text' required = 'true' name='name'></input>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
