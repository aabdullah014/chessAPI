from db import db

class FamilyModel(db.Model):
    #table for sqlalchemy
    __tablename__ = 'families'

    id_count = 0
    id = db.Column(db.Integer)
    name = db.Column(db.String(20))

    tasks = db.relationship('TaskModel', lazy='dynamic')

    def __init__(self, name) -> None:
        self.name = name

    def json(self):
        return {'name': self.name, 'tasks': [task.json() for task in self.tasks.all()]}
    
    @classmethod
    def find_by_name(cls, name):
        # SELECT * FROM tasks WHERE name=name LIMIT 1 using sqlalchemy
        return cls.query.filter_by(name=name).first()

    
    def save_to_db(self):
        #INSERT INTO tasks VALUES (?, ?)
        id_count += 1
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(self):
        id_count -= 1
        db.session.delete(self)
        db.session.commit()
        