from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
import datetime

# SETUP APP
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDo(db.Model):
    # CONFIGURE TABLE
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    body = db.Column(db.String(500), nullable=True)
    date = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=False)


class CreateToDoForm(FlaskForm):
    # WTForm
    title = StringField("To Do", validators=[DataRequired()])
    body = CKEditorField("Description", validators=[DataRequired()])
    due_date = DateTimeField("Due Date")
    submit = SubmitField("Save")


@app.route('/')
def home():
    todos = db.session.query(ToDo).all()
    return render_template("index.html", all_todos=todos)


@app.route('/todo/<int:id>')
def show_todo():
    requested_todo = ToDo.query.get(id)
    return render_template("todo.html", todo=requested_todo)


@app.route("/new-todo", methods=['GET', 'POST'])
def new_todo():
    form = CreateToDoForm()
    if form.validate_on_submit():
        print("Validated 👌")
        new_todo = ToDo(
            title=form.title.data,
            body=form.body.data,
            due_date=form.due_date.data,
            status=form.status.data,
            date=datetime.datetime.now().strftime("%B %d, %Y")
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-todo.html", form=form)


@app.route("/edit-todo/<int:id>", methods=['GET', 'POST'])
def edit_todo(id):
    todo = ToDo.query.get(id)
    form = CreateToDoForm(obj=todo)
    if form.validate_on_submit():
        print("Validated 👌")
        todo.title = form.title.data,
        todo.body = form.body.data,
        todo.due_date = form.due_date.data,
        todo.status = form.status.data,
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-todo.html", form=form)


@app.route("/delete/<int:id>")
def delete_post(id):
    todo = ToDo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)