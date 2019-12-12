#encoding:utf-8
import os
# the following code is referenced from lecture slide WEEK 11
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never_guess'
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir,'blogdb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



