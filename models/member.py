import sqlite3

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