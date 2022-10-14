from src.connexion import get_db_connection
from src.exceptions.IdException import IdException
from src.exceptions.NameException import NameException
from src.exceptions.QuantityException import QuantityException
from src.model.product import Product


# Check quantity method for potential errors
def check_quantity(product_quantity):
    if product_quantity is None or type(product_quantity) is not int:
        raise QuantityException('Quantity should be an integer')
    if product_quantity < 0:
        raise QuantityException('Quantity is lower than 0')


# Check ID method for potential errors
def check_product_id(product_id):
    if product_id is None or type(product_id) is not int:
        raise IdException('Id should be an integer')


# Check name method for potential errors
def check_product_name(product_name):
    if product_name is None or type(product_name) is not str:
        raise NameException('Name should be a string')


class Dao:

    def __init__(self, test=False):
        self.test = test

    def check_name_already_exist(self, product_name):
        check_product_name(product_name)
        product = self.get_product_by_name(product_name)
        if product is not None:
            raise NameException('This name is already used by another product')

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
        check_quantity(product_id)
        check_product_name(product_name)
        self.check_name_already_exist(product_name)

        product = self.get_product_by_name(product_name)
        if product is not None and product.id != product_id:
            raise ValueError('This name is already used by another product')

        conn = get_db_connection(test=self.test)
        conn.execute("""Update Products set name=?, quantity=? where id=?""",
                     (product_name, product_quantity, product_id,))
        conn.commit()
        conn.close()

    # Insert method
    def add_product(self, product: Product):
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
            raise Exception("Product not found")  # CUSTOM EXCEPTION

        conn = get_db_connection(test=self.test)
        conn.execute("""Delete from Products where id=?""", (product_id,))
        conn.commit()
        conn.close()
