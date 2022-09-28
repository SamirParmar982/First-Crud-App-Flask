from flask import Flask, render_template, url_for ,request , redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.db'  # 3 slash for relative path and 4 for absolute path  
db = SQLAlchemy(app)    # creating data base , initializing database

# creating a model 
class Todo(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    content = db.Column(db.String(200),nullable = False)
    completed = db.Column(db.Integer , default=0)
    date_created = db.Column(db.DateTime , default=datetime.utcnow)   #import datetime 

#creating function that will return string everytime inside class
    def __repr__(self):
        # return way to write for database
        return '<Task %r>' % self.id
    

@app.route('/', methods=['POST','GET'])  #methods post will send data to our database and vice-versa

def index():
    if request.method == 'POST':
        task_content = request.form['content'] # variable task_content is taking request from form created in index.html  
           #  ['content']  is value in  form i.e; name = "content"
        # creating Todo object below because we have Todo model 
        new_task = Todo(content = task_content)

        #Pushing it to the database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()          # see all the data created and .all() we could write.first()                   
        return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')     # id is from class Todo

def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']   # current task content to the request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating that task'
    else:
        return render_template('update.html',task = task)

if __name__ == "__main__":
    app.run(debug = True)
