from flask import Flask, request, jsonify
from datetime import datetime
import pymysql

app = Flask(__name__)

# Database
def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host='hagisuda.mysql.pythonanywhere-services.com',
            database='flaskapi',
            user='hagisuda',
            password='flaskapi1234',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route('/', methods=['GET'])
def index():
    return jsonify({'msg':"Connected successfully!"})

#Get all posts
@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    conn = db_connection()
    jsons = []
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM posts')
            rows = cur.fetchall()
            for row in rows:
                jsons.append(to_json_post(row))
    finally:
        conn.close()

    return jsonify(jsons)

#Get all users
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    conn = db_connection()
    jsons = []
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users')
            rows = cur.fetchall()
            for row in rows:
                jsons.append(to_json_user(row))
    finally:
        conn.close()

    return jsonify(jsons)

# Create a post
@app.route('/api/v1/post', methods=['POST'])
def add_post():
    conn = db_connection()
    cursor = conn.cursor()
    desc = request.json['desc']
    photo = request.json['photo']
    user_id = request.json['user_id']
    new_id = 0
    try:
        with conn.cursor() as cur:
            sql = """INSERT INTO posts (`user_id`, `desc`, `photo`, `created_dt`, `like`, `comment`) VALUES(%s, %s, %s)"""
            cur.execute(sql, (user_id, desc, photo, datetime.now(), 0, 0)) 
            new_id = cur.lastrowid;
            conn.commit()
    finally:
        conn.close()
        
    return jsonify({'id':new_id})

def to_json_post(row):
    return {
        "id" : row['id'],
        "desc" : row['desc'],
        "photo" : row['photo'],
        "user_id" : row['user_id'],
        "date" : row['created_dt'],
        "like" : row['like'],
        "comment" : row['comment'],
    }

def to_json_user(row):
    return {
        "id" : row['id'],
        "username" : row['username'],
        "profile_picture" : row['profile_picture'],
    }

if __name__ == "__main__":
    app.run(debug=True)
