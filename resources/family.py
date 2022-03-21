from flask_restful import Resource
from models.family import FamilyModel

class Family(Resource):
    def get(self, name):
        family = FamilyModel.find_by_name(name)
        if family:
            return family.json()
        return {'message': 'Family not found'}, 404
    
    def post(self, name):
        if FamilyModel.find_by_name(name):
            return {'message': 'A family with name "{}" already exists.'.format(name)}, 400
        
        family = FamilyModel(name)

        try:
            family.save_to_db()
        except:
            return {'message': 'An error occurred while creating the family.'}, 500

        return family.json()

    def delete(self, name):
        family = FamilyModel.find_by_name(name)
        if family:
            family.delete_from_db
        
        return {'message': 'Family deleted'}


class FamilyList(Resource):
    def get(self):
        return {'families': list(map(lambda x: x.json(), FamilyModel.query.all()))}