from flask import Flask, render_template, url_for, request, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:skr123@localhost:5432/todoapp'

# #1stThing 
#  Initialize Flask-Migrate -  linking it to the Flask app models and database, 
# link to command line scripts for running migrations, set up folders to store migrations
migrate = Migrate(app,db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# db.create_all() - we need not have this here as we want the migrate versions to take care of create a table...
# #2ndThing - Run python -m flask db init so that it creates migration folder + necessary files
# #3rdThing - Run python -m flask db migrate to create a migrate script under versions folder. If any changes to be done can be done there.
# #4thThing - Run python -m flask db updrade to roll-out the DB upgrade


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