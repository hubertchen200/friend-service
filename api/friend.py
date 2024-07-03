from api.utils import get_connection
from flask import jsonify
import json
import datetime


def get_request(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        select_query = 'select * from requests where receiver = %s'
        select_data = (user_id,)
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

def send_request(user_id, friend_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "select * from users where id = %s"
        select_data = (friend_id, )
        cursor.execute(select_query, select_data)
        row = cursor.fetchall()
        if len(row) == 0:
            return jsonify({"error": "failed to find friend"})
        insert_query = "insert into requests (sender, receiver) values (%s, %s)"
        insert_data = (user_id, friend_id)
        cursor.execute(insert_query, insert_data)
        conn.commit()
        return jsonify(insert_data), 201
    except Exception as e:
        return jsonify({"error": f"message: {e}"})


def decline(id):
    conn = get_connection()
    cursor = conn.cursor()
    delete_query = 'delete from requests where id = %s'
    delete_data = (id,)
    cursor.execute(delete_query, delete_data)
    conn.commit()
    return json.dumps({"status": "request declined success fully"})


def accept(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        insert_query = 'insert into friends (user1, user2, timestamp) values (%s, %s, %s)'
        select_query = 'select * from requests where id = %s'
        select_data = (id,)
        cursor.execute(select_query, select_data)
        row = cursor.fetchall()
        insert_data = (row[0][1],row[0][2],datetime.datetime.now())
        cursor.execute(insert_query, insert_data)
        delete_query = 'delete from requests where id = %s'
        delete_data = (id,)
        cursor.execute(delete_query, delete_data)
        conn.commit()
        return jsonify({'status':'request accepted'})
    except Exception as e:
        return jsonify({"error": f"message: {e}"})
# accept(2)
