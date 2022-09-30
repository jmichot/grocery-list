import init_db
from flask import Flask
from src.controller import configure_routes

app = Flask(__name__)

configure_routes(app)

if __name__ == '__main__':
    init_db
    app.run()