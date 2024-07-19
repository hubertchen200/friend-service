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
        user_id = request.args.get('user_id')
        return get_friend(user_id)

@friend_bp.route('/friend/request', methods = ["GET", "POST"])
def my_friend():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "GET":
        id = request.args.get("user_id", 0)
        return get_request(id)
    if request.method == "POST":
        my_request = request.get_json()
        return send_request(my_request["user_id"], my_request["friend_id"])



@friend_bp.route("/friend/accept", methods = ["POST"])
def friend_accept():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "POST":
        return accept(request.args.get("id"))


@friend_bp.route("/friend/decline", methods = ["POST"])
def friend_decline():
    data, code = my_jwt.check_token(request.headers)
    if code == 401:
        return jsonify(data), code
    if request.method == "POST":
        return decline(request.args.get("id"))





