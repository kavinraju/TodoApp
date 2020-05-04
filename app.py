from flask import Flask, render_template, url_for, request, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost:5432/todoapp'

migrate = Migrate(app, db)

# child model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# parent model
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'




@app.route('/todos/create', methods=['POST'])
def todo_create():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['todo_id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
    except:
        # session handler is rolled back to avoid the implictied commits done by the database on closing a connection.
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()  
    
    if error:
        abort(400)
    else:
        return jsonify(body)


# <todo_id> should be same as in the method argument
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:    
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        print('completed kavin ', completed, 'id = ', todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))

@app.route('/todos/delete/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True})

@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.order_by('id').all())