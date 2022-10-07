from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model
db = 'obake_sushi'

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.fish = data['fish']
        self.rice = data['rice']
        self.wasabi = data['wasabi']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders LEFT JOIN users on shows.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        orders = []
        for row in results:
            order = cls(row)
            user_data = {
                'id': row['user.id'],
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
            orders.append(order)
        return orders
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders (fish, rice, wasabi, price, quantity, user_id) \
        VALUES ( %(fish)s, %(rice)s, %(wasabi)s, %(price)s, %(quantity)s, %(user_id)s );"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_order(cls, id):
        query = f"SELECT * FROM orders LEFT JOIN orders on orders.user_id = users.id WHERE \
        orders.id = {id};"
        results = connectToMySQL(db).query_db(query)
        order = cls(results[0])
        for row in results:
            order = cls(row)
            user_data = {
                'id': row['user.id'],
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
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_order(order):
        is_valid = True
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, order)
        if len(order['method']) == 0 or len(order['fish']) == 0 or len(order['rice']) == 0 or \
        len(order['wasabi']) == 0 or len(order['quantity']) == 0:
            flash("All fields required", "order")
            is_valid = False
        return is_valid