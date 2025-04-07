from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, EmailField
from wtforms.validators import DataRequired, ValidationError, Length


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    second_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    phone = StringField('Номер телефона',
                        validators=[DataRequired(), Length(min=6, max=12)])
    address = StringField('Адрес', validators=[DataRequired()])
    # email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Отправить')

