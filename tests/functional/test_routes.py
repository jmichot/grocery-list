import json

import pytest
from flask import Flask

import init_db
from src import controller
from app import app
from src.dao import Dao
from src.model.product import Product
from src.constants import *

PARAM_ONE = b'[{"id":1,"name":"TestName","quantity":3}]\n'
PARAM_TWO = b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":3}]\n'
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

    def get_all_product_request(self, res):
        get_all = self.client.get('/product')
        assert get_all.status_code == 200
        assert get_all.data == res
        return get_all

    def put_request(self, url, data, code):
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == code
        return response

    # =====================================================#

    def test_base_route(self):
        url = '/'
        response = self.client.get(url)
        self.client.delete()
        assert response.status_code == 200

    # =====================================================#

    def test_modify_quantity_success(self):
        url = '/product/1'
        data = {'name': 'NewName', 'quantity': 8}
        code = 200
        self.put_request(url, data, code)
        self.get_all_product_request(b'[{"id":1,"name":"NewName","quantity":8}]\n')

    # =====================================================#

    def test_modify_failure_id_not_integer(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product/NotId'
        data = {'name': 'TestName', 'quantity': 8}
        response = self.put_request(url, data, 400)
        assert str(response.text) == ID_NOT_INT
        self.get_all_product_request(PARAM_ONE)

    def test_modify_failure_id_not_exist(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product/125656'
        data = {'name': 'TestName', 'quantity': 8}
        response = self.put_request(url, data, 404)
        assert str(response.text) == PRODUCT_NOT_FOUND
        self.get_all_product_request(PARAM_ONE)

    # =====================================================#

    def test_modify_failure_quantity(self):
        url = '/product/1'
        data = {'name': 'TestName', 'quantity': 0}
        response = self.put_request(url, data, 400)
        assert str(response.text) == QUANTITY_LOWER_THAN_ONE
        self.get_all_product_request(PARAM_ONE)

    def test_modify_failure_quantity_negative(self):
        url = '/product/1'
        data = {'name': 'TestName', 'quantity': -50}
        response = self.put_request(url, data, 400)
        assert str(response.text) == QUANTITY_LOWER_THAN_ONE
        self.get_all_product_request(PARAM_ONE)

    def test_modify_failure_quantity_null(self):
        url = '/product/1'
        data = {'name': 'TestName'}
        response = self.put_request(url, data, 400)
        assert str(response.text) == MISSING_ARGUMENTS
        self.get_all_product_request(PARAM_ONE)

    # =====================================================#

    def test_delete_failure_id_not_integer(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product/NotId'
        response = self.client.delete(url)
        assert response.status_code == 400
        assert str(response.text) == ID_NOT_INT
        self.get_all_product_request(PARAM_ONE)

    def test_delete_failure_id_not_exist(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product/125656'
        response = self.client.delete(url)
        assert response.status_code == 404
        assert str(response.text) == PRODUCT_NOT_FOUND
        self.get_all_product_request(PARAM_ONE)

    # =====================================================#

    def test_delete_success(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product/1'
        response = self.client.delete(url)
        assert response.status_code == 200
        self.get_all_product_request(b'[]\n')

    # =====================================================#

    def test_modify_if_conflict(self):
        dao = Dao(test=True)
        dao.add_product(Product(None, 3, "Test"))
        self.get_all_product_request(PARAM_TWO)
        url = '/product/1'
        data = {'name': 'Test', 'quantity': 8}
        response = self.put_request(url, data, 409)
        assert str(response.text) == NAME_CONFLICT
        self.get_all_product_request(PARAM_TWO)

    # =====================================================#

    def test_add_ok(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product'
        data = {'name': 'Test', 'quantity': 8}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        self.get_all_product_request(b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":8}]\n')

    # =====================================================#

    def test_add_if_conflict(self):
        self.get_all_product_request(PARAM_ONE)
        url = '/product'
        data = {'name': 'TestName', 'quantity': 8}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 409
        assert str(response.text) == NAME_CONFLICT
        self.get_all_product_request(PARAM_ONE)

    # =====================================================#

    def test_get_all(self):
        self.get_all_product_request(PARAM_ONE)

    # =====================================================#

    def test_wrong_url(self):
        response = self.client.get('/bad/url')
        assert response.status_code == 404

    # =====================================================#
