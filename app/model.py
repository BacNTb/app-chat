from app.connection import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__  = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    def __init__(self, fullname, username, password, phone):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.phone = phone

class Message(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, conversation_id, user_id):
        self.message = message
        self.conversation_id = conversation_id
        self.user_id = user_id

class Conversation(db.Model):
    __tablename__  = 'conversations'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    user_1 = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    user_2 = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2

class GroupChat(db.Model):
    __tablename__  = 'groupchats'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    group_name = db.Column(db.String(100))
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime())

    def __init__(self, group_name, created_by):
        self.group_name = group_name
        self.created_by = created_by

class GroupUser(db.Model):
    __tablename__  = 'groupusers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    group_id = db.Column(db.String(36), db.ForeignKey('groupchats.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

class GroupMessage(db.Model):
    __tablename__  = 'groupmessages'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    group_id = db.Column(db.String(36), db.ForeignKey('groupchats.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, group_id, user_id):
        self.message = message
        self.group_id = group_id
        self.user_id = user_id


if __name__ == '__main__':
    db.create_all()