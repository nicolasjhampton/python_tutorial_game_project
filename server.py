from flask import Flask, g, request

import forms
import models


#####################
# Server Settings
#####################

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)


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


# @app.route('/register', methods=['GET'])
# def register():
#     """GET route for our register page"""
#     return "Registration Page"


@app.route('/register', methods=['GET', 'POST'])
def post_registration():
    """POST route for our register page to create a User"""
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        # **userinfo would work, but we have to get rid of password2 first
        models.User.create_user(username=form.username.data,
                                email=form.email.data,
                                password=form.password.data)
        return "{} Registered!".format(models.User.get(email=form.email.data))
    return "Registration Page"


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
