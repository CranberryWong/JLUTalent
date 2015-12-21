#! /usr/bin/env python
#coding=utf-8

import os
import time
import tornado.web
from models.entity import Upload, db_session
from PIL import Image
from cStringIO import StringIO

articles_path = os.path.join(os.path.abspath('.'), 'static/articles/')
addon_path = os.path.join(os.path.abspath('.'), 'static/addon/')

def nameRewrite(filename):
    file_timestamp = int(time.time())
    name_split = filename.split('.')
    if len(name_split) == 1:
        filename = filename + str(file_timestamp)
    else:
        filename = name_split[0] + str(file_timestamp) + '.' + name_split[1]
    return filename

def saveIntoDB(filename):
    session = db_session
    session.add(Upload(filename, upload_path+filename))
    session.commit()

def fileUpload(path):
    if 'file' in self.request.files:
        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = nameRewrite(file_dict["filename"]).encode('utf8')
            data = file_dict["body"]
            with open(addon_path + filename, 'w') as f:
                f.write(data)
        saveIntoDB(filename)
        self.write('success')

class ImageUpload(tornado.web.RequestHandler):

    def post(self):
        #upload_path = os.path.join(os.path.dirname(__file__),"static"),
        if 'fileData' in self.request.files:
            file_dict_list = self.request.files['fileData']
            for file_dict in file_dict_list:
                filename = nameRewrite(file_dict["filename"]).encode('utf8')
                data = file_dict["body"]
                image = Image.open(StringIO(data))
                image.save(articles_path + filename, quality=150)
            self.write({
			"success": True,
			"msg": 'success',
			"file_path": '/static/articles/' + filename
		})
