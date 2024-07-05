from flask import Flask
from flask_cors import CORS

class Config:
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/tp1_intro'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'ajdhaskjdhasdkashdj'

    

