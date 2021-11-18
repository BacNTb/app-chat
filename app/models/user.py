from app.model import User
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
import hashlib
from app.connection import db
from app.logger import logging_message

PATH_FILE = '/home/bacntb/app-chat/logger/user.log'

class UserModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def getAll(self):
        identity = get_jwt_identity()
        try:
            users = User.query.order_by(User.created_at).all()
            result = []
            if users:
                for user in users:
                    data = {'id': user.id, 'fullname': user.fullname, 'username': user.username, 'password': user.password, 'phone': user.phone, 'created_at': user.created_at, 'updated_at': user.updated_at}
                    result.append(data)

            self.logger.info(identity['username'] + ' - Get All User')
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' Get All User Fail ' + str(e))
            return 'Server Error'

    def getById(self, user_id):
        identity = get_jwt_identity()
        try:
            user = User.query.get(user_id)
            result = []
            if user:
                result_1 = {'id': user.id, 'fullname': user.fullname, 'username': user.username, 'password': user.password, 'phone': user.phone, 'created_at': user.created_at, 'updated_at': user.updated_at}
                result.append(result_1)

            self.logger.error(identity['username'] + ' Get User By ID ' + user_id.id)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' Get User By ID Fail' + str(e))
            return 'Server Error'

    def getByUsername(self, key):
        identity = get_jwt_identity()
        try:
            users = User.query.filter(User.username.like('%{}%'.format(key.name))).order_by(User.created_at).all()
            result = []
            if users:
                for user in users:
                    data = {'id': user.id, 'fullname': user.fullname, 'username': user.username, 'password': user.password, 'phone': user.phone, 'created_at': user.created_at, 'updated_at': user.updated_at}
                    result.append(data)

            self.logger.info(identity['username'] + ' Get User By Username ' + key.name)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' Get User By Username ' + str(e))
            return 'Server Error'

    def getByFullname(self, key):
        identity = get_jwt_identity()
        try:
            users = User.query.filter(User.fullname.like('%{}%'.format(key.name))).order_by(User.created_at).all()
            result = []
            if users:
                for user in users:
                    data = {'id': user.id, 'fullname': user.fullname, 'username': user.username, 'password': user.password, 'phone': user.phone, 'created_at': user.created_at, 'updated_at': user.updated_at}
                    result.append(data)

            self.logger.info(identity['username'] + ' Get User By Fullname ' + key.name)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' Get User By Fullname ' + str(e))
            return 'Server Error'

    def post(self, data):
        username = data.username
        try:
            user = User.query.filter(User.username == username).first()
            if user:
                result = 'Username already exists, please enter another name'
                message = result
            else:
                fullname = data.fullname
                password = hashlib.sha1(data.password.encode()).hexdigest()
                phone = data.phone

                my_data = User(fullname, username, password, phone)
                db.session.add(my_data)
                db.session.commit()

                result = {'id': my_data.id, 'fullname': fullname, 'username': username, 'password': password, 'phone': phone, 'status': my_data.status, 'created_at': my_data.created_at, 'updated_at': my_data.updated_at}
                message = 'Successfully'

            self.logger.info(username + ' - Add User - ' + message)
            return result

        except Exception as e:
            self.logger.error(username + ' Add User Fail ' + str(e))
            return 'Server Error'

    def put(self, user_id, data):
        identity = get_jwt_identity()
        try:
            if identity['id'] == user_id.id:
                user = User.query.get(user_id)
                if user:
                    duplicate_user = User.query.filter((User.username == data.username) & (User.id != user_id.id)).first()
                    if duplicate_user:
                        result = 'Username already exists, please enter another name'
                        message = result
                    else:
                        user.username = data.username
                        user.fullname = data.fullname
                        user.password = hashlib.sha1(data.password.encode()).hexdigest()
                        user.phone = data.phone
                        user.updated_at = datetime.now()
                        db.session.commit()

                        result = {'id': user.id, 'fullname': user.fullname, 'username': user.username, 'password': user.password, 'phone': user.phone, 'created_at': user.created_at, 'updated_at': user.updated_at}
                        message = 'Update successfully'
                else:
                    result = 'Cannot find User has ID: ' + user_id.id + ' to Update'
                    message = result
            else:
                result = 'You do not have permission to edit this user !!!'
                message = result

            self.logger.info(identity['username'] + ' - Update User - ' + message)
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' - Update User Fail - ' + str(e))
            return 'Server Error'

    def delete(self, user_id):
        identity = get_jwt_identity()
        try:
            if identity['id'] == user_id.id:
                user = User.query.get(user_id)
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    result = 'Delete User Successfully'
                else:
                    result = 'Cannot find User has ID: ' + user_id.id + ' to Delete'
            else:
                result = 'You do not have permission to delete this user !!!'

            self.logger.info(identity['username'] + ' - ' + result)
            return result

        except Exception as e:
            self.logger.error('Delete User Fail - ' + str(e))
            return 'Server Error'