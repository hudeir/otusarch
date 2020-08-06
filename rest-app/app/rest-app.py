import os
import json

from flask import Flask, request
from sqlalchemy import  create_engine

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}
engine = create_engine(config['DATABASE_URI'], echo=True)

@app.route("/health")
def health():
    return '{"status": "OK"}'

@app.route("/version")
def version():
    return '{"version": "0.1"}'

@app.route("/")
def hello():
    return 'Hello world from ' + os.environ['HOSTNAME'] + '!'

@app.route("/config")
def configuration():
    return json.dumps(config)

@app.route('/db')
def db():
    rows=[]
    with engine.connect() as connection:
        result = connection.execute("select id, username from client;")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# Add
@app.route('/user', methods=['POST'])
def add_user():
    rows=[]
    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone = request.json['phone']
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(f"insert into client(username, firstname, lastname, email, phone) values ('{username}', '{firstname}', '{lastname}', '{email}', '{phone}');")
        with connection.begin():
            result = connection.execute(f"select * from client where username = '{username}';")
            rows = [dict(r.items()) for r in result]

    return json.dumps(rows)

# Get
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    rows = []
    with engine.connect() as connection:
        result = connection.execute(f"select * from client where id = {id};")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# Update
@app.route('/user', methods=['PUT'])
def update_user():
    rows = []    
    id = request.json['id']
    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    phone = request.json['phone']
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(f"update client set username = '{username}', firstname = '{firstname}', lastname = '{lastname}', email = '{email}', phone = '{phone}' where id = {id};")
            result = connection.execute(f"select * from client where id = {id};")
            rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

# Delete
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    with engine.connect() as connection:
        connection.execute(f"delete from client where id = {id};")

    return f"user {id} deleted"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80')
