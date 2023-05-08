from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeLocalField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
from flask_bootstrap import Bootstrap5
import datetime

# SETUP APP
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)

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
    # due_date = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(6), default='todo', nullable=False)

    def __repr__(self):
        return '<ToDo %r>' % self.title

# Setup create a new DB and Tables
# with app.app_context():
#     db.create_all()


class CreateToDoForm(FlaskForm):
    # WTForm
    title = StringField("Name", validators=[DataRequired()])
    body = CKEditorField("Description", validators=[DataRequired()])
    # due_date = DateTimeLocalField("Due Date")
    status = HiddenField()
    submit = SubmitField("Save")


@app.route('/')
def home():
    todos = db.session.query(ToDo).all()
    return render_template("index.html", all_todos=todos)


@app.route('/todo/<int:id>')
def show_todo(id):
    requested_todo = ToDo.query.get(id)
    return render_template("todo.html", todo=requested_todo)


@app.route("/add_todo", methods=['GET', 'POST'])
def add_todo():
    status = request.args.get("status", default="todo", type=str)
    form = CreateToDoForm(status=status)
    if form.validate_on_submit():
        print("Validated 👌")
        new_todo = ToDo(
            title=form.title.data,
            body=form.body.data,
            # due_date=form.due_date.data,
            date=datetime.datetime.now().strftime("%B %d, %Y")
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-todo.html", form=form, todo='')


@app.route("/edit_todo/<int:id>", methods=['GET', 'POST'])
def edit_todo(id):
    todo = ToDo.query.get(id)
    form = CreateToDoForm(obj=todo)
    if form.validate_on_submit():
        print("Validated 👌")
        todo.title = form.title.data
        todo.body = form.body.data
        # todo.due_date = form.due_date.data
        # todo.status = form.status.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-todo.html", form=form, todo=todo)


@app.route("/change_status/<int:id>")
def change_status(id):
    todo = ToDo.query.get(id)
    print(f"Orignal status {todo.status}")
    todo.status = request.args.get("status", default="todo", type=str)
    db.session.commit()
    print(f"Changed to {todo.status}")
    return redirect(url_for('home'))


@app.route("/delete/<int:id>")
def delete_todo(id):
    todo = ToDo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
