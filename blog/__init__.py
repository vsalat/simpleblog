# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
root_dir=os.path.dirname(os.path.realpath(__file__))
blog = Flask(__name__)
blog.config.from_object('config')
blog.config['STORAGE_FOLDER'] = root_dir+'/storage/'
blog.config['STATIC_FOLDER'] = root_dir+'/static/'
blog.config['DOMAIN']='example.com'
db = SQLAlchemy(blog)
from blog import views, models
from blog.admin_views import admin
# Register blueprint(s)
blog.register_blueprint(admin)