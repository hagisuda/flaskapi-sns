import pymysql

conn = pymysql.connect(
    host='localhost',
    database='test',
    user='root',
    password='',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()
create_user_table_query = """
CREATE TABLE users (
    `id` integer PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `profile_picture` varchar(500)
)
"""
cursor.execute(create_user_table_query)

create_post_table_query = """
CREATE TABLE posts (
    `id` integer PRIMARY KEY AUTO_INCREMENT,
    `user_id` integer NOT NULL,
    `desc` text NOT NULL,
    `photo` varchar(500),
    `created_dt` datetime NOT NULL,
    `like` integer,
    `comment` integer
)
"""
cursor.execute(create_post_table_query)

conn.close()