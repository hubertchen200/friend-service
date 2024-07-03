from . import friend_bp
from flask import request, jsonify
from api.friend import get_request, send_request, accept, decline
from api.jwt_token.my_jwt import jwt_decode

@friend_bp.route('/friend/request', methods = ["GET", "POST"])
def my_friend():
    token = request.headers.get('Authorization')
    token = token.replace("Bearer ", "")
    payload = jwt_decode(token)
    if payload == "TOKEN_EXPIRED":
        return jsonify({'error': "TOKEN_EXPIRED"})
    if payload == "INVALID_TOKEN":
        return jsonify({'error': 'INVALID_TOKEN'})

    if request.method == "GET":
        id = request.args.get("user_id", 0)
        return get_request(id)
    if request.method == "POST":
        my_request = request.get_json()
        return send_request(my_request["user_id"], my_request["friend_id"])



@friend_bp.route("/friend/accept", methods = ["POST"])
def friend_accept():
    token = request.headers.get('Authorization')
    token = token.replace("Bearer ", "")
    payload = jwt_decode(token)
    if payload == "TOKEN_EXPIRED":
        return jsonify({'error': "TOKEN_EXPIRED"})
    if payload == "INVALID_TOKEN":
        return jsonify({'error': 'INVALID_TOKEN'})
    if request.method == "POST":
        return accept(request.args.get("id"))


@friend_bp.route("/friend/decline", methods = ["POST"])
def friend_decline():
    token = request.headers.get('Authorization')
    token = token.replace("Bearer ", "")
    payload = jwt_decode(token)
    if payload == "TOKEN_EXPIRED":
        return jsonify({'error': "TOKEN_EXPIRED"})
    if payload == "INVALID_TOKEN":
        return jsonify({'error': 'INVALID_TOKEN'})
    if request.method == "POST":
        return decline(request.args.get("id"))





