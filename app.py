#!/usr/bin/env python

from flask import (Flask, render_template, redirect, flash, url_for, g
                   )
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)


import forms
import models


DEBUG = True
PORT = '8000'
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'uyrury653gsf..631fff!@hhhmnv&%*%ahabcgnotk.8'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.username = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            username = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your username or password is incorrect", "error")
        else:
            if models.User.validate_password(username, form.password.data):
                login_user(username)
                flash("You have successfully logged in.", "success")
                return redirect(url_for('index'))
            else:
                flash("Your username or password is incorrect", "error")
    return render_template('login.html', form=form)

#Homepage, acts as the Listing route
@app.route('/')
def index():
    return redirect(url_for('entries'))


#Will act as the Listing route just like /
@app.route('/entries')
def entries():
    return render_template('index.html')


@app.route('/register', methods=('GET','POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You have successfully registered.", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


#The Create route
@app.route('/entries/new', methods=('GET','POST')   )
@login_required
def new_entry():
    form = forms.NewEntry()
    if form.validate_on_submit():
        models.Entry.create(username=g.username._get_current_object(),
                            title=form.title.data.strip(),
                            date=form.date.data,
                            time_spent=form.time_spent.data.strip(),
                            what_i_learned=form.what_i_learned.data.strip(),
                            resources_to_remember=form.resources_to_remember.data.strip()
                            )
        flash("Entry has been successfully posted.", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)
"""
#The Detail Route
@app.route('/entries/<id>')
@login_required
def detail_entry(id):
    return render_template('detail.html')

#The Edit or Update route
@app.route('/entries/<id>/edit')
@login_required
def edit_entry(id):
    return render_template('edit.html')

#The Delete route
@app.route('/entries/<id>/delete', methods=('POST',))
@login_required
def delete_entry(id):
    flash("Entry has been successfully deleted.", "success")
    return redirect(url_for('index'))
"""

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    """
    try:
        models.User.create_user(
            username='lisa',
            email='lisa@lisa.com',
            password='password1234'
            admin=True
        )
    except ValueError:
        pass
    """
    app.run(debug=DEBUG, host=HOST, port=PORT)