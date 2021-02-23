#Luke Staib 2021 - Using code from docs: flask_restful and marshmallow

#import modules
from file_uploader_ingest import *
from NLP_analysis import *
from newsfeed_ingest import *

#flask_restful and marshmallow imports
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource

#other imports
import datetime as dt

#################################

app = Flask(__name__)
api = Api(app)      

TODOS = {
	'todo1': {'task': 'Do homework'},
	'todo2': {'task': 'Enjoy the weather'},
	'todo3': {'task': 'Sleep'},
}

def abort_if_todo_doesnt_exist(todo_id):
	if todo_id not in TODOS:
		abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

# Todo: shows a single todo item and lets you delete a todo item
class Todo(Resource):
	def get(self, todo_id):
		abort_if_todo_doesnt_exist(todo_id)
		return TODOS[todo_id]

	def delete(self, todo_id):
		abort_if_todo_doesnt_exist(todo_id)
		del TODOS[todo_id]
		return '', 204

	def put(self, todo_id):
		args = parser.parse_args()
		task = {'task': args['task']}
		TODOS[todo_id] = task
		return task, 201


# TodoList: shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
	def get(self):
		return TODOS

	def post(self):
		args = parser.parse_args()
		todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
		todo_id = 'todo%i' % todo_id
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201

## Setup the Api resource routing here
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

@app.route('/')
def home():
	return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)