from flask import Flask, render_template, redirect, request
from loginform import LoginForm
from registerform import RegisterForm
from button_delete import ButtonDelete
from marksform import MarksForm
from data import db_session
from data.users import User
from data.marks import Marks
from flask_login import LoginManager, login_required, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
username = ''
user = ''
mark = ''


def get_list_students():
    db_sess = db_session.create_session()
    list_1 = db_sess.query(User).filter(User.status == 'ученик').all()
    return list_1


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global username, user
    form = LoginForm()
    db_sess = db_session.create_session()
    user = User()
    user.email = form.username.data
    user.password = form.password.data
    user1 = db_sess.query(User).filter(User.email == form.username.data).first()
    if user.email and user.password:
        if user1 is None:
            return render_template('login.html', title='Электронный дневник', form=form,
                                   message='Пользователь не существует или удален')
        if user.email == user1.email and user.password != user1.password:
            return render_template('login.html', title='Электронный дневник', form=form,
                                   message='Неверный логин или пароль')
        if form.validate_on_submit():
            username = user1.surname + ' ' + user1.name
            user = user1
            return redirect('/marks')
    return render_template('login.html', title='Электронный дневник', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global username, user
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
        username = user.surname + ' ' + user.name
        return redirect('/marks')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/marks', methods=['GET', 'POST'])
def marks():
    global username, user, mark
    db_sess = db_session.create_session()
    mark = db_sess.query(Marks).filter(Marks.user_email == user.email).first()
    if user.status == 'учитель':
        return redirect('/marks_teacher')
    return render_template('marks.html', title='Оценки', username=username, marks=mark)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global user
    button = ButtonDelete()
    if request.method == 'POST':
        return redirect('/delete')
    return render_template('profile.html', title='Профиль', user=user, button=button)


@app.route('/delete', methods=['GET', 'POST', 'DELETE'])
def delete():
    global user
    logout_user()
    db_sess = db_session.create_session()
    a = db_sess.query(User).filter(User.id == user.id).first()
    db_sess.delete(a)
    db_sess.commit()
    return redirect('/login')


@app.route('/marks_teacher', methods=['GET', 'POST'])
def marks_teacher():
    global user, mark
    marksform = MarksForm()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        i = db_sess.query(Marks).filter((Marks.surname == marksform.student.data.split()[0]) and
                                             (Marks.name == marksform.student.data.split()[1])).first()
        if i:
            i.math = marksform.math.data
            i.russian = marksform.russian.data
            i.biology = marksform.biology.data
            i.chemistry = marksform.chemistry.data
            i.geografy = marksform.geografy.data
            i.history = marksform.history.data
            i.phisics = marksform.phisics.data
            i.english = marksform.english.data
            db_sess.commit()
        else:
            mark = Marks()
            mark.surname = marksform.student.data.split()[0]
            mark.name = marksform.student.data.split()[1]
            mark.math = marksform.math.data
            mark.russian = marksform.russian.data
            mark.biology = marksform.biology.data
            mark.chemistry = marksform.chemistry.data
            mark.geografy = marksform.geografy.data
            mark.history = marksform.history.data
            mark.phisics = marksform.phisics.data
            mark.english = marksform.english.data
            db_sess.add(mark)
            db_sess.commit()
    return render_template('teacher_account.html', title='Оценки', username=username, marks=mark,
                           users=db_sess.query(User).filter(User.status == 'ученик').all(), form=marksform)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')