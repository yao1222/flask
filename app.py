from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/flask_crud"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all() # In case user table doesn't exists already. Else remove it.

@app.route('/', methods=['GET','POST'])
#@app.route("/index")
#@app.route("/home")
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) # Add Data
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_create).all() # Read Data
        return render_template('index.html', tasks = tasks) # 1st tasks means the variable in this page

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There is a problem updating this task.'
    
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)