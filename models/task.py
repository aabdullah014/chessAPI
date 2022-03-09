import sqlite3
from this import d

class TaskModel:
    def __init__(self, name, due_date) -> None:
        self.name = name
        self.due_date = due_date

    def json(self):
        return {'name': self.name, 'due_date': self.price}
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connecti('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM tasks WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'task': {'name': row[0], 'due_date': row[1]}}
        return {'message': 'Item not found'}, 404

    @classmethod
    def insert(cls, task):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO tasks VALUES (?, ?)"
        cursor.execute(query, (task['name'], task['due_date']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, task):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE tasks SET due_date=? WHERE name=?"
        cursor.execute(query, (task['due_date'], task['name']))

        connection.commit()
        connection.close()