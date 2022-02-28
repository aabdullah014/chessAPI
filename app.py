from flask import Flask, jsonify, request, render_template

#give file unique name
app = Flask(__name__)

members = [
    {
        'name': 'Abdulrahman',
        'tasks': [
            {
                'name': 'practice Task',
                'due_date': 2282022
            }
        ]
    }
]

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


app.run(port=3000)