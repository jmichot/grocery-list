from flask import Flask
import init_db

from src import controller
from app import app
from src.dao import Dao
from src.model.product import Product


class TestRoutes:
    def create_client(self):
        init_db.reset_db(True)
        app = Flask(__name__, template_folder='../../templates')
        app.config.update({
            "TESTING": True,
        })
        controller.configure_routes(app, True)
        client = app.test_client()
        dao = Dao(test=True)
        dao.addProduct(Product(None, 3, "TestName"))
        return client

    # =====================================================#

    def test_base_route(self):
        client = self.create_client()
        url = '/'
        response = client.get(url)
        client.delete()
        assert response.status_code == 200

    # =====================================================#

    def test_add_one_if_exist(self):
        client = self.create_client()

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/addOne?id=1'
        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":4}]\n'

    # =====================================================#

    def test_add_one_if_not_exist(self):
        client = self.create_client()

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/addOne?id=NotId'
        response = client.post(url)
        assert response.status_code == 400

        url = '/addOne?id=123541'
        response = client.post(url)
        assert response.status_code == 404

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_remove_one_ok(self):
        client = self.create_client()

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/removeOne?id=1'
        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":2}]\n'

        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":1}]\n'

        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[]\n'

    # =====================================================#

    def test_remove_one_not_exist(self):
        client = self.create_client()
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/removeOne?id=NotId'
        response = client.post(url)
        assert response.status_code == 400

        url = '/removeOne?id=132412412'
        response = client.post(url)
        assert response.status_code == 404

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_delete_all_ok(self):
        client = self.create_client()

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/deleteAll?id=1'
        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[]\n'

    # =====================================================#

    def test_delete_all_if_not_exist(self):
        client = self.create_client()
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/deleteAll?id=NotId'
        response = client.post(url)
        assert response.status_code == 400

        url = '/deleteAll?id=12415242'
        response = client.post(url)
        assert response.status_code == 404

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_modify_ok(self):
        client = self.create_client()
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/modify?id=1&quantity=20&name=Test'
        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"Test","quantity":20}]\n'

    def test_modify_if_not_exist(self):
        client = self.create_client()

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/modify?id=5&quantity=20&name=Test'
        response = client.post(url)
        assert response.status_code == 404

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_modify_if_conflict(self):
        client = self.create_client()
        dao = Dao(test=True)
        dao.addProduct(Product(None, 3, "Test"))
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":3}]\n'

        url = '/modify?id=1&quantity=20&name=Test'
        response = client.post(url)
        assert response.status_code == 404

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"Test","quantity":3}]\n'

    # =====================================================#

    def test_add_ok(self):
        client = self.create_client()
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/add?quantity=20&name=MyNewProductTest'
        response = client.post(url)
        assert response.status_code == 200

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3},{"id":2,"name":"MyNewProductTest","quantity":20}]\n'

    # =====================================================#

    def test_add_if_conflict(self):
        client = self.create_client()
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

        url = '/add?quantity=20&name=TestName'
        response = client.post(url)
        assert response.status_code == 409

        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_get_all(self):
        client = self.create_client()
        get_all = client.get('/getAll')
        assert get_all.status_code == 200
        assert get_all.data == b'[{"id":1,"name":"TestName","quantity":3}]\n'

    # =====================================================#

    def test_default_url(self):
        with app.app_context():
            client = self.create_client()
            response = client.get('/')
            ### assert with render template index.html

    # =====================================================#

    def test_wrong_url(self):
        client = self.create_client()
        response = client.get('/bad/url')
        assert response.status_code == 404

    # =====================================================#
