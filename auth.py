from models.member import MemberModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = MemberModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return MemberModel.find_by_id(user_id)