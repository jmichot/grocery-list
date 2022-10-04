from src.connexion import get_db_connection
from src.model.product import Product


class Dao:

    def __init__(self, test=False):
        self.test = test

    def getProductById(self, product_id):
        conn = get_db_connection(test=self.test)
        cur = conn.cursor()
        res = cur.execute("""Select * from Products where id=?""", (product_id,))
        p = res.fetchone()
        conn.close()
        if p is None:
            return None
        return Product(p[0], p[1], p[2])

    def getProductByName(self, product_name):
        conn = get_db_connection(test=self.test)
        cur = conn.cursor()
        res = cur.execute("""Select * from Products where name=?""", (product_name,))
        p = res.fetchone()
        conn.close()
        if p is None:
            return None
        return Product(p[0], p[1], p[2])

    def addOneQuantity(self, product_id):
        product = self.getProductById(product_id)
        if product is None:
            raise Exception('The product does not exist')
        conn = get_db_connection(test=self.test)
        conn.execute("""Update Products set quantity=quantity+1 where id=?""", (product_id,))
        conn.commit()
        conn.close()

    def removeOneQuantity(self, product_id):
        product = self.getProductById(product_id)
        if product is None:
            raise Exception('The product does not exist')
        if product.quantity <= 1:
            self.deleteProductById(product_id)
        else:
            conn = get_db_connection(test=self.test)
            conn.execute("""Update Products set quantity=quantity-1 where id=?""", (product_id,))
            conn.commit()
            conn.close()

    def addProduct(self, product: Product):
        already_exist = self.getProductByName(product.name)
        if already_exist is not None:
            raise Exception('This name is already used by another product')
        conn = get_db_connection(test=self.test)
        conn.execute("""Insert into Products (name, quantity) values (?, ?)""", (product.name, product.quantity))
        conn.commit()
        conn.close()

    def deleteProductById(self, product_id):
        product = self.getProductById(product_id)
        if product is None:
            raise Exception('The product does not exist')
        conn = get_db_connection(test=self.test)
        conn.execute("""Delete from Products where id=?""", (product_id,))
        conn.commit()
        conn.close()

    def modifyProduct(self, product: Product):
        already_exist = self.getProductByName(product.name)
        if already_exist is not None:
            raise Exception('This name is already used by another product')
        old_product = self.getProductById(product.id)
        if old_product is None:
            raise Exception('The product does not exist')
        print(product.name, product.quantity, product.id)
        conn = get_db_connection(test=self.test)
        conn.execute("""Update Products set name=?, quantity=? where id=?""",
                          (product.name, product.quantity, product.id))
        conn.commit()
        conn.close()

    def getAll(self):
        conn = get_db_connection(test=self.test)
        cur = conn.cursor()
        products = cur.execute('SELECT * FROM Products').fetchall()
        conn.close()
        return [Product(row[0], row[1], row[2]).serialize() for row in products]
