#!/usr/bin/python2
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from blog import blog,db
migrate = Migrate(blog, db)
manager = Manager(blog)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
