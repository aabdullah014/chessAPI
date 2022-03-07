from os import curdir
import sqlite3
from flask_restful import Resource, reqparse

class Member:
    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM members WHERE username=?"

        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            member = cls(*row)
        else:
            member = None

        connection.close()
        return member

    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM members WHERE username=?"

        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            member = cls(*row)
        else:
            member = None

        connection.close()
        return member

class MemberRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type = str,
        required = True,
        help = "This field cannot be blank."    
    )
    parser.add_argument('password', 
        type = str,
        required = True,
        help = "This field cannot be blank."    
    )

    def post(self):
        data = MemberRegister.parser.parse_args()

        if Member.find_by_username(data['username']):
            return{'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO members VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return{'message': "User created successfully."}, 201