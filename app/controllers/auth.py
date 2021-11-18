from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from app.verify import verify_username, verify_password
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.auth import AuthModel

parser = reqparse.RequestParser()
parser.add_argument('username', type=verify_username, required=True, location='json')
parser.add_argument('password', type=verify_password, required=True, location='json')

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        auth_model = AuthModel()
        result = auth_model.login(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 401))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        auth_model = AuthModel()
        result = auth_model.refresh()
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class Logout(Resource):
    @jwt_required()
    def delete(self):
        auth_model = AuthModel()
        result = auth_model.logout(self)

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))
