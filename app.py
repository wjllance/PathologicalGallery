# coding:utf-8
#D:\software\pyworkspace\flasktest

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import glob
import datetime

import openslide
from skimage import io
import numpy as np
import sys

fname=sys.argv[1]
osh=openslide.OpenSlide(fname)
thumb=np.array(osh.get_thumbnail((500,500)))
io.imsave(sys.argv[2],thumb)


from MysqlTool import MysqlTool
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'exe'])
UPLOAD_PATH = 'static/files'
THUMB_PATH = 'static/files/thumbs'
DOWNLOAD_PATH = 'static/files'
PATTERN = '*'
DB_NAME = 'test'
DB_IP = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = ''
DB_TABLE = 'file'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generateImage(filename):
    fp = file.save(os.path.join(UPLOAD_PATH, filename))

    osh = openslide.OpenSlide(fname)
    thumb = np.array(osh.get_thumbnail((500, 500)))
    pass

def process(filename, metadata):

    Thumbnail = generateImage(filename)
    FileName = filename
    UploadDate = datetime.date.today().strftime("%Y%m%d")
    UploaderContactInfo = metadata.get('Email')
    TissueType = metadata.get('Tissue')
    SlideCreationDate = metadata.get('date')
    BaseMagnification = metadata.get('magnification')
    ArtifactsTypes = metadata.get('Artifacts')
    StainType = metadata.get('Stain')
    Comments =  metadata.get('Comments')
    ImageSizeInPixels = ''
    ImageSizeInGB = ''
    FileType = ''
    Scanner = metadata.get('Scanner')
    PreparationType = metadata.get('Preparation')
    SpecimenType = metadata.get('Specimen')
    Url = ''
    thumb = ''
    mt.insert(DB_TABLE, [FileName,UploadDate,UploaderContactInfo,TissueType,SlideCreationDate,BaseMagnification,ArtifactsTypes,
               StainType,Comments,ImageSizeInPixels,ImageSizeInGB,FileType,Scanner,PreparationType,SpecimenType,Url])

app = Flask(__name__)
mt = MysqlTool(DB_NAME, DB_IP, DB_PORT, DB_USER, DB_PASSWORD)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def histoqc():
    return render_template('histoqc.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        fileList = request.files.getlist('file')
        metadata = request.form
        for file in fileList:
            if file.filename == '':
                return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
            else:
                try:
                    origin_file_name = file.filename
                    filename = origin_file_name
                    if not os.path.exists(UPLOAD_PATH):
                        os.makedirs(UPLOAD_PATH)
                    file.save(os.path.join(UPLOAD_PATH, filename))
                    process(filename, metadata)
                except Exception as e:
                    return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred: %s' % e})
        return redirect('/gallery')
    else:
        return render_template('upload.html')

@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    return send_from_directory(DOWNLOAD_PATH, filename, as_attachment=True)

@app.route('/gallery')
def gallery():
    fileList = mt.selectAll(DB_TABLE)
    return render_template('gallery.html', files=fileList)

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 15000,
        debug = True
    )
