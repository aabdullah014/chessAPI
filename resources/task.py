from flask_restful import Resource, reqparse
from flask_jwt  import jwt_required
from models.task import TaskModel

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('due_date',
        type = int,
        required = True,
        help = "This field cannot be left blank"
    )
    parser.add_argument('family_name', 
        type = int,
        required = True,
        help = "This field cannot be blank."    
    )

    @jwt_required()
    def get(self, name):
        task = TaskModel.find_by_name(name)

        if task:
            return task.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if TaskModel.find_by_name(name):
            return {'message': 'An item with name "{}" already exists.'.format(name)}, 400

        data = Task.parser.parse_args()

        task = TaskModel(name, **data)

        try:
            task.save_to_db()
        except:
            return{'message': 'An error occurred inserting the item.'}, 500

        return task.json(), 201

    @jwt_required()
    def delete(self, name):
        task = TaskModel.find_by_name(name)
        if task: 
            task.delete_from_db()
            return {'message': 'Task deleted.'}
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def put(self, name):
        data = Task.parser.parse_args()

        task = TaskModel.find_by_name(name)

        if task:
            task.due_date = data['due_date']
        else:
            task = TaskModel(name, **data)  
        task.save_to_db()

        return task.json()

class TaskList(Resource):
    def get(self):
        return {'tasks': list(map(lambda x: x.json(), TaskModel.query.all()))}
