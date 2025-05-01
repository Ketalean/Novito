from flask import Flask
from data import db_session
from data.users import User
from data.markets import Market

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#  пайтон файл, создающий БД (novito.db). Следует запустить, если нет папки db или если в этой папке нет самой БД


def add_user(username, phone, address, password):
    """
    Функция добавляет пользователей в таблицу Users в БД novito.db
    :param username: <str> имя пользователя
    :param phone: <str> номер телефона
    :param address: <str> адрес
    :param password: <str> пароль
    :return: None
    """
    user = User()
    user.username = username
    user.phone = phone
    user.address = address
    user.set_password(password)
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_market(title, description, seller, price, stock, img, category):
    """
    Функция добавляет товары в таблицу Users в БД novito.db
    :param title: <str>
    :param description: <str>
    :param seller: <int>
    :param price: <int>
    :param stock: <bool>
    :param img: <str>
    :param category: <str>
    :return: None
    """
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
    market.category_id = category
    db_sess = db_session.create_session()
    db_sess.add(market)
    db_sess.commit()


def main():
    """
    Главная функция данного файла. Подключается к БД novito.db и заполняет её информацией, используя доп функции:
    add_user() и add_market()
    :return: None
    """
    db_session.global_init("db/novito.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        print(user)

    add_user("Oleg", "+7 (999) 135-99-90", "г. Челябинск", "Oleg_World!2021")
    add_user("Irina", "+7 (900) 756-34-34", "г. Челябинск, ул. Доватора, дом 13",
             "_25Irina52_")

    add_market("Немецкая противотанковая мина времён ВМв", "Очень хорошо работает", 1, 14088,
               True, "/static/images/mina.jpg,  /static/images/mina_2.jpg, /static/images/mina_3.png",
               1)

    add_market("Бита", "Ей можно бить", 2, 120,
               True, "/static/images/bita.png, /static/images/bita_2.jpg", 2)

    add_market("Мяч", "Отлично прыгает", 1, 4444,
               True, "/static/save_images/p1.png, /static/save_images/p3.png", 2)

    #  app.run()


if __name__ == '__main__':
    main()
