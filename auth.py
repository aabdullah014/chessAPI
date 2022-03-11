from models.member import MemberModel
from hmac import compare_digest


def authenticate(username, password):
    member = MemberModel.find_by_username(username)
    if member and compare_digest(member.password, password):
        return member

def identity(payload):
    user_id = payload['identity']
    return MemberModel.find_by_id(user_id)