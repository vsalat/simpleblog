"""
Sample config
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_POOL_RECYCLE = 30
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'thought-glass'
WHOOSH_BASE = os.path.join(basedir, 'search.db')