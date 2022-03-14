from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from auth import authenticate, identity
from resources.member import MemberRegister
from resources.task import Task, TaskList
from resources.family import Family, FamilyList
from db import db


#give file unique name
app = Flask(__name__)

#sqlalchemy turns off flask modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#tell sqlalchemy that data.db is in root folder of directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPOGATE_EXCEPTIONS'] = True
app.secret_key = 'secretysecret'

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)


api.add_resource(Task, '/task/<string:name>')
api.add_resource(TaskList, '/tasks')
api.add_resource(MemberRegister, '/register')
api.add_resource(Family, '/family/<string:name>')
api.add_resource(FamilyList, '/families')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=3000, debug=True)