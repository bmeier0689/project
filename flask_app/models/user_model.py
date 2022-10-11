from flask import flash
import re
from final_project.flask_app.config.mysqlconnection import connectToMySQL
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.order_model import Order

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^(?P<password>((?=\S*[A-Z])(?=\S*[a-z])(?=\S*\d)(?=\S*[\!\"\§\$\%\&\/\(\)\=\?\+\*\#\'\^\°\,\;\.\:\<\>\ä\ö\ü\Ä\Ö\Ü\ß\?\|\@\~\´\`\\])\S{8,}))+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
db = 'obake_sushi'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.orders = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, address, city, state, email, password) \
        VALUES ( %(first_name)s, %(last_name)s, %(address)s, %(city)s, %(state)s, %(email)s, %(password)s );"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def check_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, {'email': email})
        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, address = %(address)s, \
        city = %(city)s, state = %(state)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        if len(results) >= 1:
            flash("Email is already in use. Please login or register a new email address", "register")
            is_valid = False
        if len(user['first_name']) == 0 or len(user['last_name']) == 0 or len(['email']) == 0 or len(user['password']) == 0:
            flash("All fields required", "register")
            is_valid = False
            return is_valid
        if not EMAIL_REGEX.match(user['email']):
            flash("Not a valid email address", "register")
            is_valid = False
        if not NAME_REGEX.match(user['first_name']):
            flash("First name must be at least 2 characters and contain only letters", "register")
            is_valid = False
        if not NAME_REGEX.match(user['last_name']):
            flash("Last name must be at least 2 characters and contain only letters", "register")
            is_valid = False
        if not PWD_REGEX.match(user['password']):
            flash("Password must contain at least 8 characters, 1 uppercase, 1 lowercase, a number, and a special character", "register")
            is_valid = False
        if user['password'] != user['confirm_pass']:
            flash("Passwords must be the same", "register")
            is_valid = False
        return is_valid