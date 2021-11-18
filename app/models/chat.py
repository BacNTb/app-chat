from flask_jwt_extended import get_jwt_identity
from app.connection import db
from app.model import User, Conversation, Message
from datetime import datetime
from app.logger import logging_message

PATH_FILE = '/home/bacntb/app-chat/logger/chat.log'

class ChatModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def get(self, conversation_id):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            conversation = Conversation.query.filter(((Conversation.id == conversation_id.id) & (Conversation.user_1 == user_id)) | ((Conversation.id == conversation_id.id) & (Conversation.user_2 == user_id))).first()
            result = []
            if conversation:
                messages = Message.query.filter(Message.conversation_id == conversation_id.id).order_by(Message.created_at).all()
                if messages:
                    for i in messages:
                        mess = {'id': i.id, 'conversation_id': i.conversation_id, 'user_id': i.user_id, 'message': i.message, 'created_at': i.created_at, 'updated_at': i.updated_at}
                        result.append(mess)
            self.logger.info(identity['username'] + ' Get Message Ok')
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' - Get Message Fail - ' + str(e))
            return 'Server Error'

    def post(self, data):
        identity = get_jwt_identity()
        user_id = identity['id']
        username = identity['username']
        try:
            conversation = Conversation.query.filter(((Conversation.user_1 == user_id) & (Conversation.user_2 == data.id)) | ((Conversation.user_1 == data.id) & (Conversation.user_2 == user_id))).first()
            conversation_id = conversation.id if conversation else False
            if conversation_id == False:
                my_conversation = Conversation(user_id, data.id)
                db.session.add(my_conversation)
                db.session.commit()
                conversation_id = my_conversation.id

            my_message = Message(data.message, conversation_id, user_id)
            db.session.add(my_message)
            db.session.commit()
            result = {'id': my_message.id, 'conversation_id': conversation_id, 'user_id': user_id, 'message': data.message,'created_at': my_message.created_at, 'updated_at': my_message.updated_at}

            self.logger.info(username + ' - Post Message Ok')
            return result

        except Exception as e:
            self.logger.error(username + ' - Post Message Fail - ' + str(e))
            return 'Server Error'

    def put(self, data):
        identity = get_jwt_identity()
        user_id = identity['id']
        username = identity['username']
        try:
            message = Message.query.filter((Message.id == data.id) & (Message.user_id == user_id)).first()
            if message:
                message.message = data.message
                message.updated_at = datetime.now()
                db.session.commit()

                result = {'id': message.id, 'conversation_id': message.conversation_id, 'user_id': message.user_id, 'message': data.message, 'created_at': message.created_at, 'updated_at': message.updated_at}
                message = 'Update Message Ok'
            else:
                result = 'You do not have permission to edit this message !!!'
                message = result

            self.logger.info(username + ' - Update Message - ' + message)
            return result

        except Exception as e:
            self.logger.error(username + ' - Update Message Fail - ' + str(e))
            return 'Server Error'

    def delete(self, message_id):
        identity = get_jwt_identity()
        user_id = identity['id']
        username = identity['username']
        try:
            message = Message.query.filter((Message.id == message_id.id) & (Message.user_id == user_id)).first()
            if message:
                db.session.delete(message)
                db.session.commit()
                result = 'Delete Message Successfully'
            else:
                result = 'You do not have permission to delete this message !!!'

            self.logger.info(username + ' - ' + result)
            return result

        except Exception as e:
            return 'Server Error'

class ConversationModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def getConversation(self):
        identity = get_jwt_identity()
        user_id = identity['id']
        try:
            conversation_ids =  Conversation.query.filter((Conversation.user_1 == user_id) | (Conversation.user_2 == user_id)).all()
            conversation_id = []
            if conversation_ids:
                for conversation in conversation_ids:
                    conversation_id.append(conversation.id)

            self.logger.info(identity['username'] + ' - Get Conversation OK')
            return conversation_id

        except Exception as e:
            self.logger.error(identity['username'] + ' - Get Conversation Fail ' + str(e))
            return 'Server Error'
