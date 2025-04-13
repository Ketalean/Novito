from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user, login_user
from flask_restful import Api
from PIL import Image

from data.db_session import global_init, create_session
from data.markets import Market
from data.users import User
from data import db_session
from forms.loginform import LoginForm
from forms.regform import RegisterForm
from forms.market_form import MarketForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)

global_init(f'db/novito.db')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Набросок обработчика регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.second_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            phone=form.phone.data,
            address=form.address.data,

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обработчик авторизации
    рабочий
    """
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    """
    Позволяет получить информацию о пользователе.
    :param user_id: id пользователя, int
    :return: объект, у которого можно получить информацию о пользователе с user_id
    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    """
    Выход из аккаунта
    :return: перекидывает на главную страницу
    """
    logout_user()
    return redirect("/")


@app.route('/add_market', methods=['GET', 'POST'])
@login_required
def add_market():
    form = MarketForm()
    if form.validate_on_submit():
        with open('./static/save_images/num.txt') as f:
            n = int(f.readline())
            n += 1
            with open('./static/save_images/num.txt', 'w') as file:
                file.write(str(n))
            f = request.files['file']
            f.save(f'./static/save_images/p{n}.png')
            im = Image.open(f'./static/save_images/p{n}.png')
            im = im.resize((400, 200))
            im.save(f'./static/save_images/p{n}.png')
        db_sess = db_session.create_session()
        market = Market(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            contacts=form.contacts.data,
            address=form.address.data,
            img=f'/static/save_images/p{n}.png',
            category=form.category.data
        )
        db_sess.add(market)
        db_sess.commit()
        return redirect('/')
    return render_template('add_market.html', title='Добавление товара', form=form)


@app.route("/edit_market/<market_id>", methods=['GET', 'POST'])
def edit_market(market_id):
    form = MarketForm()
    if form.validate_on_submit():
        if request.files['file'] is not None:
            with open('./static/save_images/num.txt') as f:
                n = int(f.readline())
                n += 1
                with open('./static/save_images/num.txt', 'w') as file:
                    file.write(str(n))
            f = request.files['file']
            f.save(f'./static/save_images/p{n}.png')
        db_sess = db_session.create_session()
        market = db_sess.query(Market).filter(Market.id == int(market_id)).first()

        market.title = form.title.data
        market.description = form.description.data
        market.price = form.price.data
        market.contacts = form.contacts.data
        market.address = form.address.data
        market.stock = form.stock.data
        market.category = form.category.data
        if request.files['file'] is not None:
            market.img = market.img + f', /static/save_images/p{n}.png'

        db_sess.commit()
        return redirect('/')

    db_sess = db_session.create_session()
    market = db_sess.query(Market).filter(Market.id == int(market_id)).first()

    form.title.data = market.title
    form.description.data = market.description
    form.price.data = market.price
    form.contacts.data = market.contacts
    form.address.data = market.address
    form.stock.data = market.stock
    form.category.data = market.category

    return render_template('add_market.html', title='Редактирование товара', form=form)


@app.route('/index')
@app.route('/')
def index():
    """
    Домашняя страница
    :return: html код домашней страницы
    """
    db_sess = create_session()
    lst = []
    for market in db_sess.query(Market).all():
        lst.append(market)
    return render_template('home.html', title='Милый дом', list=lst)


def main():
    """
    Главная функция. Инициализирует БД, позволяет работать с ней. Запускается работа сервера
    :return: Nothing
    """
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
