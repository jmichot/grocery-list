import json

import pytest
from flask import Flask

import init_db
from src import controller
from app import app
from src.dao import Dao
from src.model.product import Product
from src.constants import *


class TestRoutes:

    @pytest.fixture(autouse=True)
    def run_before_and_after_tests(self):
        init_db.reset_db(True)
        app = Flask(__name__, template_folder='../../templates')
        app.config.update({
            "TESTING": True,
        })
        controller.configure_routes(app, True)
        client = app.test_client()
        dao = Dao(test=True)
        dao.add_product(Product(None, 3, "TestName"))
        self.client = client

    # =====================================================#

    def test_base_route(self):
        url = '/'
        response = self.client.get(url)
        self.client.delete()
        assert response.status_code == 200

    # =====================================================#

    def test_modify_quantity_success(self):
        url = '/product/1'
        dict = {'name': 'NewName', 'quantity': 8}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 200

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"NewName","quantity":8}]\n'

    # =====================================================#

    def test_modify_failure_id_not_integer(self):

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product/NotId'
        dict = {'name': 'TestName', 'quantity': 8}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 400
        assert str(response.text) == ID_NOT_INT

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    def test_modify_failure_id_not_exist(self):

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product/125656'
        dict = {'name': 'TestName', 'quantity': 8}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 404
        assert str(response.text) == PRODUCT_NOT_FOUND

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_modify_failure_quantity(self):

        url = '/product/1'
        dict = {'name': 'TestName', 'quantity': 0}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 400
        assert str(response.text) == QUANTITY_LOWER_THAN_ONE

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    def test_modify_failure_quantity_negative(self):
        url = '/product/1'
        dict = {'name': 'TestName', 'quantity': -50}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 400
        assert str(response.text) == QUANTITY_LOWER_THAN_ONE

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    def test_modify_failure_quantity_null(self):
        url = '/product/1'
        dict = {'name': 'TestName'}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 400
        assert str(response.text) == MISSING_ARGUMENTS

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_delete_failure_id_not_integer(self):
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product/NotId'
        response = self.client.delete(url)
        assert response.status_code == 400
        assert str(response.text) == ID_NOT_INT

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    def test_delete_failure_id_not_exist(self):
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product/125656'
        response = self.client.delete(url)
        assert response.status_code == 404
        assert str(response.text) == PRODUCT_NOT_FOUND

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_delete_success(self):

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product/1'
        response = self.client.delete(url)
        assert response.status_code == 200

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[]\n'

    # =====================================================#

    def test_modify_if_conflict(self):
        dao = Dao(test=True)
        dao.add_product(Product(None, 3, "Test"))
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":3}]\n'

        url = '/product/1'
        dict = {'name': 'Test', 'quantity': 8}
        response = self.client.put(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 409
        assert str(response.text) == NAME_CONFLICT

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":3}]\n'

    # =====================================================#

    def test_add_ok(self):
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product'
        dict = {'name': 'Test', 'quantity': 8}
        response = self.client.post(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 200

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":8}]\n'

    # =====================================================#

    def test_add_if_conflict(self):
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/product'
        dict = {'name': 'TestName', 'quantity': 8}
        response = self.client.post(url, data=json.dumps(dict), content_type='application/json')
        assert response.status_code == 409
        assert str(response.text) == NAME_CONFLICT

        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_get_all(self):
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_default_url(self):
        with app.app_context():
            response = self.client.get('/')
            ### assert with render template index.html

    # =====================================================#

    def test_wrong_url(self):
        response = self.client.get('/bad/url')
        assert response.status_code == 404

    # =====================================================#
