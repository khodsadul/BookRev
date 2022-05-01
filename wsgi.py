import uuid
from datetime import datetime

from flask import Flask, jsonify, request, render_template
from sqlalchemy import Column, String, DateTime, Integer
from flask_mail import Mail, Message

import api.config as config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow(app)

app.config.from_object(config.DevelopmentConfig)

mail = Mail(app)

db = SQLAlchemy(app)


@app.route('/user/id/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user_schema.dump(user))


@app.route('/user/email/<user_email>', methods=['GET'])
def get_user(user_email):
    user = User.query.filter_by(email=user_email).first()
    return jsonify(success=True, data=user_schema.dump(user), message="Record retrieved successfully.")


@app.route("/user/all")
def print_all_user():
    user_data = User.query.all()
    return jsonify(success=True, data=users_schema.dump(user_data), message="Records retrieved successfully.")


def send_email(user):
    message = Message(subject="Welcome to BookRev!! {}".format(user.full_name), recipients=[user.email])
    message.html = render_template("mail.html", user=user, href="https://laxmi-portfolio.herokuapp.com/")
    # message.body = render_template("mail.txt", user=user)
    mail.send(message)


@app.route("/user/add", methods=['POST'])
def add_user():
    user_data = request.get_json()
    email = user_data.get("email")
    exsting_user = User.query.filter_by(email=email).first()
    user_name = user_data.get('name')
    password = user_data.get('password')
    if exsting_user is not None:
        return jsonify(success=False, data=None, message="email already exist.")
    if len(user_name) <= 0:
        return jsonify(success=False, data=None, message="Name can not be empty.")
    if len(password) < 8:
        return jsonify(success=False, data=None, message="Password too short.")

    user = User(full_name=user_data.get('name'), email=user_data.get('email'), password=user_data.get('password'),
                dob=datetime.strptime(user_data.get('dob'), "%Y-%m-%d %H:%M:%S"))
    db.session.add(user)
    db.session.commit()
    send_email(user)
    return jsonify(success=True, data=user_schema.dump(user), message="Record added successfully.")


@app.route("/user/", methods=['PUT'])
def update_user():
    user_data = request.get_json()
    return jsonify(data=user_data)


@app.route("/user/name/<name>")
def book_get(name):
    book_data = Book.querry.filtter_by(name=name).first()
    return jsonify(success=True, data=book_schema.dump(book_data), message="Record added successfully.")


@app.route("/book/add", methods=["POST"])
def add_book():
    book_data = request.get_json()
    name = book_data.get("name")
    author = book_data.get("author")
    ratting = book_data.get("ratting")
    description = book_data.get("description")
    created_by = book_data.get("created_by")
    modified_by = book_data.get('modified_by')

    if len(name) <= 0:
        return jsonify(success=False, data=None, message="Name can not be empty.")

    book = Book(name=name, author=author, ratting=ratting,
                description=description, created_by=created_by, modified_by=modified_by)
    db.session.add(book)
    db.session.commit()
    return jsonify(success=True, data=book_schema.dump(book), message="Record added successfully.")


@app.route("/user-book/add", methods=["POST"])
def add_user_book():
    user_book_data = request.get_json()
    ratting = user_book_data.get("ratting")
    user_id = user_book_data.get("user_id")
    book_id = user_book_data.get("book_id")
    created_by = user_book_data.get("created_by")
    modified_by = user_book_data.get('modified_by')
    user_book = User_Book(user_id=user_id, book_id=book_id, ratting=ratting, created_by=created_by,
                          modified_by=modified_by)
    db.session.add(user_book)
    db.session.commit()
    return jsonify(success=True, data=book_schema.dump(user_book), message="Record added successfully.")


@app.route("/book/all")
def get_all_books():
    book_data = Book.query.all()
    return jsonify(success=True, data=books_schema.dump(book_data), message="record get successfully")


@app.route("/user-book/all")
def get_all_book_user():
    user_book_data = User_Book.query.all()
    return jsonify(success=True, data=user_books_schema.dump(user_book_data), message="record get successfully")


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'boook_review'}
    id = Column(String, name='id', primary_key=True, default=generate_uuid)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    status = Column(String, nullable=False, default='INA')
    dob = Column(DateTime)
    created_by = Column(String, nullable=False, default="system-user")
    creation_dttm = Column(DateTime, nullable=False, default=datetime.now())
    modified_by = Column(String, nullable=False, default="system-user")
    modification_dttm = Column(DateTime, nullable=False, default=datetime.now())
    version = Column(Integer, nullable=False, default=0)
    verification_token = Column(String, nullable=False, default='12345')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'full_name', 'email', 'status', 'dob', 'status', 'creation_dttm', 'version')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Book(db.Model):
    __tablename__ = "book"
    __table_args__ = {'schema': 'boook_review'}
    id = Column(String, name='id', primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String)
    author = Column(String, nullable=False)
    created_by = Column(String, nullable=False, default="system-user")
    creation_dttm = Column(DateTime, nullable=False, default=datetime.now())
    modified_by = Column(String, nullable=False, default="system-user")
    modification_dttm = Column(DateTime, nullable=False, default=datetime.now())
    version = Column(Integer, nullable=False, default=0)
    ratting = Column(Integer, nullable=False)


class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'author', 'ratting', 'description', 'created_by', 'creation_dttm', 'modified_by',
                  'modification_dttm', 'version')


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class User_Book(db.Model):
    __tablename__ = "user_book"
    __table_args__ = {"schema": "boook_review"}
    user_id = Column(String, primary_key=True, nullable=False)
    book_id = Column(String, primary_key=True, nullable=False)
    ratting = Column(Integer, nullable=False)
    created_by = Column(String, nullable=False, default="system-user")
    creation_dttm = Column(DateTime, nullable=False, default=datetime.now())
    modified_by = Column(String, nullable=False, default="system-user")
    modification_dttm = Column(DateTime, nullable=False, default=datetime.now())
    version = Column(Integer, nullable=False, default=0)


class User_BookSchema(ma.Schema):
    class Meta:
        fields = ('user_id', "book_id", 'ratting', 'created_by', 'creation_dttm', 'modified_by',
                  'modification_dttm', 'version')


user_book_schema = BookSchema()
user_books_schema = BookSchema(many=True)

if __name__ == '__main__':
    app.run()
