import init_db as init_db
from src.connexion import get_db_connection
from src.dao import Dao
from src.model.product import Product
import pytest


class TestDao():
    test_id = 3
    test_quantity = 1
    test_name = "TestName"

    def init_dao(self):
        init_db.reset_db(True)
        dao = Dao(test=True)
        return dao

    def add_test_product(self):
        conn = get_db_connection(True)
        conn.execute("""Insert into Products (id,quantity,name) values (?,?,?)""", (self.test_id, self.test_quantity, self.test_name))
        conn.commit()
        conn.close()

    def get_rows(self):
        conn = get_db_connection(True)
        cur = conn.cursor()
        rows = cur.execute("""Select * From Products""").fetchall()
        conn.close()
        return rows

    def test_insert_success(self):
        dao = self.init_dao()
        product = Product(None, self.test_quantity, self.test_name)
        dao.addProduct(product)

        rows = self.get_rows()
        assert rows[0]['id'] == 1
        assert rows[0]['quantity'] == self.test_quantity
        assert rows[0]['name'] == self.test_name

    def test_insert_failed_str(self):
        dao = self.init_dao()
        product = Product(None, "not a int", self.test_name)
        with pytest.raises(ValueError):
            dao.addProduct(product)

        rows = self.get_rows()
        assert len(rows) == 0

    def test_insert_failed_quantity_none(self):
        dao = self.init_dao()
        product = Product(None, None, self.test_name)
        with pytest.raises(ValueError):
            dao.addProduct(product)

        rows = self.get_rows()
        assert len(rows) == 0

    def test_insert_failed_name_none(self):
        dao = self.init_dao()
        product = Product(None, self.test_quantity, None)
        with pytest.raises(ValueError):
            dao.addProduct(product)

        rows = self.get_rows()
        assert len(rows) == 0

    def test_insert_failed_id_not_none(self):
        dao = self.init_dao()
        product = Product(21, self.test_quantity, self.test_name)
        with pytest.raises(ValueError):
            dao.addProduct(product)

        rows = self.get_rows()
        assert len(rows) == 0

    def test_get_product_by_id_success(self):
        dao = self.init_dao()
        self.add_test_product()
        product = dao.getProductById(self.test_id)
        assert product.id == self.test_id
        assert product.quantity == self.test_quantity
        assert product.name == self.test_name

    def test_get_product_by_id_failed_wrong_id(self):
        dao = self.init_dao()
        self.add_test_product()
        product = dao.getProductById(2)
        assert product is None

    def test_get_product_by_id_failed_none_id(self):
        dao = self.init_dao()
        self.add_test_product()
        with pytest.raises(ValueError):
            dao.getProductById(None)

    def test_get_product_by_id_failed_str_id(self):
        dao = self.init_dao()
        self.add_test_product()
        with pytest.raises(ValueError):
            dao.getProductById("not id")

    def test_get_product_by_name_success(self):
        dao = self.init_dao()
        self.add_test_product()
        with pytest.raises(ValueError):
            dao.getProductById("not id")