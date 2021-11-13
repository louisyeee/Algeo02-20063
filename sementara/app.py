from PIL import Image
from cmp import *
from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
#from PIL import Image
#from cmp import *

def pil2datauri(img):
    #converts PIL image to datauri
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'

app.secret_key = "tubesalgelo"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/compress',methods = ['POST'])

def compress():
    if request.method == 'POST':
        percen = request.form
        perc = float(percen['rate'])

        if 'file' in request.files:

            pic = request.files['file']
            # pic.save(secure_filename(pic.filename))
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            pic = Image.open(request.files['file'].stream)
            #pic = Image.Image(pic)
            finalImage, diffRatio, runtime = compressx(pic,perc) 

            finalname = 'compressed.jpg'
            finalImage = finalImage.save(os.path.join(app.config['UPLOAD_FOLDER'],finalname))

            #finalimg = pil2datauri(finalImage)
            
            #finalname = secure_filename(f'{filename}_compress')
            # finalimg.save(os.path.join(app.config['UPLOAD_FOLDER'],finalname))
            
        return render_template('index.html', rtime = runtime, pixel = diffRatio, imagename = filename, imagefinal = finalname )

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

