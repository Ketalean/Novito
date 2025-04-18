from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
#  класс, который является flask-формой для регистрации пользователя


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    second_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    phone = StringField('Номер телефона',
                        validators=[DataRequired(), Length(min=6, max=12)])
    address = StringField('Адрес', validators=[DataRequired()])
    # email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Отправить')

