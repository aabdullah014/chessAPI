from resources.member import Member

members = [
    Member(1, 'bob', 'dingus')
]

username_mapping = {m.username: m for m in members}

userid_mapping = {m.id: m for m in members}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)