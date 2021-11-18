from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from app.models.chat import ChatModel, ConversationModel
from app.verify import verify_message, verify_id
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument('id', type=verify_id, required=True, location='json')
parser.add_argument('message', type=verify_message, required=True, location='json')

parser_id = reqparse.RequestParser()
parser_id.add_argument('id', type=verify_id, required=True, location='json')

class Message(Resource):
    @jwt_required()
    def get(self):
        conversation_id = parser_id.parse_args()
        chat_model = ChatModel()
        result = chat_model.get(conversation_id)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        chat_model = ChatModel()
        result = chat_model.post(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def put(self):
        args = parser.parse_args()
        chat_model = ChatModel()
        result = chat_model.put(args)
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

    @jwt_required()
    def delete(self):
        message_id = parser_id.parse_args()
        chat_model = ChatModel()
        result = chat_model.delete(message_id)
        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))

class Conversation(Resource):
    @jwt_required()
    def get(self):
        # conversation_id = parser_id.parse_args()
        conversation_model = ConversationModel()
        result = conversation_model.getConversation()
        if type(result) == str:
            return make_response(jsonify({'success': False, 'message': 'fail', 'data': result}, 200))

        return make_response(jsonify({'success': True, 'message': 'success', 'data': result}, 200))
