from flask import Flask, render_template, url_for, request, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:skr123@localhost:5432/todoapp'

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/todos/create', methods=['POST'])
def todo_create():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
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


@app.route('/')
def index():
    return render_template('index.html',data=Todo.query.all())