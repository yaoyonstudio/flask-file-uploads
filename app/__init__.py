from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config.from_object('app.config')



from app.models import db
db.init_app(app)


from app.routes import Api
# init_api(app)
