import init_db
from flask import Flask

app = Flask(__name__)

import src.controller

if __name__ == '__main__':
    init_db
    app.run()