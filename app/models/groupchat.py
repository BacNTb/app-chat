from flask_jwt_extended import get_jwt_identity
from app.connection import db
from app.model import User, GroupMessage, GroupChat, GroupUser
from datetime import datetime
from app.logger import logging_message

PATH_FILE = '/home/bacntb/app-chat/logger/groupchat.log'

class GroupMessageModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def get(self, group_id):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            group_user = GroupUser.query.filter((GroupUser.group_id == group_id.id) & (GroupUser.user_id == user_id)).first()
            message = []
            if group_user:
                messages = GroupMessage.query.filter(GroupMessage.group_id == group_id.id).order_by(GroupMessage.created_at).all()
                for i in messages:
                    mess = {'id': i.id, 'group_id': i.group_id, 'user_id': i.user_id, 'message': i.message, 'created_at': i.created_at, 'updated_at': i.updated_at}
                    message.append(mess)

            self.logger.info(identity['username'] + ' - Get Message Ok')
            return message

        except Exception as e:
            return 'Server Error'

    def post(self, data):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            group_user = GroupUser.query.filter((GroupUser.group_id == data.id) & (GroupUser.user_id == user_id)).first()
            if group_user:
                message = GroupMessage(data.message, data.id, user_id)
                db.session.add(message)
                db.session.commit()

                result = {'id': message.id, 'message': message.message, 'created_at': message.created_at, 'updated_at': message.updated_at}
                message = 'Ok'
            else:
                result = 'You are not in this chat group !!!'
                message = result

            self.logger.info(identity['username'] + ' - Post Message - ' + message)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' - Post Message Fail - ' + str(e))
            return 'Server Error'

    def put(self, data):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            message = GroupMessage.query.filter((GroupMessage.id == data.id) & (GroupMessage.user_id == user_id)).first()
            if message:
                message.message = data.message
                message.updated_at = datetime.now()
                db.session.commit()

                result = {'id': message.id, 'message': message.message, 'created_at': message.created_at, 'updated_at': message.updated_at}
                message = 'Ok'
            else:
                result = 'You dont have no right to edit this message !!!'
                message = result
            self.logger.info(identity['username'] + ' - Put Message - ' + message)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' - Put Message Fail - ' + str(e))
            return 'Server Error'

    def delete(self, group_id):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            message = GroupMessage.query.filter((GroupMessage.id == group_id.id) & (GroupMessage.user_id == user_id)).first()
            if message:
                db.session.delete(message)
                db.session.commit()
                result = 'Delete Message Successfully'
            else:
                result = 'You dont have no right to delete this message !!!'
            self.logger.info(identity['username'] + ' - Delte message - ' + result)
            return result

        except Exception as e:
            return 'Server Error'

class GroupChatModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def get(self):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            group_users = GroupUser.query.filter(GroupUser.user_id == user_id).all()
            group_chats = []
            if group_users:
                for group_user in group_users:
                    group_chat = GroupChat.query.filter(GroupChat.id == group_user.group_id).first()
                    group = {'id': group_chat.id, 'group_name': group_chat.group_name, 'created_by': group_chat.created_by, 'updated_by': group_chat.updated_by, 'created_at': group_chat.created_at, 'updated_at': group_chat.updated_at}
                    group_chats.append(group)
                message = 'Ok'
            else:
                group_chats = 'You dont have any group chat yet !!!'
                message = group_chats

            self.logger.info(identity['username'] + ' - Get Group Chat - ' + message)
            return group_chats

        except Exception as e:
            self.logger.error(identity['username'] + ' - Get Group Chat Fail - ' + str(e))
            return 'Server Error'

    def post(self, data):
        identity = get_jwt_identity()
        created_by = identity['id']
        user_ids = data['id'].split(',')
        try:
            group_chat = GroupChat(data.group_name, created_by)
            db.session.add(group_chat)
            db.session.commit()
            if group_chat:
                user_ids.append(created_by)
                for user_id in user_ids:
                    try:
                        group_user = GroupUser(group_chat.id, user_id.strip())
                        db.session.add(group_user)
                    except Exception as e:
                        break
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.delete(group_chat)
                    db.session.commit()
                    self.logger.error(created_by + ' - Create Group Chat Fail - ' + str(e))
                    return 'Group creation failed, please select user in group again !!!'

            result = {'id': group_chat.id, 'group_name': group_chat.group_name, 'created_by': group_chat.created_by, 'updated_by': group_chat.updated_at, 'created_at': group_chat.created_at, 'updated_at': group_chat.updated_at}
            self.logger.info(created_by + ' - Create Group Chat Ok')
            return result

        except Exception as e:
            self.logger.error(created_by + ' - Create Group Chat Fail - ' + str(e))
            return 'Server error 1'

    def put(self, data):
        identity = get_jwt_identity()
        updated_by = identity['id']
        try:
            group_user = GroupUser.query.filter((GroupUser.group_id == data.id) & (GroupUser.user_id == updated_by)).first()
            if group_user:
                group_chat = GroupChat.query.get(data.id)
                if group_chat:
                    group_chat.group_name = data.group_name
                    group_chat.updated_by = updated_by
                    group_chat.updated_at = datetime.now()
                    db.session.commit()

                    result = {'id': group_chat.id, 'group_name': group_chat.group_name, 'created_by': group_chat.created_by, 'updated_by': group_chat.updated_at, 'created_at': group_chat.created_at, 'updated_at': group_chat.updated_at}
                    message = 'Ok'
                else:
                    result = 'Cannot find Group Chat has ID: ' + data.id + ' to Update'
                    message = result
            else:
                result = 'You do not have permission to modify this chat group !!!'
                message = result

            self.logger.info(updated_by + ' - Put Message - ' + message)
            return result

        except Exception as e:
            return 'Server Error'

    def delete(self, group_id):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            group_chat = GroupChat.query.filter((GroupChat.id == group_id.id) & (GroupChat.updated_by == user_id)).all()
            if group_chat:
                group_users = GroupUser.query.filter(GroupUser.group_id == group_chat[0].id).all()
                group_messages = GroupMessage.query.filter(GroupMessage.group_id == group_chat[0].id).all()
                for value in [group_messages, group_users, group_chat]:
                    for i in value:
                        db.session.delete(i)
                        db.session.commit()

                result = 'Delete Group Message Successfully'
            else:
                result = 'You do not have permission to delete this chat group !!!'
            self.logger.info(identity['username'] + ' - Delete Group Chat - ' + result)
            return result
        except Exception as e:
            self.logger.error(identity['username'] + ' - Delete Group Chat Fail - ' + str(e))
            return 'Server Error'

class GroupUserModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def getGroupUser(self, group_id):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            group_user = GroupUser.query.filter((GroupUser.group_id == group_id.id) & (GroupUser.user_id == user_id)).first()
            result = []
            if group_user:
                group_users = GroupUser.query.filter(GroupUser.group_id == group_id.id).all()
                for i in group_users:
                    user = User.query.get(i.user_id)
                    if user:
                        result1 = {'id': user.id, 'fullname': user.fullname, 'username': user.username, 'password': user.password, 'phone': user.phone, 'created_at': user.created_at, 'updated_at': user.updated_at}
                        result.append(result1)
                message = 'Ok'
            else:
                result = 'You are not part of this chat group !!!'
                message = result
            self.logger.info(identity['username'] + ' - Get Group User - ' + message)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' - Get Group User Fail - ' + str(e))
            return 'Server Error'
