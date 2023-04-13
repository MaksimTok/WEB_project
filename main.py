from flask import Flask, render_template, make_response, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, EmailField, TextAreaField, TelField
from wtforms.validators import DataRequired
from data import db_session
from data.admin import Admin
from data.master import Master
from data.process import Process
from data.record import Record
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    login = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Название организации', validators=[DataRequired()])
    login = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    phone_number = TelField('Номер телефона организации', validators=[DataRequired()])
    info = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(Admin, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Admin).filter(Admin.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Admin).filter(Admin.login == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        
        user = Admin(
            name=form.name.data,
            login=form.login.data,
            info=form.info.data,
            number=form.phone_number.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def timeline():  # Вкладка на которой можно поменять основные данные
    pass


@app.route("/profile/timeline")
def timeline():  # Заготовка для таймлайна
    pass


@app.route("/profile/masters")
def masters():  # Заготовка для вкладки мастеров
    pass


@app.route("/profile/process")
def process():   # Заготовка для вкладки услуг
    pass


def main():
    db_session.global_init("db/base.db")
    app.run()


if __name__ == '__main__':
    main()