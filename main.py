import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for,send_from_directory,render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader,PdfFileMerger

UPLOAD_FOLDER='upload_folder'
ALLOWED_EXTENSIONS={'pdf'}
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def merger(data):
    print(data)
    mergedObject = PdfFileMerger()
    for fileName in data:
        mergedObject.append(PdfFileReader('upload_folder/{}'.format(fileName),'rb'))
        print("succesfull")
    filename="mergedfilesoutput.pdf"
    mergedObject.write(filename)
    print(mergedObject)
    print("sucessfull mergered")
    return redirect(url_for('uploaded_file',filename=filename))
    
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        if 'files[]' not in request.files:
            flash("Tidak ada file ditemukan")
            return redirect(request.url)
        files=request.files.getlist('files[]')
        data=[]
        for file in files:
            if file.name=='':
                flash("No Selected File")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename=secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data.append(filename)
                flash('File(s) successfully uploaded')
        merger(data)
    return render_template('index.html')
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__=="__main__":
    app.run(debug=True)