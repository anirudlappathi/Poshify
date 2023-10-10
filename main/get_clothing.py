from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Set the upload folder

UPLOAD_FOLDER = os.path.join('main', 'clothing_img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('../src/index.html')

@app.route('/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Save the uploaded file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)