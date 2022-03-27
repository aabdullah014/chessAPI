from db import db

class TaskModel(db.Model):
    #table for sqlalchemy
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    due_date = db.Column(db.Integer)

    family_id = db.Column(db.Integer, db.ForeignKey('families.id'))
    family = db.relationship('FamilyModel')

    def __init__(self, name, due_date, family_id) -> None:
        self.name = name
        self.due_date = due_date
        self.family_id = family_id

    def json(self):
        return {'name': self.name, 'due_date': self.due_date}
    
    @classmethod
    def find_by_name(cls, name):
        # SELECT * FROM tasks WHERE name=name LIMIT 1 using sqlalchemy
        return cls.query.filter_by(name=name).first()

    
    def save_to_db(self):
        #INSERT INTO tasks VALUES (?, ?)
        db.session.add(self)
        db.session.commit()

    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
