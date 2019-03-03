import os

from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from flask_wtf.csrf import CSRFError, CsrfProtect, urlparse
from wtforms import (BooleanField, PasswordField, TextAreaField, TextField,
                     validators)

from hotel.forms.account import LoginForm, RegisterForm


app = Flask(__name__)
app.config.from_object('config.Develop')
db = SQLAlchemy(app)

csrf = CsrfProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return user.get_user(username)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/accomodation')
def accomodation():
    return render_template('accomodation.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/blog/details')
def blog_details():
    return render_template('blog-details.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        usr = user.get_user(username=form.username.data)
        if usr is None or not user.check_password2(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(usr, remember=form.remember.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(home())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = account.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user.save_user(username=form.username.data,
                       password=form.password.data)
        return login()
    else:
        return render_template('register.html', title='Register', form=form)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.descriptionc
                           ), 400


if __name__ == "__main__":
    app.run()
