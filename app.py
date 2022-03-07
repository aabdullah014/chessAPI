from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from auth import authenticate, identity
from member import MemberRegister
from task import Task, TaskList

#give file unique name
app = Flask(__name__)
app.secret_key = 'secretysecret'

api = Api(app)

jwt = JWT(app, authenticate, identity)


api.add_resource(Task, '/task/<string:name>')
api.add_resource(TaskList, '/tasks')
api.add_resource(MemberRegister, '/register')

if __name__ == "__main__":
    app.run(port=3000)