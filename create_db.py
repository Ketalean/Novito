from flask import Flask
from data import db_session
from data.users import User
from data.markets import Market

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_user(username, phone, address, password):
    user = User()
    user.username = username
    user.phone = phone
    user.address = address
    user.set_password(password)
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_market(title, description, seller, price, stock, img, category):
    market = Market()
    market.title = title
    market.description = description
    market.seller = seller
    market.price = price
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == seller).first()
    market.contacts = user.phone
    market.address = user.address
    market.stock = stock
    market.img = img
    market.category = category
    db_sess = db_session.create_session()
    db_sess.add(market)
    db_sess.commit()


def main():
    db_session.global_init("db/novito.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)

    add_user("Oleg", "+7 (999) 135-99-90", "г. Челябинск", "Oleg_World!2021")
    add_user("Irina", "+7 (900) 756-34-34", "г. Челябинск, ул. Доватора, дом 13",
             "_25Irina52_")

    add_market("Немецкая противотанковая мина времён ВМв", "Очень хорошо работает", 1, 14088,
               True, "/static/images/mina.jpg,  /static/images/mina_2.jpg, /static/images/mina_3.png",
               "Бытовая техника")

    add_market("Бита", "Ей можно бить", 2, 120,
               True, "/static/images/bita.png, /static/images/bita_2.jpg", "Спорт")

    #  app.run()


if __name__ == '__main__':
    main()
