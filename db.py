#db.py
import os
import pymysql
from flask import jsonify

db_user = os.environ.get('sonali')
db_password = os.environ.get('123456789')
db_name = os.environ.get('menu')
db_connection_name = os.environ.get('chatbot-wsrv:asia-south2:menu-details')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn


def fetch_data(name):
    conn = open_connection()
    with conn.cursor() as cursor:
        if name == 'unknown':
            result = cursor.execute('SELECT Top 5 FROM ratings order by ratings DESC limit 5;')
            data = cursor.fetchall()
            if result > 0:
                details = jsonify(data)
            else:
                details = 'No data available'
        else:
            result = cursor.execute(f'select * from order.csv where Name = {name}; ')
            data = cursor.fetchall()
            if result > 0:
                details = jsonify(data)

            else:
                details = 'No data available'
        conn.close()
        return details

def add_data(song):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO songs (title, artist, genre) VALUES(%s, %s, %s)', (song["title"], song["artist"], song["genre"]))
    conn.commit()
    conn.close()

def details():
    pass

