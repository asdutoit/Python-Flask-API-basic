import os
from security import authenticate, identity
from resources.user import UserRegister
from resources.todo import Todo, AllTodos, AllTodosByUser
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from db import db

# os.system("python create_tables.py")

app = Flask(__name__)
app.config["SECRET_KEY"] = "stephan"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://asdutoit:peanuts@127.0.0.1/data"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(hours=1)
app.config["JWT_AUTH_HEADER_PREFIX"] = "Bearer"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token, ident):
    return jsonify({"access_token": access_token.decode("utf-8"), "user_id": ident.id, "username": ident.username})


api.add_resource(AllTodos, "/todos")
api.add_resource(AllTodosByUser, "/todos_by_user")
api.add_resource(Todo, "/todo/<string:todo_id>")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
