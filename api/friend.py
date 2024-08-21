from api.utils import get_connection
from flask import jsonify
import json
import datetime

def get_friend(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "select * from friends where user1 = %s or user2 = %s"
        select_data = (username, username)
        cursor.execute(select_query, select_data)
        rows = cursor.fetchall()
        friends = []
        for row in rows:
            friend = {
                "id": row[0],
                "user1": row[1],
                "user2": row[2],
                "timestamp": row[3],
            }
            friends.append(friend)
        return jsonify({'status':'success', 'data': friends})
    except Exception as e:
        return jsonify({"error": f"message:{e}"})

def get_request(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        select_query = 'select * from requests where receiver = %s'
        select_data = (username,)
        cursor.execute(select_query, select_data)
        rows = cursor.fetchall()
        requests = []
        for row in rows:
            request = {
                "id": row[0],
                "sender": row[1],
                "receiver": row[2],
            }
            requests.append(request)
        print(json.dumps(requests, indent=4))
        return json.dumps(requests)
    except Exception as e:
        print(f"failed: {e}")
        return jsonify({"error": f"message: {e}"})


def send_request(sender, receiver):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "select * from users where username = %s"
        select_data = (receiver, )
        cursor.execute(select_query, select_data)
        row = cursor.fetchall()
        if len(row) == 0:
            return jsonify({"error": "failed to find friend"})
        insert_query = "insert into requests (sender, receiver) values (%s, %s)"
        insert_data = (sender, receiver)
        cursor.execute(insert_query, insert_data)
        conn.commit()
        result = {"sender": sender, "receiver": receiver}
        return result
    except Exception as e:
        return {"error": f"message: {e}"}


def decline(sender, receiver):
    conn = get_connection()
    cursor = conn.cursor()
    delete_query = 'delete from requests where sender = %s and receiver = %s'
    delete_data = (sender, receiver)
    cursor.execute(delete_query, delete_data)
    conn.commit()
    return json.dumps({"status": "request declined success fully"})


def accept(sender, receiver):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        select_query = 'select * from requests where sender = %s and receiver = %s'
        select_data = (sender, receiver)
        cursor.execute(select_query, select_data)
        row = cursor.fetchall()
        if len(row) != 1:
            return jsonify({'error': 'No friend request.'})

        insert_query = 'insert into friends (user1, user2, timestamp) values (%s, %s, %s)'
        insert_data = (sender, receiver,datetime.datetime.now())
        cursor.execute(insert_query, insert_data)

        delete_query = 'delete from requests where id = %s'
        delete_data = (row[0][0],)
        cursor.execute(delete_query, delete_data)
        conn.commit()
        return {'status':'request accepted'}
    except Exception as e:
        return {"error": f"message: {e}"}
# accept(2)
