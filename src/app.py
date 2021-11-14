from PIL import Image
from image_process import *
from flask import Flask
from flask import render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/' # directory for uploading image
ALLOWED_EXTENSIONS = {'jpg','jpeg','png'} # web can only process this extension

app.secret_key = "tubesalgeotercinta"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename): # checking file extension
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# If the submit button is pressed
@app.route('/compress',methods = ['POST'])
def compress_app():
    if request.method == 'POST':
        # Check whether the request has rate and file 
        if 'rate' not in request.form or 'file' not in request.files:
            flash('There is no input')
            return redirect('/') #
        else:
            percen = request.form
            perc = float(percen['rate'])

            pic = request.files['file']

            if (perc<0) or (perc>=100) or (not allowed_file(pic.filename)) or (pic.filename == ''): # validating user input
                flash('Wrong input, please retry')        
                return redirect('/')    
            else:
                filename = secure_filename(pic.filename) # take the name of the pic
                pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) # save to static folder

                pic = Image.open(request.files['file'].stream) # convert into PIL Image
                finalImage, diffRatio, runtime = compress(pic,perc) # compression

                global finalname
                finalname = 'compressed_' + filename
                finalImage = finalImage.save(os.path.join(app.config['UPLOAD_FOLDER'],finalname)) # save the compressed picture to static folder

                return render_template('index.html', rtime = runtime, pixel = diffRatio, imagename = filename, imagefinal = finalname )

    return redirect('/')

# To download the compressed picture
@app.route('/download')
def download():
    global finalname
    path = UPLOAD_FOLDER + finalname
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)