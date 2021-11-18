from app.model import User
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
import hashlib
from app.logger import logging_message
import logging

PATH_FILE = '/home/bacntb/app-chat/logger/auth.log'

class AuthModel():
    def __init__(self):
        self.logger = logging_message(PATH_FILE)

    def login(self, data):
        username = data.username
        password = hashlib.sha1(data.password.encode()).hexdigest()
        try:
            user = User.query.filter((User.username == username) & (User.password == password)).first()
            if user:
                access_token = create_access_token(identity={'id': user.id, 'username': user.username})
                refresh_token = create_refresh_token(identity={'id': user.id, 'username': user.username})
                result = {'id': user.id, 'username': user.username, 'password': user.password, 'access_token': access_token, 'refresh_token': refresh_token, 'created_at': user.created_at, 'updated_at': user.updated_at}
                message = 'Successfully'
            else:
                result = 'Incorrect Username or Password !!! '
                message = result

            self.logger.info(username + ' - Login - ' + message)
            return result

        except Exception as e:
            self.logger.error(username + ' - Login Fail - ' + str(e))
            return 'Server Error'

    def refresh(self):
        identity = get_jwt_identity()
        try:
            access_token = create_access_token(identity=identity)
            result = {'access_token': access_token}
            self.logger.info(identity['username'] + ' - Refresh Token Ok')
            return result

        except Exception as e:
            self.logger.error(identity['username'] + ' - Refresh Token Fail - ' + str(e))
            return 'System error, please try again!!!'

    def logout(self):
        identity = get_jwt_identity()
        try:
            self.logger.info(identity['username'] + ' - Logout OK')
            return 'Logout Successfully!!!'

        except Exception as e:
            self.logger.error(identity['username'] + ' - Logout Fail - ' + str(e))
            return 'System error, please try again!!!'
