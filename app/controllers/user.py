from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from app.models.user import UserModel
from flask_jwt_extended import jwt_required
from app.verify import verify_fullname, verify_username, verify_password, verify_phone, verify_id, verify_message

parser = reqparse.RequestParser()
parser.add_argument('fullname', type=verify_fullname, required=True, location='json')
parser.add_argument('username', type=verify_username, required=True, location='json')
parser.add_argument('password', type=verify_password, required=True, location='json')
parser.add_argument('phone', type=verify_phone, required=True, location='json')

parser_id = reqparse.RequestParser()
parser_id.add_argument('id', type=verify_id, required=True, location='json')

parser_name = reqparse.RequestParser()
parser_name.add_argument('name', type=verify_message, required=True, location='json')

class User(Resource):
    @jwt_required()
    def get(self):
        user_model = UserModel()
        result = user_model.getAll()
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 500))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    # @jwt_required()
    def post(self):
        args = parser.parse_args()
        user_model = UserModel()
        result = user_model.post(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 500))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def put(self):
        user_id = parser_id.parse_args()
        args = parser.parse_args()
        user_model = UserModel()
        result = user_model.put(user_id, args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 500))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def delete(self):
        user_id = parser_id.parse_args()
        user_model = UserModel()
        result = user_model.delete(user_id)
        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class UserID(Resource):
    '''Get User By ID'''

    @jwt_required()
    def get(self):
        user_id = parser_id.parse_args()
        user_model = UserModel()
        result = user_model.getById(user_id)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 500))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class UserUsername(Resource):
    '''Get User By Username'''

    @jwt_required()
    def get(self):
        username = parser_name.parse_args()
        user_model = UserModel()
        result = user_model.getByUsername(username)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 500))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class UserFullname(Resource):
    '''Get User By Fullname'''

    @jwt_required()
    def get(self):
        fullname = parser_name.parse_args()
        user_model = UserModel()
        result = user_model.getByFullname(fullname)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 500))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))
