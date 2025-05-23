from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user, login_user
from flask_restful import Api
from PIL import Image

from data.categories import Category
from data.db_session import global_init, create_session
from data.markets import Market
from data.users import User
from data import db_session
from data.API import users_api
from data.API import markets_api
from data.API import category_api
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


@app.route('/add_market/<user_id>', methods=['GET', 'POST'])
@login_required
def add_market(user_id):
    """
    Обработчик страницы, позволяющей добавить товар
    :return: html код страницы, позволяющей добавить товар
    """
    form = MarketForm()
    categories = ['Техника', 'Спорт', 'Природа', 'Отдых', 'Еда', 'Другое']
    if form.validate_on_submit():
        if not request.files['file']:
            return render_template('add_market.html', title='Добавление товара',
                                   form=form, img_error='Вы забыли добавить изображение!', categories=categories)
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
        chosen = request.form['education']
        db_sess = db_session.create_session()
        category_id = db_sess.query(Category).filter(Category.name == chosen).first().id
        market = Market(
            title=form.title.data,
            description=form.description.data,
            seller=user_id,
            price=form.price.data,
            contacts=form.contacts.data,
            address=form.address.data,
            img=f'/static/save_images/p{n}.png',
            stock=form.stock.data,
            category_id=category_id
        )
        db_sess.add(market)
        db_sess.commit()
        return redirect('/')

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    form.contacts.data = user.phone

    return render_template('add_market.html', title='Добавление товара',
                           form=form, img_error='', categories=categories)


@app.route("/edit_market/<market_id>", methods=['GET', 'POST'])
def edit_market(market_id):
    """
        Обработчик страницы, позволяющей изменять информацию о товаре
        :return: html код страницы, позволяющей изменять информацию о товаре
        """
    form = MarketForm()
    categories = ['Техника', 'Спорт', 'Природа', 'Отдых', 'Еда', 'Другое']
    if form.validate_on_submit():
        if request.files['file']:
            with open('./static/save_images/num.txt') as f:
                n = int(f.readline())
                n += 1
                with open('./static/save_images/num.txt', 'w') as file:
                    file.write(str(n))
            f = request.files['file']
            f.save(f'./static/save_images/p{n}.png')
        db_sess = db_session.create_session()
        chosen = request.form['education']
        category_id = db_sess.query(Category).filter(Category.name == chosen).first().id
        market = db_sess.query(Market).filter(Market.id == int(market_id)).first()

        market.title = form.title.data
        market.description = form.description.data
        market.price = form.price.data
        market.contacts = form.contacts.data
        market.address = form.address.data
        market.stock = form.stock.data
        market.category_id = category_id
        if request.files['file']:
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
    category_id = market.category_id
    print(category_id)

    return render_template('add_market.html', title='Редактирование товара', form=form,
                           categories=categories, category_id=category_id)


@app.route('/delete_market/<market_id>')
def delete_market(market_id):
    db_sess = db_session.create_session()
    market = db_sess.query(Market).filter(Market.id == market_id).first()
    if market:
        db_sess.delete(market)
        db_sess.commit()
        return redirect('/')
    else:
        return 404


@app.route('/market_ad/<id>')
def ad(id):
    """
    Позволяет перейти на нужное объявление.
    :param id: id объявления, int
    :return: страница объявления жи есть
    """
    db_sess = db_session.create_session()
    ad = db_sess.query(Market).filter(Market.id == id).first()
    format_category = str(ad.category)[14:]
    seller = db_sess.query(User).filter(User.id == ad.seller).first()
    format_regdate = seller.reg_date.strftime('%d-%m-%Y')
    print(seller.address)
    format_price = '{0:,}'.format(ad.price).replace(',', ' ')
    return render_template('ad.html', market=ad, price=format_price, cat=format_category, seller=seller, reg_date=format_regdate)


@app.route('/confirm/<market_id>')
def confirm(market_id):
    return render_template('confirmation.html', title='Уверен?', id=market_id)


@app.route('/index')
@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Домашняя страница
    :return: html код домашней страницы
    """
    categories = ['Все', 'Техника', 'Спорт', 'Природа', 'Отдых', 'Еда']
    if request.method == 'POST':
        chosen = request.form['education']
    else:
        chosen = "Все"
    db_sess = create_session()
    lst = []
    for market in db_sess.query(Market).all():
        if chosen == 'Все':
            lst.append(market)
        else:
            if market.category.name == chosen:
                lst.append(market)
    return render_template('home.html', title='Novito: все что вам нужно', list=lst, category=chosen,
                           categories=categories)


def main():
    """
    Главная функция. Инициализирует БД, позволяет работать с ней. Запускается работа сервера
    :return: Nothing
    """

    # Добавляет API для работы со списком пользователей
    api.add_resource(users_api.UsersListResource, '/api/users')

    # Добавляет API для работы с одним пользователем
    api.add_resource(users_api.UsersResource, '/api/users/<user_id>')

    # Добавляет API для работы со списком товаров
    api.add_resource(markets_api.MarketsListResource, '/api/markets')

    # Добавляет API для работы с одним товаром
    api.add_resource(markets_api.MarketsResource, '/api/markets/<market_id>')

    # Добавляет API для работы со списком категорий
    api.add_resource(category_api.CategorysListResource, '/api/category')

    # Добавляет API для работы с одной категорией
    api.add_resource(category_api.CategorysResource, '/api/category/<category_id>')

    db_session.global_init("db/novito.db")
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
