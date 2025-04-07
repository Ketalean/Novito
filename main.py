from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, logout_user, login_user
from flask_restful import Api

from data.db_session import global_init, create_session
from data.markets import Market
from data.users import User
from data import db_session
from forms.loginform import LoginForm
from forms.regform import RegisterForm

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
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
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
