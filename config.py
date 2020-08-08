from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'songs.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'verysecretkey'
    UPLOAD_FOLDER = path.join(basedir,'application','static')