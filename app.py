"""
Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), 
дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц (итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
* Чтение всех
* Чтение одного
* Запись
* Изменение
* Удаление
"""

from flask import Flask, request, jsonify
from pydantic import BaseModel
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class ProductModel(BaseModel):
    name: str
    description: str
    price: float

class OrderModel(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str

class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

# CRUD operations for Products
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price} for p in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price})
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = ProductModel(**data)
    new_product = Product(**product.dict())
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    data = request.get_json()
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

# CRUD operations for Orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'user_id': o.user_id, 'product_id': o.product_id, 'order_date': o.order_date, 'status': o.status} for o in orders])

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify({'id': order.id, 'user_id': order.user_id, 'product_id': order.product_id, 'order_date': order.order_date, 'status': order.status})
    else:
        return jsonify({'message': 'Order not found'}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = OrderModel(**data)
    new_order = Order(**order.dict())
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    data = request.get_json()
    order.user_id = data['user_id']
    order.product_id = data['product_id']
    order.order_date = data['order_date']
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

# CRUD operations for Users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserModel(**data)
    new_user = User(**user.dict())
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)