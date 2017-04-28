DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_DB = 'flask-file-uploads'

DEBUG = True
PORT = 3333
HOST = "192.168.1.141"

UPLOAD_FOLDER = '\img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB


