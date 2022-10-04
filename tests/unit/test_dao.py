import init_db
from src.connexion import get_db_connection
from src.dao import Dao
from src.model.product import Product


class TestDao:

    def init_dao(self):
        init_db.reset_db(True)
        dao = Dao(test=True)
        return dao

    def test_insert_success(self):
        dao = self.init_dao()
        product = Product(None, 3, "MyTestName")
        dao.addProduct(product)

        conn = get_db_connection(True)
        cur = conn.cursor()
        rows = cur.execute("""Select * From Products""").fetchall()
        assert len(rows) == 1
        assert rows[0]['id'] == 1
        assert rows[0]['quantity'] == 3
        assert rows[0]['name'] == "MyTestName"
