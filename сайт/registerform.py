from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    father = StringField('Отчество', validators=[DataRequired()])
    schoolclass = StringField('Класс', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    status = SelectField('Выберете тип аккаунта', choices=['ученик', 'учитель'])