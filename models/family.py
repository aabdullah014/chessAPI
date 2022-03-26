from db import db

class FamilyModel(db.Model):
    #table for sqlalchemy
    __tablename__ = 'families'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    tasks = db.relationship('TaskModel', lazy='dynamic')

    def __init__(self, name) -> None:
        self.name = name

    def json(self):
        return {'name': self.name, 'tasks': [task.json() for task in self.tasks.all()]}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        