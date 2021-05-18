import sqlite3

from db import db


class TodoModel(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def __init__(self, todo, user_id):
        self.todo = todo
        self.user_id = user_id

    def json(self):
        return {"id": self.id, "todo": self.todo}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM todos WHERE id=?"
        # result = cursor.execute(query, (int(todo_id),))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return {"todo": {"id": row[0], "task": row[1]}}
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_todo(cls, todo):
        return cls.query.filter_by(todo=todo)

    @classmethod
    def find_all(cls):
        return cls.query.all()
