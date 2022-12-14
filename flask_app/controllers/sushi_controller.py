from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models import user_model, order_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register')
def register_user():
    return render_template('index.html')

@app.route('/register_user', methods=['POST'])
def register():
    if not user_model.User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = user_model.User.save(data)
    return redirect('/home')

@app.route('/login')
def login_user():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login():
    user = user_model.User.check_email(request.form['email'])
    if user == False:
        flash("Please enter a valid email address and password", "login")
        return redirect('/login')
    if bcrypt.check_password_hash(user.password, request.form['password']) == False:
        flash("Password is incorrect, please try again", "login")
        return redirect('/login')
    else:
        if bcrypt.check_password_hash(user.password, request.form['password']) == True:
            session['user_id'] = user.id
            return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = user_model.User.get_one_user(data)
    return render_template('home.html', user = user)

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = user_model.User.get_one_user(data)
    return render_template('account.html', user = user)

@app.route('/edit_account', methods=['POST'])
def edit_account():
    if not user_model.User.validate_user_update(request.form):
        return redirect(request.referrer)
    print(request.form)
    user_model.User.update_user(request.form)
    return redirect('/account')

@app.route('/order')
def order():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('order.html')

@app.route('/new_order', methods=['POST'])
def new_order():
    if not order_model.Order.validate_order(request.form):
        return redirect('/order')
    print(request.form.getlist("fish"))
    # order_model.Order.save(request.form)
    order_model.Order.process_order(request.form)
    return redirect('/checkout')

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('checkout.html', orders = order_model.Order.checkout(session['user_id']))

@app.route('/delete')
def delete():
    data = {
        'id': session['user_id']
    }
    order_model.Order.delete(data)
    return redirect('/order')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')