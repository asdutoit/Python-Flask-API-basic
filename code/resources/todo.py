import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.todo import TodoModel


class AllTodos(Resource):
    @jwt_required()
    def get(self):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM todos"
        # result = cursor.execute(query)
        # print(result)
        # print(type(result))
        # row = result.fetchall()
        # return {"todos": row}, 200
        todos = [todo.json() for todo in TodoModel.find_all()]
        return todos


class AllTodosByUser(Resource):
    @jwt_required()
    def get(self):
        todos = [todo.json() for todo in TodoModel.find_all_by_user(current_identity.id)]
        return todos


class Todo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("task", type=str, required=True, help="This field cannot be blank")

    def get(self, todo_id):
        todo = TodoModel.find_by_id(todo_id)
        if todo:
            return todo.json()
        return {"message": "Item not found"}, 500  # Internal server error

    def put(self, todo_id):
        data = self.parser.parse_args()

        todo = TodoModel.find_by_id(todo_id)

        if todo:
            todo.todo = data["task"]
        else:
            todo = TodoModel(data["task"], current_identity.id)

        todo.save_to_db()

        return todo.json()

    @jwt_required()
    def post(self, todo_id):
        data = Todo.parser.parse_args()
        try:
            todo = TodoModel(data["task"], current_identity.id)
            todo.save_to_db()
            return todo.json(), 201
        except:
            return {"message": "An error occured inserting the item"}

        # return data, 201

    @jwt_required()
    def delete(self, todo_id):
        todo = TodoModel.find_by_id(todo_id)

        if todo:
            todo.delete_from_db()
            return {"message": "todo deleted"}, 200
        return {"message": "No todo found"}, 404
