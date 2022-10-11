from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
db = 'obake_sushi'

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.fish = data['fish']
        self.rice = data['rice']
        self.wasabi = data['wasabi']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders LEFT JOIN users on orders.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        orders = []
        for row in results:
            order = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'address': row['address'],
                'city': row['city'],
                'state': row['state'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            order.user = user_model.User(user_data)
        return orders

    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders (method, fish, rice, wasabi, quantity, user_id) VALUES ( %(method)s, \
        %(fish)s, %(rice)s, %(wasabi)s, %(quantity)s, %(user_id)s );"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_order(cls, id):
        query = f"SELECT * FROM orders LEFT JOIN users on orders.user_id = users.id WHERE orders.id = {id};"
        results = connectToMySQL(db).query_db(query)
        order = cls(results[0])
        for row in results:
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'address': row['address'],
                'city': row['city'],
                'state': row['state'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            order.user = user_model.User(user_data)
        return order

    @staticmethod
    def validate_order(order):
        is_valid = True
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, order)
        if len(order['fish']) == 0:
            flash("Please choose a fish", "order")
            is_valid = False
        return is_valid
