from flask import Flask, render_template, redirect
from loginform import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/login')
    return render_template('login.html', title='Электронный дневник', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')