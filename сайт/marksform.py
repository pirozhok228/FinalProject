from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class MarksForm(FlaskForm):
    math = StringField(validators=[DataRequired()])
    russian = StringField(validators=[DataRequired()])
    phisics = StringField(validators=[DataRequired()])
    chemistry = StringField(validators=[DataRequired()])
    biology = StringField(validators=[DataRequired()])
    history = StringField(validators=[DataRequired()])
    geografy = StringField(validators=[DataRequired()])
    english = StringField(validators=[DataRequired()])
    student = StringField('Введите фамилию и имя ученика')
    submit = SubmitField('Добавить оценки')
