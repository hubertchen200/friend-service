from . import friend_bp
from flask import request, jsonify
from api.friend import get_request, send_request, get_friend, accept, decline
from hubertchen_package import my_jwt


@friend_bp.route('/friends', methods = ["GET"])
def my_friends():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "GET":
        username = request.args.get('username')
        return get_friend(username)

@friend_bp.route('/friend/request', methods = ["GET", "POST"])
def my_friend():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "GET":
        username = request.args.get("username")
        return get_request(username)
    if request.method == "POST":
        my_request = request.get_json()
        result = send_request(my_request["sender"], my_request["receiver"])
        if 'error' in result.keys():
            return jsonify(result), 400
        return jsonify(result), 200



@friend_bp.route("/friend/accept", methods = ["POST"])
def friend_accept():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "POST":
        receiver = data['data']['username']
        result = accept(request.args.get("sender"), receiver)
        if 'error' in result:
            return jsonify(result), 400
        return jsonify(result), 200

@friend_bp.route("/friend/decline", methods = ["POST"])
def friend_decline():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "POST":
        receiver = data['data']['username']
        return decline(request.args.get("sender"), receiver)





