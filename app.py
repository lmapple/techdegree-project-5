#!/usr/bin/env python

import datetime
import forms
import models

from flask import (Flask, render_template, redirect, flash, url_for,
                   g, abort
                   )
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user
                         )


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


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            username = models.User.get(models.User.username
                                       == form.username.data
                                       )
        except models.DoesNotExist:
            flash("Your username or password is incorrect", "error")
        else:
            if models.User.validate_password(username,
                                             form.password.data
                                             ):
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
    user_entries = models.Entry.select().limit(20)
    #https://peewee.readthedocs.io/en/latest/peewee/playhouse.html?highlight=pagination#PaginatedQuery
    return render_template('index.html', user_entries=user_entries)


@app.route('/entries/tag/<tag_name>')
@login_required
def tagged_entries(tag_name):
    user_entries = models.Tag.get(models.Tag.tag_name == tag_name)\
        .get_tagged_entries().limit(20)
    return render_template('index.html', user_entries=user_entries)


#The Detail Route
@app.route('/entries/<id>')
@login_required
def detail_entry(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('detail.html', entry=entry)


#The Create Route
@app.route('/entries/new', methods=('GET','POST'))
@login_required
def new_entry():
    form = forms.NewEntry()
    if form.validate_on_submit():
        models.Entry.create_entry(
            username=g.username._get_current_object(),
            title=form.title.data.strip(),
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_i_learned=form.what_i_learned.data.strip(),
            resources_to_remember=form.resources_to_remember.data.strip(),
        )
        tag_list = form.tags.data.replace(","," ").split()
        for tag in tag_list:
            if models.DoesNotExist():
                try:
                    models.Tag.create_tag(tag)
                except models.IntegrityError:
                    pass
            models.TagEntry_Relationship.create_relationship(
                tag=tag,
                entry=form.title.data.strip()
            )
        flash("Entry has been successfully posted.", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


#The Edit or Update Route
@app.route('/entries/<id>/edit', methods=('GET','POST'))
@login_required
def edit_entry(id):
    entry = models.Entry.get(models.Entry.id == id)
    tags = entry.get_tag_names()
    tag_list = []
    for tag in tags:
        tag_list.append(tag.tag_name)
    tag_string = ", ".join(tag_list)

    form = forms.EditEntry(title=entry.title,date=entry.date,
                           time_spent=entry.time_spent,
                           what_i_learned=entry.what_i_learned,
                           resources_to_remember=entry.resources_to_remember,
                           tags=tag_string
                           )

    if form.validate_on_submit():
        tag_list_new = form.tags.data.replace(",", " ").split()

        #Delete tags that have been removed
        for tag in tag_list:
            if tag in tag_list_new:
                pass
            else:
                tag_old = models.Tag.get(models.Tag.tag_name == tag)
                relationship = models.TagEntry_Relationship.get(
                    tagged_entries=models.Entry.
                        get(models.Entry.id == entry.id),
                    entry_tags=models.Tag.
                        get(models.Tag.id == tag_old.id)
                )
                if len(tag_old.get_tagged_entries()) == 1:
                    tag_old.delete_instance()
                relationship.delete_instance()

        #Create tags and tag-entry relationships if they do not exist
        for tag in tag_list_new:
            if tag not in tag_list:
                if models.DoesNotExist():
                    try:
                        models.Tag.create_tag(tag)
                    except models.IntegrityError:
                        pass
                    models.TagEntry_Relationship.create_relationship(
                        tag=tag,
                        entry=form.title.data.strip()
                    )

        entry.username = g.username._get_current_object()
        entry.title = form.title.data.strip()
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.what_i_learned = form.what_i_learned.data.strip()
        entry.resources_to_remember = form.resources_to_remember.data.strip()
        entry.tags = form.tags.data.strip()
        entry.last_updated = datetime.datetime.now()
        entry.save()
        flash("Entry has been successfully updated.", "success")
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry, form=form)


#The Delete Route
@app.route('/entries/<id>/delete', methods=('GET','POST'))
@login_required
def delete_entry(id):
    entry = models.Entry.get(models.Entry.id == id)
    relationships = models.TagEntry_Relationship.select().where(
        models.TagEntry_Relationship.tagged_entries_id == entry.id)
    for tag in entry.get_tag_names():
        if len(tag.get_tagged_entries()) == 1:
            tag.delete_instance()
    for relationship in relationships:
        relationship.delete_instance()
    entry.delete_instance()
    flash("Entry has been successfully deleted.", "success")
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('index'))



if __name__ == '__main__':

    models.initialize()

    app.run(debug=DEBUG, host=HOST, port=PORT)