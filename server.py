from flask import Flask, g, request, url_for, redirect, render_template

import forms
import models


#####################
# Server Settings
#####################

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)

app.secret_key = 'iuh23ehciubwrfiuwegyhiwbefdewicdhuib'


@app.before_request
def before_request():
    """Connect to database before request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close he database connection after request"""
    g.db.close()
    return response


#####################
# Routes
#####################


@app.route('/register', methods=['GET', 'POST'])
def registration():
    """GET and POST route for our register page to create a User"""
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        models.User.create_user(username=form.username.data,
                                email=form.email.data,
                                password=form.password.data)
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(username=form.username.data)
        except:
            pass
        else:
            if user.check_password_against_hash(form.password.data):
                # login the user
                return redirect(url_for('login'))
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
