from flask import Flask, json, jsonify, request, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.models.groupchat import GroupChatModel, GroupMessageModel, GroupUserModel
from app.verify import verify_group_name, verify_message, verify_id
from flask_jwt_extended import get_jwt_identity

group_chat = reqparse.RequestParser()
group_chat.add_argument('id', type=str, required=True, location='json')
group_chat.add_argument('group_name', type=verify_group_name, required=True, location='json')

group_message = reqparse.RequestParser()
group_message.add_argument('id', type=verify_id, required=True, location='json')
group_message.add_argument('message', type=verify_message, required=True, location='json')

parser_id = reqparse.RequestParser()
parser_id.add_argument('id', type=verify_id, required=True, location='json')

class GroupMessage(Resource):
    @jwt_required()
    def get(self):
        group_id = parser_id.parse_args()
        group_message_model = GroupMessageModel()
        result = group_message_model.get(group_id)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def post(self):
        args = group_message.parse_args()
        group_message_model = GroupMessageModel()
        result = group_message_model.post(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def put(self):
        args = group_message.parse_args()
        group_message_model = GroupMessageModel()
        result = group_message_model.put(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def delete(self):
        group_message_model = GroupMessageModel()
        message_id = parser_id.parse_args()
        result = group_message_model.delete(message_id)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class GroupChat(Resource):
    @jwt_required()
    def get(self):
        group_chat_model = GroupChatModel()
        result = group_chat_model.get()
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def post(self):
        args = group_chat.parse_args()
        group_chat_model = GroupChatModel()
        result = group_chat_model.post(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def put(self):
        args = group_chat.parse_args()
        group_chat_model = GroupChatModel()
        result = group_chat_model.put(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def delete(self):
        group_id = parser_id.parse_args()
        group_chat_model = GroupChatModel()
        result = group_chat_model.delete(group_id)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class GroupUser(Resource):
    @jwt_required()
    def get(self):
        group_id = parser_id.parse_args()
        group_user_model = GroupUserModel()
        result = group_user_model.getGroupUser(group_id)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))
