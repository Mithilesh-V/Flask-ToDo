import pandas as pd
from flask import Flask,render_template,request,jsonify,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

class logincred(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route("/app")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/")
def signin():
    return render_template("login.html")

@app.route("/signUp",methods = ["POST","GET"])
def signUp():
    if request.method == 'POST':
        username_val = request.form.get("username")
        password_val = request.form.get("password")
        new_user = logincred(username = username_val,password = password_val)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/login",methods=['POST'])
def login():
    username_val = request.form.get("username")
    password_val = request.form.get("password")
    curr = logincred.query.filter_by(username = username_val).first() 
    users = logincred.query.all()
    if curr and curr.password == password_val:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("signin"))

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run()
