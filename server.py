"""Flask server boilerplate code"""

from flask import Flask

# server settings
DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
    
@app.route('/register')
def register():
    return "Registration Page"
    
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)