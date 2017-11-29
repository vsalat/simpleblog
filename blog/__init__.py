# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys
import os

def create_app(config_filename):
    """
    Flask application factory
    :param config_filename:
    :return:
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    # Корень приложения
    root_dir = os.path.dirname(os.path.realpath(__file__))
    # Путь к storage
    app.config['STORAGE_FOLDER'] = root_dir + '/storage/'
    # Пусть к статике
    app.config['STATIC_FOLDER'] = root_dir + '/static/'
    # ОРМ
    from blog.models import db
    db.init_app(app)
    # Импорт моделей, вьюх
    from blog import views
    from blog.admin_views import admin
    # Register blueprint(s)
    app.register_blueprint(admin)
    return app
