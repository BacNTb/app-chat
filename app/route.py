from app import app
from flask_restful import Api
from app.controllers.user import User, UserID, UserUsername, UserFullname
from app.controllers.auth import Login, Logout, Refresh
from app.controllers.chat import Conversation, Message
from app.controllers.groupchat import GroupChat, GroupMessage, GroupUser

api = Api(app)

# Auth
api.add_resource(Login, '/login', methods=['POST'])
api.add_resource(Refresh, '/refresh', methods=['POST'])
api.add_resource(Logout, '/logout', methods=['DELETE'])

# User
api.add_resource(User, '/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(UserID, '/user/id', methods=['GET'])
api.add_resource(UserUsername, '/user/username', methods=['GET'])
api.add_resource(UserFullname, '/user/fullname', methods=['GET'])

# Chat 1 - 1
api.add_resource(Message, '/message', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(Conversation, '/conversation', methods=['GET'])

# Chat 1 - n
api.add_resource(GroupMessage, '/group-message', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(GroupChat, '/group-chat', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(GroupUser, '/group-user', methods=['GET'])
