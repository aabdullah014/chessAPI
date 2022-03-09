from os import curdir
import sqlite3
from flask_restful import Resource, reqparse
from models.member import MemberModel

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

        if MemberModel.find_by_username(data['username']):
            return{'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO members VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return{'message': "User created successfully."}, 201