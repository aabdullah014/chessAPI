from flask_restful import Resource, reqparse
from flask_jwt  import jwt_required
import sqlite3

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
        connection = sqlite3.connecti('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tasks WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'task': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connecti('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tasks WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'task': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}, 404

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