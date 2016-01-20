"""Flask server boilerplate code"""

from flask import Flask, g

import models

# server settings
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
    
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)