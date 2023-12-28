from flask import Flask, flash, redirect, render_template, request, url_for, make_response, session

app = Flask(__name__)
app.secret_key = b'ef3b106b57b769bafe5f64a1ddb8f2735f34f50e53539790354498394ea8e888'


@app.route('/titul/')
def index1():
    context = {
        'title': 'Главная',
        'name': 'Покупатель'
    }
    response = make_response(render_template('main.html', **context))
    response.headers['new_head'] = 'New-value'
    response.set_cookie('username', context['name'])
    return response

@app.route('/getcookie/')
def get_cookies():
    name = request.cookies.get('username')
    return f"Значение cookie: {name}"

@app.route('/basic/')
def index():
    if 'username' in session:
        return f'Привет, {session["username"]}'
    else:
        return redirect(url_for('login'))
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        return redirect(url_for('index'))
    return render_template('username_form.html')

@app.route('/logout/')
def loguot():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
def temps():
    return render_template('temps.html')

@app.route('/greet', methods=['POST'])
def greet():
    username = request.form['username']
    return render_template('greet.html', username=username)

@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя и email', 'danger')
            return redirect(url_for('form'))
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))
    return render_template('flash_form.html')

@app.route('/main/')
def main():
    content = {'title': 'Главная'}
    return render_template('main.html', **content)

@app.route('/data/')
def data():
    content = {'title': 'Обувь'}
    return render_template('data.html', **content)

@app.route('/jacket/')
def jacket():
    content = {'title': 'Куртка'}
    return render_template('jacket.html', **content)

if __name__ == '__main__':
    app.run(debug=True)