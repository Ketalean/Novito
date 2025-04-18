from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired
#  класс, который является flask-формой для заполнения информации о товаре


class MarketForm(FlaskForm):
    title = StringField('Наименование товара', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    contacts = StringField('Номер телефона',
                           validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    stock = BooleanField('Есть в наличии')
    img = FileField('Изображение')
    category = StringField('Категория', validators=[DataRequired()])
    submit = SubmitField('Отправить')
