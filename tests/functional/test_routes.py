from flask import Flask
import init_db


from src import controller
from src.connexion import get_db_connection

class TestRoutes():

    def create_client(self):
        init_db.reset_db()
        app = Flask(__name__, template_folder='../../templates')
        controller.configure_routes(app)
        client = app.test_client()
        return client

    #=====================================================# 

    def test_base_route(self):
        client = self.create_client()
        url = '/'
        response = client.get(url)
        client.delete
        assert response.status_code == 200
        
    #=====================================================# 

    def test_add_one_if_exist(self):
        client = self.create_client()
        url = '/addOne?id=1' 
        response = client.post(url)
        assert response.status_code == 200
        url = '/addOne?id=2' 
        response = client.post(url)
        assert response.status_code == 200

    def test_add_one_if_not_exist(self):
        client = self.create_client()
        url = '/addOne?id=3' 
        response = client.post(url)
        assert response.status_code == 404

    #=====================================================# 

    def test_remove_one_ok(self):
        client = self.create_client()
        url = '/removeOne?id=1' 
        response = client.post(url)
        assert response.status_code == 200
        response = client.post(url)
        assert response.status_code == 200
        response = client.post(url)
        assert response.status_code == 200

    def test_remove_one_not_allowed(self):
        client = self.create_client()
        url = '/removeOne?id=1' 
        response = client.post(url)
        assert response.status_code == 200
        response = client.post(url)
        assert response.status_code == 200
        response = client.post(url)
        assert response.status_code == 200
        response = client.post(url)
        assert response.status_code == 405

    def test_remove_one_not_exist(self):
        client = self.create_client()
        url = '/removeOne?id=3' 
        response = client.post(url)
        assert response.status_code == 404
        
    #=====================================================# 

    def test_delete_all_ok(self):
        client = self.create_client()
        url = '/deleteAll?id=1' 
        response = client.post(url)
        assert response.status_code == 200

    def test_delete_all_if_not_exist(self):
        client = self.create_client()
        url = '/deleteAll?id=3' 
        response = client.post(url)
        assert response.status_code == 404

    #=====================================================# 

    def test_modify_ok(self):
        client = self.create_client()
        conn = get_db_connection() 
        product = conn.execute("""Select * from things where id=?""", (1,)).fetchall()
        old_name = product[0]['thing']
        old_quantity = product[0]['quantity']
        assert old_name == "Tomates"
        assert old_quantity == 3
        url = '/modify?id=1&quantity=20&name=Test'
        response = client.post(url)
        assert response.status_code == 200
        product = conn.execute("""Select * from things where id=?""", (1,)).fetchall()
        new_name = product[0]['thing']
        new_quantity = product[0]['quantity']
        assert new_name == "Test"
        assert new_quantity == 20

    def test_modify_if_not_exist(self):
        client = self.create_client()
        url = '/modify?id=5&quantity=20&name=Test'
        response = client.post(url)
        assert response.status_code == 404

    def test_modify_if_conflict(self):
        client = self.create_client()
        conn = get_db_connection()
        product = conn.execute("""Select * from things where id=?""", (1,)).fetchall()
        old_name = product[0]['thing']
        url = '/modify?id=1&quantity=20&name=' + old_name
        response = client.post(url)
        assert response.status_code == 409
        
    #=====================================================# 
    
    def test_add_ok(self):
        client = self.create_client()
        conn = get_db_connection()
        product = conn.execute("""Select count(*)=1 as exist from things where thing=?""", ("Test",)).fetchall()
        exist = product[0]['exist']
        assert not exist
        url = '/add?quantity=20&name=Test'
        response = client.post(url)
        assert response.status_code == 200
        product = conn.execute("""Select count(*)=1 as exist from things where thing=?""", ("Test",)).fetchall()
        exist = product[0]['exist']
        assert exist

    def test_add_if_conflict(self):
        client = self.create_client()
        conn = get_db_connection()
        product = conn.execute("""Select * from things where id=?""", (1,)).fetchall()
        old_name = product[0]['thing']
        url = '/add?quantity=20&name=' + old_name
        response = client.post(url)
        assert response.status_code == 409

    #=====================================================# 
        
    def test_get_all(self):
        client = self.create_client()
        url = '/getAll'
        response = client.get(url)
        assert response.status_code == 200
        assert response.data == b'[[1,3,"Tomates"],[2,30,"Feuilles"]]\n'


