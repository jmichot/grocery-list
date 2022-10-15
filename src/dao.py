from src.connexion import get_db_connection
from src.exceptions.IdException import IdException
from src.exceptions.NameException import NameException
from src.exceptions.ProductException import ProductException
from src.exceptions.QuantityException import QuantityException
from src.exceptions.conflictException import ConflictException
from src.model.product import Product
from src.constants import *


# Check quantity method for potential errors
def check_quantity(product_quantity):
    if product_quantity is None or type(product_quantity) is not int:
        raise QuantityException(QUANTITY_NOT_INT)
    if product_quantity <= 0:
        raise QuantityException(QUANTITY_LOWER_THAN_ONE)


# Check ID method for potential errors
def check_product_id(product_id):
    if product_id is None or type(product_id) is not int:
        raise IdException(ID_NOT_INT)


def check_product_id_set_to_none(product_id):
    if product_id is not None:
        raise IdException(ID_NONE_WHEN_ADD)


# Check name method for potential errors
def check_product_name(product_name):
    if product_name is None or type(product_name) is not str:
        raise NameException(NAME_NOT_STRING)


class Dao:

    def __init__(self, test=False): # pragma: no mutate
        self.test = test

    def check_name_already_exist(self, product_name):
        check_product_name(product_name)
        product = self.get_product_by_name(product_name)
        if product is not None:
            raise ConflictException(NAME_CONFLICT)

    # Get method
    def get_product_by_id(self, product_id):
        check_product_id(product_id)

        conn = get_db_connection(test=self.test)
        cur = conn.cursor()
        res = cur.execute("""Select * from Products where id=?""", (product_id,))
        p = res.fetchone()
        conn.close()
        if p is None:
            return None
        return Product(p[0], p[1], p[2])

    def get_product_by_name(self, product_name):
        check_product_name(product_name)

        conn = get_db_connection(test=self.test)
        cur = conn.cursor()
        res = cur.execute("""Select * from Products where name=?""", (product_name,))
        p = res.fetchone()
        conn.close()
        if p is None:
            return None
        return Product(p[0], p[1], p[2])

    def get_all_product(self):
        conn = get_db_connection(test=self.test)
        cur = conn.cursor()
        products = cur.execute('SELECT * FROM Products').fetchall()
        conn.close()
        return [Product(row[0], row[1], row[2]) for row in products]

    # Update method
    def update_product(self, product_id, product_name, product_quantity):
        # Check method
        check_product_id(product_id)
        check_quantity(product_quantity)
        check_product_name(product_name)

        if self.get_product_by_id(product_id) is None:
            raise ProductException(PRODUCT_NOT_FOUND)

        product = self.get_product_by_name(product_name)
        if product is not None and product.id != product_id:
            raise ConflictException(NAME_CONFLICT)

        conn = get_db_connection(test=self.test)
        conn.execute("""Update Products set name=?, quantity=? where id=?""",
                     (product_name, product_quantity, product_id,))
        conn.commit()
        conn.close()

    # Insert method
    def add_product(self, product: Product):
        check_product_id_set_to_none(product.id)
        check_product_name(product.name)
        check_quantity(product.quantity)
        self.check_name_already_exist(product.name)

        conn = get_db_connection(test=self.test)
        conn.execute("""Insert into Products (name, quantity) values (?, ?)""", (product.name, product.quantity))
        conn.commit()
        conn.close()

    # Delete method
    def delete_product_by_id(self, product_id):
        check_product_id(product_id)
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ProductException(PRODUCT_NOT_FOUND)  # CUSTOM EXCEPTION

        conn = get_db_connection(test=self.test)
        conn.execute("""Delete from Products where id=?""", (product_id,))
        conn.commit()
        conn.close()
