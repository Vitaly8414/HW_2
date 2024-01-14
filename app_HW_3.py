from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash

from form import RegistrationForm

import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-key'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
                       (first_name, last_name, email, password))
        connection.commit()
        connection.close()

        return redirect(url_for('success'))
    return render_template('register.html', form=form)

@app.route('/success')
def success():
    return 'Пользователь успешно зарегистрирован!'

def create_db():
    if not os.path.exists('users.db'):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE users (
                               id INTEGER PRIMARY KEY,
                               first_name TEXT,
                               last_name TEXT,
                               email TEXT UNIQUE,
                               password TEXT)''')
        connection.commit()
        connection.close()


if __name__ == '__main__':
    create_db()
    app.run(debug=True)