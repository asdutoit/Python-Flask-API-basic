import sqlite3

from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    todos = db.relationship("TodoModel", lazy="dynamic")

    def __init__(self, username, password):
        # self.id = id
        self.username = username
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "name": self.username,
            "todos": [todo.json() for todo in self.todos.all()],
        }  # Remove .all() if you remove lazy="dynamic" at the todos relationship statement

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def __str__(self):
    #     return "User(id='%s')" % self.id

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # if row:
        #     user = cls(row[0], row[1], row[2])
        # else:
        #     user = None

        # connection.close()
        # return user
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # if row:
        #     user = cls(row[0], row[1], row[2])
        # else:
        #     user = None

        # connection.close()
        # return user
        return cls.query.filter_by(id=_id).first()
