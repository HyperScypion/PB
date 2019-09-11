from flask import Flask, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.create_database import User, Base, Product, Car
from database.salt import Salt
import hashlib
import os


engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        salt = Salt(20).generate()
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password += salt
        h = hashlib.sha512(password.encode())
        result = str(h.hexdigest())
        session_db = Session(engine)
        user = User()
        user.password = result
        user.email = email
        user.username = username
        user.salt = salt
        session_db.add(user)
        session_db.commit()
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session_db = Session(engine)
        user = session_db.query(User).filter(User.email == email).one()
        if user.email is not None:
            password += user.salt
            h = hashlib.sha512(password.encode())
            result = str(h.hexdigest())
            if result == user.password:
                session['name'] = user.username
                session['email'] = user.email
                return render_template('home.html')
            else:
                return "Error password or email does not match"
        else:
            return "Error user not found"
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        return render_template('account.html')
    else:
        password = request.form['password']
        session_db = Session(engine)
        user = session_db.query(User).filter(User.username == session['name']).one()
        if user.username is not None:
            newpassword = request.form['newpassword']
            newpassword += user.salt
            print(newpassword)
            h = hashlib.sha512(newpassword.encode())
            result = str(h.hexdigest())
            # session_db.query(User).filter(User.username == session['name']).update({'oldPassword': User.password})
            session_db.query(User).filter(User.username == session['name']).update({'password': result})
            session_db.commit()
        else:
            return "Error user not found"
    return render_template('home.html')

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'GET':
        return render_template('shop.html')
    else:
        session_db = Session(engine)
        pattern = request.form['pattern']
        print(pattern)
        products = session_db.query(Product.productName).(pattern).all()
        print(products[0])
        # car_model = session_db.query(Car.carModel).filter(products.id == Car.id)
        # car_make = session_db.query(Car.carMake).filter(products.id == Car.id)
        # return render_template('results.html', products=products, car_make=car_make, car_model=car_model)



if __name__ == "__main__":
    app.secret_key = "AAA"
    app.run(debug=True, host='0.0.0.0', port=4000)
