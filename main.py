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
    due_date = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=False)


class CreateToDo(FlaskForm):
    # WTForm
    title = StringField("To Do", validators=[DataRequired()])
    body = CKEditorField("Description", validators=[DataRequired()])
    due_date = DateTimeField("Due Date")
    submit = SubmitField("Save")


if __name__ == '__main__':
    app.run(debug=True)
