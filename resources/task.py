from flask_restful import Resource, reqparse
from flask_jwt  import jwt_required
from models.task import TaskModel
import sqlite3

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('due_date',
        type = int,
        required = True,
        help = "This field cannot be left blank"
    )
    # data = parser.parse_args()

    @jwt_required
    def get(self, name):
        task = TaskModel.find_by_name(name)

        if task:
            return task
        return {'message': 'Item not found'}, 404

    @jwt_required
    def post(self, name):
        if TaskModel.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400

        data = Task.parser.parse_args()

        task = Task.parser.parse_args()

        try:
            TaskModel.insert(task)
        except:
            return{'message': 'An error occurred inserting the item.'}, 500

        return task, 201

    @jwt_required
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM tasks WHERE name=?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        
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