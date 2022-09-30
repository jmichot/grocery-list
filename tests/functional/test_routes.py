from flask import Flask
import json
import pytest


from src import controller

class TestRoutes():

    def create_client(self):
        app = Flask(__name__, template_folder='../../templates')
        controller.configure_routes(app)
        client = app.test_client()
        return client

    def test_base_route(self):
        client = self.create_client()
        url = '/'
        response = client.get(url)
        assert response.status_code == 200
        