from db import db

class MemberModel(db.Model):
    #table for sqlalchemy
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String)


    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
