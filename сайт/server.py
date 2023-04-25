from flask import Flask, render_template, redirect
from loginform import LoginForm
from registerform import RegisterForm
from data import db_session
from data.users import User
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_sess = db_session.create_session()
    user = User()
    user.email = form.username.data
    user.password = form.password.data
    user1 = db_sess.query(User).filter(User.email == form.username.data).first()
    if user.email and user.password:
        if user.email == user1.email and user.password != user1.password:
            return render_template('login.html', title='Электронный дневник', form=form,
                                   message='Неверный логин или пароль')
        if form.validate_on_submit():
            return redirect('/marks')
    return render_template('login.html', title='Электронный дневник', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.father = form.father.data
        user.email = form.email.data
        user.password = form.password.data
        user.schoolclass = form.schoolclass.data
        user.status = form.status.data
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/marks')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    return render_template('base.html', title='Оценки')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')