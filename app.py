from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from auth import authenticate, identity

#give file unique name
app = Flask(__name__)
app.secret_key = 'secretysecret'

api = Api(app)

jwt = JWT(app, authenticate, identity)


members = []

tasks = [
            {
                'name': 'practice Task',
                'due_date': 2282022
            }
        ]

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('due_date',
        type = int,
        required = True,
        help = "This field cannot be left blank"
    )
    data = parser.parse_args()

    @jwt_required
    def get(self, name):
        task = next(filter(lambda x: x['name'] == name, tasks), None)

        return {'task': task}, 200 if task else 404

    @jwt_required
    def post(self, name):
        data = Task.parser.parse_args()

        if next(filter(lambda x: x['name'] == name, tasks), None) is not None:
            return {'message': 'This item already exists.'}, 400

        task = {'name': name, 'due_date': data['due_date']}
        tasks.append(task)

    @jwt_required
    def delete(self, name):
        global tasks
        tasks = list(filter(lambda x: x['name'] != name, tasks))
        return {'message': 'Task deleted.'}

    @jwt_required
    def put(self, name):
        data = Task.parser.parse_args()

        task = next(filter(lambda x: x['name'] == name, tasks), None)
        if not task:
            task = {'name': name, 'due_date': data['due_date']}
            tasks.append(task)
        else:
            task.update(data)
        return task

class TaskList(Resource):
    def get(self):
        return {'tasks': tasks}

#render index.html file from templates folder
@app.route('/')
def home():
    return render_template('index.html')

# GET /member/<string:name>
@app.route('/member/<string:name>')
def get_member(name):
    for mems in members:
        if mems['name'] == name:
            return jsonify(mems)
    
    return jsonify({'message': 'member not found'})

# POST /member data: {name: }
@app.route('/member', methods=['POST'])
def create_member():
    req_data = request.get_json()
    new_member = {
        'name': req_data['name'],
        'tasks': []
    }
    members.append(new_member)

    return jsonify(new_member)

# GET /member
@app.route('/member')
def get_members():
    return jsonify({'members': members})

# GET /member/<string:name>/tasks
@app.route('/member/<string:name>/task')
def get_items_per_member(name):
    for mems in members:
        if mems['name'] == name:
            return jsonify({
                'tasks': mems['tasks']
            })
    return jsonify({'message': 'member not found'})

# POST /members/<string:name/item {name:, tasks: }
@app.route('/member/<string:name>/task', methods=['POST'])
def create_tasks_per_member(name):
    req_data = request.get_json()
    for mems in members:
        if mems['name'] == name:
            new_task = {
                'name': req_data['name'],
                'due_date': req_data['due_date']
            }
            mems['tasks'].append(new_task)
            return jsonify(new_task)
    
    return jsonify({'message': 'member not found'})

api.add_resource(Task, '/task/<string:name>')
api.add_resource(TaskList, '/tasks')

app.run(port=3000)