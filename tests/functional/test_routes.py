from flask import Flask
import json


from src import controller

def test_base_route():
    app = Flask(__name__)
    client = app.test_client()
    url = '/'
    response = client.get(url)
    print(response)
    