import sys
from flask import Flask
from src.controller import configure_routes

if __name__ == '__main__':
    args = sys.argv
    app = Flask(__name__)
    try: 
        if (args[1] == "test"):
            configure_routes(app, True)
    except IndexError:
        configure_routes(app)
    app.run()